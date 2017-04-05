
from math import sqrt
from random import randrange
from numpy.random import choice
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

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

def init_centroids(Lab_colors,n):
    centroid = []
    centroid.append((Lab_colors[randrange(0, len(Lab_colors))])) # one center chosen uniformly at random
    for i in range(n):
        weight = []
        distance = []
        for j in range(len(Lab_colors)):
            minimum = float("inf")
            for k in range(len(centroid)):
                delta_e = (delta_e_cie2000(centroid[k],Lab_colors[j]))
                if delta_e < minimum:
                    minimum = delta_e
            distance.append(minimum**2)
        for j in range(len(Lab_colors)):
            weight.append(distance[j] / sum(distance))
        x = choice(list(Lab_colors),p=weight)
        centroid.append(Lab_colors[x])

    return centroid

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
