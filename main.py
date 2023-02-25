import random
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import os
# tuning variables
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 174
FONT_SIZE = 65
H_PADDING = 18
V_PADDING = 10
SHOW_MAREKRS = True
SHOW_BBOX = True
xy = (H_PADDING*2, V_PADDING * 2)

SurahNameFont = ImageFont.truetype("fonts/surahNames.ttf", FONT_SIZE,encoding="unic",layout_engine=0,)


db = sqlite3.connect("database/quran-v2.db")
cursor = db.cursor()
lines = cursor.fetchall()
# # alter table words add column x_start int default 0 not null x_end int default 0 not null y_start int default 0 not null y_end int default 0 not null
# cursor.execute("alter table word add column x_start int default 0 not null")
# cursor.execute("alter table word add column x_end int default 0 not null")
# cursor.execute("alter table word add column y_start int default 0 not null")
# cursor.execute("alter table word add column y_end int default 0 not null")

def isNewChapter(word):
    return word[7] == 1
def hasStartMark(word):
    return word[2] == 'ﱨﱩ'
def renderTextOnImage(draw, x, y, text, font):
    bbox = draw.textbbox((x, y), text, font=font)
    bbox = (bbox[0], 0, bbox[2] , CANVAS_HEIGHT)
    draw.text((x, y), text, font=font, fill="black")
    if(SHOW_BBOX):
        draw.rectangle(bbox, outline="black")
    return bbox
def isMarker(word):
    return word[10] == "end"

def updateCoords(word, bbox):
        cursor.execute("UPDATE word SET x_start = " + str(bbox[0]) + " where id = " + str(word[0]))
        cursor.execute("UPDATE word SET x_end = " + str(bbox[2]) + " where id = " + str(word[0]))
        cursor.execute("UPDATE word SET y_start = " + str(bbox[1]) + " where id = " + str(word[0]))
        cursor.execute("UPDATE word SET y_end = " + str(bbox[3]) + " where id = " + str(word[0]))
        db.commit()


def generate():
    for page in range (603, 605):
        font = ImageFont.truetype("fonts/p" + str(page)+".ttf", FONT_SIZE,encoding="unic",layout_engine=0,)
        cursor.execute("SELECT * FROM line where pageID = " + str(page) + " order by id asc")
        lines = cursor.fetchall()
        lineCounter = 1
        for line in lines:
            image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
            draw = ImageDraw.Draw(image)
            cursor.execute("SELECT * FROM word where lineID ="+ str(line[0]) + " order by id desc")
            words = cursor.fetchall()
            x, y = xy
            for word in words:
                if(isNewChapter(word)):
                    renderTextOnImage(draw, x, y, word[6], SurahNameFont)
                    x += draw.textlength("x", font=font)
                    continue
                if(isMarker(word)):
                    if(SHOW_MAREKRS):
                        renderTextOnImage(draw, x, y, word[2], font)
                    x += draw.textlength(word[2], font=font)
                    continue

                # if the word has a continuatuon or stop marks the treat it as a single word otherwise it will miss the rendering
                if(len(word[2])> 1):
                    if(hasStartMark(word)):
                        word = list(word)
                        word[2] = word[2][::-1]
                        word = tuple(word)
                        renderTextOnImage(draw, x, y, word[2], font)
                        x += draw.textlength(word[2], font=font)
                        continue
                    for char in word[2]:
                        renderTextOnImage(draw, x, y, char, font)
                    x += draw.textlength(word[2], font=font)
                    continue
                bbox = renderTextOnImage(draw, x, y, word[2], font)
                # create directory for page
                if not os.path.exists("output/" + str(page)):
                    os.makedirs("output/" + str(page))
                image.save("output/" + str(page) +"/" + str(lineCounter)+ ".png")
                # do handle error using try catch
                updateCoords(word, bbox)
                x += draw.textlength(word[2], font=font)
                
            lineCounter += 1
        print("page " + str(page) + " done")

generate()   


# def getBbox(word, x, y):
#     if(len(word[2])> 1):
#             word = list(word)
#             word[2] = word[2][::-1]
#             word = tuple(word)
#             for char in word[2]:
#                 bbox = draw.textbbox((x, y), char, font=font)
#             return bbox
#     bbox = draw.textbbox((x, y), word[2], font=font)
#     bbox = (bbox[0], 0, bbox[2] , CANVAS_HEIGHT)
#     return bbox

# def incrementX(word, x, y):
#     x += draw.textlength(word[2], font=font)

#   word = list(word)
#             word[2] = word[2][0]
#             word = tuple(word)





















    # # print ready words
    # for word in ready_words:
    #     image1 = Image.new("RGB", (1080, CANVAS_HEIGHT), "white")
    #     draw1 = ImageDraw.Draw(image1)
    #     draw1.rectangle(word[-1], outline="black")
    #     draw.rectangle(bbox,
    #                     # make the outline randome
    #                     outline=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    #                    )

    #     draw.text((x, y), word[2], font=font, fill="black")
        # draw.text(, word[2], font=font, fill="black")
        
    # image1.save("test1.png")

    


        # lineCounter += 1



# if last word end is greater than current word start then collapse
    # if(lastWordEnd > bbox[0]):
    #     lastWord = ready_words[-1]
    #     lastWordBbox = lastWord[-1]
        
    #     # update bboxes for last word and current word
    #     differnce = lastWordEnd - bbox[0]
    #     differnce = differnce / 2

    #     lastWordBbox = (lastWordBbox[0], lastWordBbox[1], lastWordBbox[2] - differnce, lastWordBbox[3])
    #     bbox = (bbox[0] + differnce, bbox[1], bbox[2], bbox[3])
    #     ready_words[-1][-1] = lastWordBbox
    # ready_words.append([word[2], bbox])
    # lastWordEnd = bbox[2]
    
    # index += 1

# for line in lines:
#     if(lineCounter > 1):
#         break
#     # query select from word where lineID = line[0]
#     cursor.execute("SELECT * FROM word where lineID = 50")
#     words = cursor.fetchall()
#     x, y = xy
#     # reverse words
#     words.reverse()
#     for word in words:
#         if(word[-2] !='word'):
#             continue
        # bbox = draw.textbbox((x, y), word[2], font=font)
        # draw.rectangle(bbox, outline="black")
        # draw.text((x, y), word[2], font=font, fill="black")
        # x += draw.textlength(word[2], font=font)

#     lineCounter += 1
        
