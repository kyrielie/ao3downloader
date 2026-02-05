## What is this?

This is a fork to Nianeyna's [Archive of Our Own](https://archiveofourown.org/) fanfiction downloading program [ao3downloader](https://github.com/nianeyna/ao3downloader). The fork creates a command line argument style interface for using ao3downloader and is a archive of how I personally use ao3downloader.

## WARNINGS

PLEASE GO READ the ao3downloader README first before using this extension.

Beta software: may contain bugs or unintended behavior. Use at your own risk. Feedback and bug reports are greatly appreciated.


## Quick Start

I recommend cloning this repo and testing with that so nothing in your existing ao3downloader directory breaks.
`git clone https://github.com/kyrielie/ao3downloader`

I personally modified my existing ao3downloader directory by adding `ao3downloader/ao3downloader/cli/cli/cli.py` and replacing `pyproject.toml`.

Use `python cli.py` to download fics. (full or relative file path)

Or install using pip:
```
cd ao3downloadercli
pip install -e .
```
Run ao3downloadercli to download files.


I don't like my files going relative to which directory I'm currently in, so I make a custom shell script to run in the same directory I used to run `ao3downloader.py` before you could PyPi install.

Use the full path output of `which python` and the full path of `cli.py` in ao3downloadercli.sh and add `ao3downloadercli` to path somehow— I usually drop a symlink where my path already points for homebrew. Is this the proper way to do things? Idk it works...

# How to Use
```
usage: cli.py [-h] [--format {epub,pdf,azw3,mobi,html}] [--no-login] urlortextfile [pages]

positional arguments:
  urlortextfile         Expects one of the following:
                        1. AO3 search / paged link
                        2. AO3 work / series link
                        3. path to text file containing one search/paged link (for long links)
                        4. path to text file containing list of work/series links
  pages                 Number of pages to download. (default=1)

options:
  -h, --help            show this help message and exit
  --format {epub,pdf,azw3,mobi,html}, -f {epub,pdf,azw3,mobi,html}
                        Choose format to download. (default=EPUB)
  --no-login            Disable login (default: enabled)
  ```

Make sure you wrap urls in " quote marks `"https://archiveofourown.org/works..."` to avoid errors.

For some reason it was easiest for me to write code that expects multiple formats in the form: `-f epub -f html -f mobi` etc. But also it's not working right now idk why :sob:, so only one format at a time.

So like you could also put multiple search / paged links interspaced with work links in your text file and number of pages you want to download from each, but why would you do that. I do not recommend doing that.

Still not sure how to start from last page stopped on with this. I think if your link contains the `&page=#` at the end that is the page that you will start downloading at.

## Helpful Tips

Firefox/Chrome
- Use extensions to get links fics you have read from your history or bookmarks.
- Instead of bookmarking use OneTab, it's easier to deal with.
- When using Tumblr fic libraries use Link Gopher to get the links. Suggestions and collections by other users are the best way to reap fics! 

Safari on ios
- Hold press the obscenely large number of tabs you have open, tap `Copy links` then paste in notes or other app and get the list of hyperlinks into your text editor. Notes -> airdrop to mac -> Obsidian -> text file works well enough.

Use regex + `sort -u` to format links.

Learn how to use vim to quickly create files. I haven't lol. 

I don't keep fics in the download folder, I use Calibre to manage them. Well, fail to manage them. But that means to avoid redundant downloads I use.

```
cat links.txt ignorelist.txt > temporary.txt
sort -u temporary.txt > ignorelist.txt
```

Sometimes the join is two links on the same line that you have to go in and fix.

### AO3 Searching

So the reason I wrote this originally is not because I am a habitual CLI data hoarder. I am that, but also before I discovered a way to get an OR search to work on AO3 I required massive links that excluded so much stuff I had already read or didn't want to read.

Those search links were so incredibly massive that they maxed out my browser url limit (2000 characters) but before that point they maxed out my terminal paste limit. There may be a way to fix `input()` like that but I wanted to stop having to tell ao3downloader my preferences each time anyways and just type out one command.

I later found that you can simply use and OR operator in the [Search Within Results](https://archiveofourown.org/admin_posts/329) field. You can also use a NOT operator to filter out specific authors.

These are ids for the fandoms I'm in:
`fandom_ids:143679061 OR fandom_ids:2692 OR fandom_ids:5450 OR fandom_ids:6943 OR fandom_ids:101375 OR fandom_ids:136512 OR fandom_ids:232768 OR fandom_ids:236208 OR fandom_ids:258526 OR fandom_ids:524391 OR fandom_ids:658827 OR fandom_ids:969647 OR fandom_ids:1147379 OR fandom_ids:8774227 OR fandom_ids:10104017 OR fandom_ids:17959080 OR fandom_ids:18245130 OR fandom_ids:27251507 OR fandom_ids:42817852 OR fandom_ids:74497137 OR fandom_ids:109615657 OR fandom_ids:124953688 OR fandom_ids:541437 OR fandom_ids:190901`

To get the fandom id tag, you can use the checkboxes in the exclude section and keep excluding everything while sorting in a popular tag, then unchecking everything you don't want to get a url contianing all the (encoded) tags you want. Then just decode that url and format the ids how you need.

My previous scripts were named epub.py and sendlink.py, very descriptive and very intuitive. Epub did text files with links and sendlink dealt with links nad text files with links. Or something. I really forgot, which is why I needed to rewrite them and properly document everything. Luckily I remembered enough that I was able to merge the two together.

