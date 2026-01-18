import os
import argparse

from ao3downloader import strings
from ao3downloader.actions import shared
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository

from tqdm import tqdm

# modified from ao3download.py and enterlinks.py

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description="CLI arguments interface for ao3downloader")
    parser.add_argument("urlortextfile",
    help=(
    "Expects one of the following:"
    "\n1. AO3 search / paged link"
    "\n2. AO3 work / series link"
    "\n3. path to text file containing one search/paged link (for long links)"
    "\n4. path to text file containing list of work/series links")
    )
    parser.add_argument("pages", 
    type=int, 
    nargs="?", 
    help="Number of pages to download. (default=1)")
    parser.add_argument("--format","-f", 
    choices=["epub","pdf","azw3","mobi","html"], 
    default="epub", 
    help="Choose format to download. (default=EPUB)")
    parser.add_argument("--no-login",
    dest="login",
    action="store_false",
    help="Disable login (default: enabled)"
    )

    args = parser.parse_intermixed_args()

    pages = args.pages if args.pages is not None else 1

    try:
        if testiflink(testlink=args.urlortextfile):
            downloadfromlink(rawlink=args.urlortextfile, pages=pages, filetypes=[args.format.upper()],login=args.login)

        else:
            fromfile(filepath=args.urlortextfile,pages=pages,filetypes=[args.format.upper()],login=args.login)
    
    except Exception:
        raise

def downloadfromlink(rawlink,pages=1,filetypes=None,login=True):
    """Takes ao3 link and downloads all works from specified pages"""
    fileops = FileOps()
    with Repository(fileops) as repo:

        if filetypes is None:
            filetypes = ["EPUB"]

        # Always get series, no images (add flag later)
        series = True
        images = False

        link = rawlink.strip()

        # account = loadaccount()
        # print('logging in')
        # repo.login(account['username'], account['password'])
        # print('login success')
        if login:
            shared.ao3_login(repo, fileops, force=True)

        visited = shared.visited(fileops, filetypes)

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, filetypes, pages, series, images)
        ao3.download(link, visited)

def fromfile(filepath,pages=1,filetypes=None,login=True):
    """Takes long link from file and downloads all works from specified pages"""
    fileops = FileOps()
    with Repository(fileops) as repo:

        if filetypes is None:
            filetypes = ["EPUB"]

        # Always get series, no images (add flag later)
        series = True
        images = False

        with open(filepath) as f:
            links = f.readlines()

        if not links:
            raise ValueError("Input file is empty.")

        link = links[0].strip()
        
        if login:
            shared.ao3_login(repo, fileops, force=True)
        
        visited = shared.visited(fileops, filetypes)

        # test what kinds of links are present

        if testworklink(link):
            print(strings.AO3_INFO_DOWNLOADING)
            ao3 = Ao3(repo, fileops, filetypes, pages, series, images)
            for link in tqdm(links):
                ao3.download(link.strip(), visited)
        else:
            print(link)
            print(strings.AO3_INFO_DOWNLOADING)
            ao3 = Ao3(repo, fileops, filetypes, pages, series, images)
            ao3.download(link, visited)

def testiflink(testlink):
    """Check if AO3 link and integer before passing"""
    if testlink.startswith("https://archiveofourown.org"):
        return True
    if testlink.endswith(".txt"):
        return False
    if testlink.startswith("https://"):
        raise ValueError("Not an AO3 link!")
    raise ValueError("Not a text file!")

def testworklink(testlink):
    """Check if link is to a single fic/series"""
    if testlink.startswith("https://archiveofourown.org/works/"):
        return True
    if testlink.startswith("https://archiveofourown.org/series/"):
        return True
    if testlink.startswith("https://archiveofourown.org/collections/") and "/works/" in testlink:
        return True
    else:
        return False

if __name__ == "__main__":
    main()