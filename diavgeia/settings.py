# Scrapy settings for diavgeia project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#


SPIDER_MODULES = ['diavgeia.spiders']
NEWSPIDER_MODULE = 'diavgeia.spiders'
ITEM_PIPELINES = { 
    'diavgeia.pipelines.DownloaderPipeline': 100
}
DOWNLOAD_HANDLERS = {'s3': None,}
# DownloaderPipeline settings

# Directory where Diavgeia PDFs are saved.
DOWNLOAD_DIR = '/tmp/diavgeia'

# Concurrent threads for downloading.
THREADS = 15
