import os
import zopfli

# compressing script using zopfli
# good quality but really slow
def main():
    for page in range (1,605):
        # for all the images in the page folder
        for image_file in os.listdir("output/" + str(page) + "/"):
            fileName = "output/" + str(page) + "/" + image_file
            with open(fileName, 'rb') as fp:
                data = fp.read()
            png = zopfli.ZopfliPNG()
            img = png.optimize(data)
            with open(fileName, 'wb') as fp:
                fp.write(img)
        print ("page " + str(page) + " done")


if __name__ == "__main__":
    main()