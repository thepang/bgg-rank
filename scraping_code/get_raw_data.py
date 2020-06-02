import math
import time

import requests
from bs4 import BeautifulSoup

from scraping_code import nucleus as n


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

    if n.file_exists(save_location):
        return save_location

    r = requests.get(url)

    if r.status_code != 200:
        raise Exception(
            f"Did not connect successfully. HTTP status code: {r.status_code}\nURL: {url}"
        )

    soup = BeautifulSoup(r.text, "lxml")

    print(f"Saving to {save_location}")
    with open(save_location, "w") as file:
        file.write(soup.prettify())

    if return_html:
        return soup.prettify()
    else:
        return None


def get_xml(game_ids, save_location):
    """
    Pass in a list of game ids, use BGG's XML API to get game metadata.
    Writes out results to CSV.
    :param game_ids: navigates to provided URL
    :param save_location: place where XMLs should be stored
    :raises Exception: Error from API
    """

    print(f"Found {len(game_ids)} ids to check...")

    games_to_check = list()

    for i in game_ids:
        i = str(i)
        if not n.file_exists(f"{save_location}/xml_{i.zfill(7)}"):
            games_to_check.append(i)
    print(
        f"Skipping {len(game_ids)-len(games_to_check)} files because they were already found"
    )

    batches = 200
    batch_no = math.ceil(len(game_ids) / batches)
    i = 1

    for chunk in n.chunker(games_to_check, batches):
        print(f"Processing {i}/{batch_no} of batches")
        s = [str(game_id) for game_id in chunk]
        chunk_ids = ",".join(s)

        url = f"https://www.boardgamegeek.com/xmlapi/boardgame/{chunk_ids}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        with open(f"{save_location}/xml_batch_{i:04}.xml", "w") as file:
            file.write(soup.prettify())

        time.sleep(5)

    print("Complete!")
