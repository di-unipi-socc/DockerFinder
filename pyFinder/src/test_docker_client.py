from pyDescriptor import ClientHub
import unittest

class TestClientHub(unittest.TestCase):

    def setUp(self):
        self.cHub = ClientHub()

    #@unittest.skip("Skipping test_get_tags")
    def test_get_tags(self):
        #repo_name = "library/java"
        repo_name ="andoladockeradmin/ubuntu"
        list_tags = self.cHub.get_all_tags(repo_name)
        count_tags = self.cHub.get_num_tags(repo_name)
        print(repo_name+": ")
        print(list_tags)
        self.assertEquals(len(list_tags), count_tags)

    @unittest.skip("Skipping test_crawl_images")
    def test_crawl_images(self):
        max_images = 50
        num_images = 0
        for list_images in self.cHub.crawl_images(page=1, page_size=10, max_images=max_images):
            num_images += len(list_images)
        self.assertEquals(max_images, num_images)

    def test_get_repo(self):
        json_image= self.cHub.get_json_repo("library/java")
        self.assertEquals(json_image['name'], 'java')

        json_image = self.cHub.get_json_repo("norepo/noimage")
        self.assertDictEqual(json_image, {})

    def test_count_all_images(self):
        count = self.cHub.count_all_images()
        self.assertGreater(count, 323650)   # 9 Luglio 2016