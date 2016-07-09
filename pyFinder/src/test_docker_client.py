from pyDescriptor import ClientHub
import  unittest
class TestClientHub(unittest.TestCase):

    def setUp(self):
        self.cHub = ClientHub()

    def test_get_tags(self):
        repo_name = "library/java"
        list_tags = self.cHub.get_all_tags(repo_name)
        count_tags = self.cHub.get_count_tags(repo_name)
        self.assertEquals(len(list_tags), count_tags)

    def test_crawl_images(self):
        max_images = None
        num_images = 0
        for list_images in self.cHub.crawl_images(page=1, page_size=10, max_images=max_images):
            num_images += len(list_images)
        self.assertEquals(max_images, num_images)

