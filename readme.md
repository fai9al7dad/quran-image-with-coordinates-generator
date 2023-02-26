# quran image with coordinates generator

a script that takes a QCF font and generates line by line images with each word coordinates and updates the database with x_start,x_end,y_start,y_end coordinates.

## Prerequisites

- python (tested on python 3.10)
- pillow package
- sqlite3 package
- QCF font from [here](https://github.com/quran/quran.com-frontend-next/tree/master/public/fonts/quran/hafs/v2/ttf). should also work with the old one and a new one if released
- a database (available on clone)

## the database

its a custom database that is scrapped from quran com api. some missing stuf like bismillah location and surah names with its lines and fixed some bugs.
the goal was to get line by line for every page, instead of the whole text as once. [see source code](https://github.com/fai9al7dad/quran-starter-api/tree/Main/src/utils)

## database schema

![database schema](/images/readme/quran_schema.png "database schema")

## database in practice

![database in practice](/images/readme/database_in_practice.png "database in practice")

## tuning variables

in the main.py you can configure how the output images look

```python
# --- Tuning variables
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 174
FONT_SIZE = 65
H_PADDING = 0
V_PADDING = 19
SHOW_MAREKRS = False
IS_THICK_TEXT = False # makes the text more thick
SHOW_BBOX = False # shows bbox around each glyph
PAGE_RANGES = [1, 604]
OUTPUT_FOLDER = "output/"
# --- End of tuning variables
```

## example output

with

```python
....
SHOW_BBOX = True
SHOW_MARKERS = True
IS_THICK_TEXT = False
....
```

and with a white background
![output example 1](/images/readme/output.png "output example 1")
with

```python
....
SHOW_BBOX = False
SHOW_MARKERS = False
IS_THICK_TEXT = True
....
```

and trasnparent background

![output example 2](/images/readme/output_2.png "output example 2")

## usage

1. download packages
2. put fonts folder in root
3. run main.py
4. run compress.py (recomended)

or just download the images from [here](https://drive.google.com/drive/folders/1EGmE-mihzC7pLilGA6_NCvdJQb2sXiiS?usp=share_link) and download the database from this repo and enjoy :)

## credits

huge thanks to [quran.com](https://github.com/quran) community for providing their api and fonts
