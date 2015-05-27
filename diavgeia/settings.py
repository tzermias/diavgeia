# Scrapy settings for diavgeia project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'diavgeia'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['diavgeia.spiders']
NEWSPIDER_MODULE = 'diavgeia.spiders'
ITEM_PIPELINES = [ 
#    'diavgeia.pipelines.DownloaderPipeline' 
]
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# DownloaderPipeline settings

# Directory where Diavgeia PDFs are saved.
DOWNLOAD_DIR = '/tmp/diavgeia'

# Concurrent threads for downloading.
THREADS = 15
