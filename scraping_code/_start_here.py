import os
import time

import pandas as pd
from dotenv import load_dotenv

from scraping_code import aws as aws
from scraping_code import get_raw_data as grd
from scraping_code import nucleus as n
from scraping_code import refine_data as ph

# Local directory info
ROOT = "/Users/pang/repos/bgg-rank"
RAW_HTML = "data/01_raw_htmls"
RAW_XML = "data/02_raw_xmls"
PARSED = "data/03_parsed"
GAME_IDS = "game_id_name_rating.csv"

# AWS info
PREFIX = "data"

# Get html from board game rank list.
# This needs to be done first so get the board game IDs
for page_no in range(1, 256):
    if len(str(page_no)) == 1:
        page_no_padded = f"00{page_no}"
    elif len(str(page_no)) == 2:
        page_no_padded = f"0{page_no}"
    else:
        page_no_padded = page_no

    html = grd.get_html(
        f"https://boardgamegeek.com/browse/boardgame/page/{page_no}?sort=bggrating&sortdir=desc",
        f"{ROOT}/{RAW_HTML}/html_{page_no_padded}.txt",
    )

    # Verifying that get_html is not returning a file path.
    if ROOT not in str(html):
        time.sleep(5)

# Parse html from board game rank list to CSV if CSV doesn't exist.
if not n.check_file(f"{ROOT}/{PARSED}/{GAME_IDS}"):
    data_to_save = ph.parse_bgg_list_page(f"{ROOT}/{RAW_HTML}")
    data = pd.DataFrame(data_to_save).T
    data.to_csv(f"{ROOT}/{PARSED}/{GAME_IDS}", index_label="game_id")

data = pd.read_csv(f"{ROOT}/{PARSED}/{GAME_IDS}", index_col="game_id")
grd.get_xml(list(data.index.values), f"{ROOT}/{RAW_XML}")

# Store CSV in S3
load_dotenv()
ACCESS = os.getenv("ACCESS_KEY")
SECRET = os.getenv("SECRET_KEY")

S3 = aws.S3Client(ACCESS, SECRET, bucket="ds-boardgamegeek")
key = f"{PREFIX}/{GAME_IDS}"
S3.upload(data.to_csv(index_label="game_id"), key)
