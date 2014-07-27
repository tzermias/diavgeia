from Queue import *
from threading import Thread, RLock
import urllib
import os
import subprocess
from time import sleep
from scrapy import log
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.stats import stats
import datetime, dateutil.parser

class DownloaderPipeline(object):
    """ Threaded downloader to fetch decisions more quickly """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        """ Instantiate the Queue, Threads """
        self.queue = Queue()
        self.spider = ""
        self.lock = RLock()
        self.settings = settings
        self.stats = stats
        dispatcher.connect(self.spider_closed, signals.spider_closed)

        # Instantiate Threads
        for i in range(self.settings['THREADS']):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

        # Wait for the queue...
        self.queue.join()

        # Check whether download dir exists.
        if not os.path.exists(self.settings['DOWNLOAD_DIR']):
            log.msg("Directory %s does not exist." %\
                self.settings['DOWNLOAD_DIR'], level=log.DEBUG)
            os.mkdir(self.settings['DOWNLOAD_DIR'])
        else:
            log.msg("Directory %s exists!" % self.settings['DOWNLOAD_DIR'],
            level=log.DEBUG)

    def worker(self):
        """ Worker. Gets a URL from the Queue and tries to download it """
        while True:
            item = self.queue.get()
            log.msg("Downloading %s ..." %item[0], level=log.DEBUG)
            #Encode URL with percent encoding top avoid 
            url = urllib.quote(item[1].encode('utf-8')).replace("%3A", ':')

            # Check whether  organizationId directory exists and if not,
            # create it.
            if not os.path.exists("%s/%s" % (self.settings['DOWNLOAD_DIR'], item[2])):
                os.mkdir("%s/%s" % (self.settings['DOWNLOAD_DIR'], item[2]))

            try:
                urllib.urlretrieve(url, "%s/%s/%s.pdf" % (self.settings['DOWNLOAD_DIR'],
                    item[2], item[0]))
                #Increment a threadsafe counter here...
                with self.lock:
                    self.stats.inc_value('ThreadedDownloader/files_downloaded')

            except IOError as e:
                log.err(e)
            finally:
                self.queue.task_done()

    def spider_closed(self, spider):
        # If queue has unfinished tasks when the spider closes, just wait them
        # to finish and print a verbose message every 30 seconds with the
        # current queue size.
        while self.queue.unfinished_tasks > 0 :
            log.msg("Queue has %s unfinished tasks! Waiting for them to finish..." % self.queue.unfinished_tasks,
                    level=log.INFO )
            sleep(30)
        log.msg("All tasks are finished", level=log.INFO)

    def process_item(self, item, spider):
        """ Put each document URL to the Queue """
        self.spider = spider
        log.msg("Downloading item %s" % item['ada'],level=log.DEBUG)
        self.queue.put((item['ada'], item['documentUrl'], item['organizationId']))

        return item

# vi: ts=4 sts=4 et sw=4 tw=80
