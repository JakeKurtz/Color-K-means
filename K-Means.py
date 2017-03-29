import colorsys
from math import sqrt
from random import randrange
from PIL import Image, ImageDraw
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

SIZE = 150
loop = True

def find_center(cluster):
    r_mean = 0
    g_mean = 0
    b_mean = 0
    nmb_colors = 0
    if len(cluster)>0:
        for i in range(len(cluster)):
            r,g,b,a = cluster[i][1]
            m = cluster[i][0] # color magnitude
            r_mean += m*(r**2)
            g_mean += m*(g**2)
            b_mean += m*(b**2)
            nmb_colors += m
        r = sqrt(r_mean/nmb_colors)
        g = sqrt(g_mean/nmb_colors)
        b = sqrt(b_mean/nmb_colors)
        lab = convert_color(sRGBColor(r,g,b), LabColor)
        return lab
    else:
        return ()

def k_means(Lab_colors, RGB_colors, k, centroid):

    cluster = [[] for i in range(k)]

    for i in range(len(Lab_colors)):
        minimum = float("inf")
        for j in range(k):
            delta_e = (delta_e_cie2000(Lab_colors[i] ,centroid[j]))
            if delta_e < minimum:
                minimum = delta_e
                idx = j
        cluster[idx].append(RGB_colors[i])

    for i in range(k):
        centroid[i] = find_center(cluster[i])
        if centroid[i] == ():
            centroid[i] = ((Lab_colors[randrange(0, len(Lab_colors))]))

    return centroid

def main():

    infile = input('Enter file name: ')
    image = Image.open(infile)
    image = image.convert('RGB')
    image = image.resize((SIZE, SIZE))
    image = image.convert('P', palette=Image.ADAPTIVE, colors=256)
    image.putalpha(0)

    # Getting colors from picture
    rgb_color = image.getcolors(256)

    k = int(input('Enter number of clusters: '))

    DICT_RGB_COLOR = {}
    DICT_LAB_COLOR = {}

    centroid = []
    rgb_centroid = []

    # Creating RGB dictionary
    i = 0
    for color in rgb_color:
        DICT_RGB_COLOR[i] = color
        i += 1

    # Creating Lab dictionary
    for key in DICT_RGB_COLOR:
        DICT_LAB_COLOR[key] = (
        convert_color(sRGBColor(DICT_RGB_COLOR[key][1][0], DICT_RGB_COLOR[key][1][1], DICT_RGB_COLOR[key][1][2]),
                      LabColor))

    # Initializing lists
    for i in range(k):
        rgb_centroid.append([])
        centroid.append((LabColor(randrange(0, 100), randrange(-86, 98), randrange(-107, 94))))

    # How many iterations to run k-means
    for i in range(15):
        centroid = k_means(DICT_LAB_COLOR,DICT_RGB_COLOR,k,centroid)

    # Converting Lab centroids into RGB
    for i in range(k):
        rgb_centroid[i] = convert_color(centroid[i], sRGBColor)
        rgb_centroid[i] = rgb_centroid[i].get_value_tuple()
        rgb_centroid[i] = (round(rgb_centroid[i][0]),round(rgb_centroid[i][1]),round(rgb_centroid[i][2]))

    rgb_centroid.sort(key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
    horizontal = 1000/k
    pal = Image.new('RGB', (1000, 1000))
    draw = ImageDraw.Draw(pal)

    posx = 0
    for i in range(k):
        draw.rectangle([posx, 0, posx+horizontal, 1000], fill=rgb_centroid[i])
        posx += horizontal

    del draw

    pal.save(infile+'-gradient'+'.PNG')

main()































