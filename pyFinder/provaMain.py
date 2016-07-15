from pyfinder import Scanner
from pyfinder import Crawler
from pyfinder import ClientApi
from pyfinder import pull_image
import json
import re


if __name__ == "__main__":
    regex = re.compile('[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*')
    v = """This is perl 5, version 22, subversion 2 (v5.22.2) built for x86_64-linux-thread-multi
        (with 15 registered patches, see perl -V for more detail)

        Copyright 1987-2015, Larry Wall

        Perl may be copied only under the terms of either the Artistic License or the
        GNU General Public License, which may be found in the Perl 5 source kit.

        Complete documentation for Perl, including FAQ lists, should be found on
        this system using "man perl" or "perldoc perl".  If you have access to the
        Internet, point your browser at http://www.perl.org/, the Perl Home Page.
        """
    match = regex.search(v)
    #print(match.group(0)+"#######################à")

    #c = Crawler(rabbit_host='172.17.0.3,  url_api="http://127.0.0.1:8000/api/images"')
    #s = Scanner(host_rabbit='172.17.0.3',  url_api="http://127.0.0.1:8000/api/images")

    #u = ClientApi(url_api="http://127.0.0.1:8000/api/images/")

    pull_image("vimagick/python")

    d = {
        "description": "Python is nothing.",
        "full_size": 5,
        "star_count": 6,
        "distro": "fedora",
        "pull_count": 55555,
        "last_updated": "2016-07-05T18:12:22.565Z",
        "repo_name": "a caso",
        "last_scan": "2016-07-07T14:24:48.859Z",
        "bins": [
            {
                "ver": "8888",
                "bin": "python"
            },
            {
                "ver": "99999",
                "bin": "python3"
            },
            {
                "ver": "33333",
                "bin": "curl"
            }
        ]
    }
    #u.put_image(d)
    #u.post_image()
    #s.scan("kino/fedora")

    #s = s.scan("library/java")

    #print(s.is_scan_updated("editoo/utils"))
    #print(s.must_scanned("editoo/ut"))
    #c.crawl(page_size=10,tot_image=10)

    #print(len(c.get_crawled_images()))
    #print(str([c.repo_name for c in c.get_crawled_images()]))

    #image = "nginx"
    #pull_image(image)


    # p = s.scan('editoo/utils')
    # u.post_image(p)
    #print(p)
    #u = s.scan('ubuntu')

    #j = s.scan('nginx')
    #print(json.dumps(p, indent=4))
    # enricobomma/docker-whale

    #response = c.post_image(p)
   # print(response)
    # print(c.get_images())


    # for im in c.get_crawled_images():
    #      if im.repo_name !="luminarytech/recchanges-server-prod":
    #          image = s.scan(im.repo_name)
    #          print(im)
    #          u.post_image(image)






