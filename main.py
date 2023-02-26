import sqlite3
from PIL import Image, ImageDraw, ImageFont
import os

# --- Tuning variables
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 174
FONT_SIZE = 65
H_PADDING = 0
V_PADDING = 19
SHOW_MAREKRS = False
IS_THICK_TEXT = True
SHOW_BBOX = False
PAGE_RANGES = [19, 604]
# --- End of tuning variables

xy = (H_PADDING*2, V_PADDING * 2)
db = sqlite3.connect("database/quran-v2.db")
cursor = db.cursor()
lines = cursor.fetchall()

def isNewChapter(word):
    return word[7] == 1

def hasStartMark(word):
    return word[2] == 'ﱨﱩ'

def isMarker(word):
    return word[10] == "end"

def isBismillah(word):
    return word[8] == 1


def renderTextOnImage(draw, x, y, text,font,fill="black",stroke_width=1, stroke_fill="black",isMarker=False,lineLength=1):
    if not IS_THICK_TEXT and stroke_width == 1:
        stroke_width = 0
    bbox = draw.textbbox((x, y), text, font=font,)
    bbox = (bbox[0], 0, bbox[2] , CANVAS_HEIGHT)
    draw.text((x , y), text, font=font, fill=fill,stroke_width=stroke_width, stroke_fill=stroke_fill)
    if(SHOW_BBOX):
        draw.rectangle(bbox, outline="black")
    return bbox

def updateCoords(rowID, bbox):
        cursor.execute("UPDATE word SET x_start = " + str(bbox[0]) + " where id = " + str(rowID))
        cursor.execute("UPDATE word SET x_end = " + str(bbox[2]) + " where id = " + str(rowID))
        cursor.execute("UPDATE word SET y_start = " + str(bbox[1]) + " where id = " + str(rowID))
        cursor.execute("UPDATE word SET y_end = " + str(bbox[3]) + " where id = " + str(rowID))
        db.commit()

def generate():
    if(PAGE_RANGES[0] > PAGE_RANGES[1]):
        raise Exception("Page range is not valid")
    for page in range (PAGE_RANGES[0], PAGE_RANGES[1] + 1):
        if not os.path.exists("output/" + str(page)):
            os.makedirs("output/" + str(page))
        font = ImageFont.truetype("fonts/p" + str(page)+".ttf", FONT_SIZE,encoding="unic",layout_engine=0,)
        cursor.execute("SELECT * FROM line where pageID = " + str(page) + " order by id asc")
        lines = cursor.fetchall()
        lineCounter = 1
      
        for line in lines:
            image = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            cursor.execute("SELECT * FROM word where lineID = "+ str(line[0]) + " order by id desc")
            words = cursor.fetchall()
            lineLength = 0
            for word in words:
                if(isNewChapter(word) or isBismillah(word)):
                    continue
                lineLength += draw.textlength(word[2], font=font)
            x, y = xy
            x += (CANVAS_WIDTH - lineLength) / 2 # to add offset to the start to center it
            for word in words:
                if(isNewChapter(word)):
                    if(isBismillah(word) and page != 187 ): # 187 = surah tawbah
                        bismillahImage = Image.open("images/bismillah.png")
                        bismillahImage.save("output/" + str(page) +"/" + str(lineCounter)+ ".png")
                        break
                    surahNameImage = Image.open("images/quranLines/" +str(page) +"/"+ str(lineCounter) + ".png" )
                    surahNameImage.save("output/" + str(page) +"/" + str(lineCounter)+ ".png")
                    break
                if(isMarker(word)):
                    if(SHOW_MAREKRS):
                        bbox = renderTextOnImage(draw, x, y, word[2], font,fill="#887f6e",stroke_fill="#c5bdb2",stroke_width=1,isMarker=True,lineLength = lineLength)
                        updateCoords(word[0], bbox)
                    else:
                        bbox = draw.textbbox((x, y), word[2], font=font)
                        bbox = (bbox[0], 0, bbox[2] , CANVAS_HEIGHT)
                        updateCoords(word[0], bbox)
                    x += draw.textlength(word[2], font=font)
                    continue

                # if the word has a continuatuon or stop marks flip it
                if(len(word[2])> 1):  
                    word = list(word)
                    word[2] = word[2][::-1]
                    word = tuple(word)
                
                bbox = renderTextOnImage(draw, x, y, word[2], font,lineLength = lineLength)
                updateCoords(word[0], bbox)
                x += draw.textlength(word[2], font=font)
            resizedImage = image.resize((CANVAS_WIDTH , CANVAS_HEIGHT ), Image.LANCZOS)
            # if the resized image is not empty save it
            if(resizedImage.getbbox()):
                resizedImage.save("output/" + str(page) +"/" + str(lineCounter)+ ".png")
            lineCounter += 1
        print("page " + str(page) + " done")

generate()   


# NOTES:
# 1- coords of surah name and bismillah are not updated
# 2- the script is not optimized and it is not the best way to do it but it works
