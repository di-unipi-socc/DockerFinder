
from pyDescriptor import Crawler

if __name__ == "__main__":
    c = Crawler()
    c.crawl(max_images=1000, from_page=1, page_size=100)