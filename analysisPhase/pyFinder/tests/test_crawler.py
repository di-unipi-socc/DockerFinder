import unittest
from pyfinder import Crawler

class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.n = 10

    def test_crawl(self):
        self.crawler.run()

    @unittest.skip("Skipping test_build")
    def test_build_test(self):
        images = self.crawler.build_test(num_images_test=self.n)
        self.assertEqual(len(images), self.n)

    @unittest.skip("Skipping test_load test")
    def test_load_test(self):
        load = self.crawler.load_test_images()
        self.assertEqual(self.n, len(load))


if __name__ == '__main__':
    unittest.main()
