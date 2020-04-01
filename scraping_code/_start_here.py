import time

from scraping_code import get_htmls as gh

ROOT = "/Users/pang/repos/bgg-rank"

for page_no in range(1, 256):
    if len(str(page_no)) == 1:
        page_no_padded = f"00{page_no}"
    elif len(str(page_no)) == 2:
        page_no_padded = f"0{page_no}"
    else:
        page_no_padded = page_no

    html = gh.get_html(
        f"https://boardgamegeek.com/browse/boardgame/page/{page_no}?sort=bggrating&sortdir=desc",
        f"{ROOT}/data/01_htmls/html_{page_no_padded}.txt",
    )

    # Verifying that get_html is not returning a filepath.
    if ROOT not in str(html):
        time.sleep(5)
