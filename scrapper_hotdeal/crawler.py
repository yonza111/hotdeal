from scrapy import cmdline

def run_scrapy_crawler():
    cmdline.execute("scrapy crawl hotdeal".split())
    # cmdline은 리스트를 인자로 받음