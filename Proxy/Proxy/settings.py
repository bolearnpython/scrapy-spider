# -*- coding: utf-8 -*-

# Scrapy settings for Proxy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Proxy'

SPIDER_MODULES = ['Proxy.spiders']
NEWSPIDER_MODULE = 'Proxy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the
# user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# 设置Log级别::
# LOG_LEVEL = 'INFO'#默认'debug'
#LOG_ENABLED= True
# LOG_FILE='log'   #文件名

# 禁止cookies::
# COOKIES_ENABLED = False
# COOKIES_DEBUG

# timeout
# DOWNLOAD_TIMEOUT = 10      # 3mins

# 爬取URL的最大长度
# URLLENGTH_LIMIT = 2083

# 禁止重试::
# RETRY_ENABLED = False
# RETRY_TIMES=2
# RETRY_HTTP_CODES=[500, 502, 503, 504, 400, 408]

# #关闭重定向::
# REDIRECT_ENABLED = False
# REDIRECT_MAX_TIMES=20
# 单个request被重定向的最大次数。
# REDIRECT_MAX_METAREFRESH_DELAY=100
# 有些网站使用 meta-refresh 重定向到session超时页面，
# 因此我们限制自动重定向到最大延迟(秒)。
# REDIRECT_PRIORITY_ADJUST
# 默认: ``+2``
# 修改重定向请求相对于原始请求的优先级。
# 负数意味着更多优先级。

# #depth防止死循环
# 爬取网站最大允许的深度(depth)值。如果为0，则没有限制。
# DEPTH_LIMIT = 0
# 整数值。用于根据深度调整request优先级。
# 如果为0，则不根据深度进行优先级调整。
# DEPTH_PRIORITY = 0
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Proxy.middlewares.ProxySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'Proxy.middlewares.UserAgentMiddleware_pc': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'Proxy.pipelines.ProxyDuplicatesPipeline': 200,
   'Proxy.pipelines.ProxyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# 自动限速
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See
# http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = True
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
