import nucleus as n
import requests
from bs4 import BeautifulSoup


def get_html(url, save_location, return_html=False):
    """
    Goes to provided URL and saves the raw HTML into provided save_location.
    Skips process if file already exists in location.
    :param url: navigates to provided URL
    :param save_location: place to save raw HTMLs, include the final name.
    :param return_html: returns raw HTML for further processing if set to True.
    :return: raw HTML if return_html is true, file location if html already exists.
    :raises Exception: Page was not accessible
    """

    if n.check_file(save_location):
        return save_location

    r = requests.get(url)

    if r.status_code != 200:
        raise Exception(
            f"Did not connect successfully. HTTP status code: {r.status_code}\nURL: {url}"
        )

    soup = BeautifulSoup(r.text, "lxml")

    with open(save_location, "w") as file:
        file.write(soup.prettify())

    if return_html:
        return soup.prettify()
    else:
        return None
