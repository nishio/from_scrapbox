import dotenv
import requests
import dotenv
import os
import unittest
from .url import get_api_url

dotenv.load_dotenv()
SID = os.getenv("SID")  # required when reading from private Scrapbox project


API_ME = "https://scrapbox.io/api/users/me"


def read_private_pages(url):
    cookie = "connect.sid=" + SID
    r = requests.get(API_ME, headers={"Cookie": cookie})
    r.raise_for_status()
    csrfToken = r.json()["csrfToken"]

    api_url = get_api_url(url)
    r = requests.get(
        api_url,
        headers={
            "Cookie": cookie,
            "Accept": "application/json, text/plain, */*",
            "X-CSRF-TOKEN": csrfToken,
        },
    )
    r.raise_for_status()
    return r.json()


def read_page(url):
    """
    url example: https://scrapbox.io/nishio/%F0%9F%A4%962023-08-13_07:08
    """
    import requests

    api_url = get_api_url(url)
    try:
        page = requests.get(api_url).json()
    except:
        # assume that the page is private
        from .read_private_project import read_private_pages

        page = read_private_pages(url)

    return page


class TestExtractPreviousNotes(unittest.TestCase):
    def test_1(self):
        data = read_private_pages("https://scrapbox.io/enchi/favicon")
        self.assertEqual(data["title"], "favicon")

    def test_2(self):
        data = read_page("favicon")
        self.assertEqual(data["title"], "favicon")


if __name__ == "__main__":
    unittest.main()
