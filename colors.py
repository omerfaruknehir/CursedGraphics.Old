import json
d = open('./table.json', 'r')
colors = json.loads(d.read(),)
d.close()

import math

def GetColorByName(name:str):
    for c in colors:
        if c["name"] == name:
            return c
    return None

import colorsys

def rgb_to_hsv(rgb_color):
    r, g, b = rgb_color
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v

def color_hsv_distance(rgb1, rgb2):
    hsv1 = rgb_to_hsv(rgb1)
    hsv2 = rgb_to_hsv(rgb2)
    distance = math.sqrt((hsv1[0] - hsv2[0])**2 + (hsv1[1] - hsv2[1])**2 + (hsv1[2] - hsv2[2])**2)
    return distance

def color_distance(rgb1, rgb2):
    distance = math.sqrt((rgb1[0] - rgb2[0])**2 + (rgb1[1] - rgb2[1])**2 + (rgb1[2] - rgb2[2])**2)
    return distance

def find_nearest_color(target_color:tuple):
    nearest_color = None
    min_distance = float('inf')

    for color in colors:
        distance = color_distance(target_color, color["rgb"])

        if distance < min_distance:
            min_distance = distance
            nearest_color = color
    
    return nearest_color

def GetColorByRGB(rgb:tuple):
    return find_nearest_color(rgb)

def GetSafeColor(rgb:tuple):
    return colors[int(rgb[0]*6/256)*36 + int(rgb[1]*6/256)*6 + int(rgb[2]*6/256)]