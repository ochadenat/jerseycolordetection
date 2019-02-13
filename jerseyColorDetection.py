import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import webcolors as wb
import pandas as pd
import os
import time
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns; sns.set()  # for plot styling

FILE_OUTPUT = "C:/Users/ochad/PycharmProjects/JerseyColorDetection/jerseys-color-subsidesports.csv"
JERSEYS_DIR = "C:/Users/ochad/PycharmProjects/JerseyCrawl/subsidesport_jpg_260x260"
NUM_CLUSTERS = 5

# retrieve the filenames (Full path) from a directory
def get_filename(path_with_files, fullpath=False):
    list_filename = os.listdir(path_with_files)
    if fullpath == True:
        list_filename_fullpath = []
        for filename in list_filename:
            filename_fullpath = path_with_files + "/" + filename
            list_filename_fullpath.append(filename_fullpath)
            list_filename = list_filename_fullpath
    return list_filename

# return (red, green, blue) for the color given as #rrggbb
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# return color as #rrggbb for the given color values
def rgb_to_hex(red, green, blue):
    return '#%02x%02x%02x' % (red, green, blue)

# https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in wb.css3_hex_to_names.items():
        r_c, g_c, b_c = wb.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = wb.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def get_colour_name_css2(requested_colour):
    try:
        closest_name = actual_name = wb.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour_css2(requested_colour)
        actual_name = None
    return actual_name, closest_name

def closest_colour_css2(requested_colour):
    min_colours = {}
    for key, name in wb.css2_hex_to_names.items():
        r_c, g_c, b_c = wb.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) * 2
        gd = (g_c - requested_colour[1]) * 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_main_color(image_filename):
    im = Image.open(image_filename)
    # Use the center to avoid taking the white background
    ar = np.asarray(im.crop((50, 50, 210, 210)))
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # Finding clusters
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # print ('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes) # assign codes
    counts, bins = scipy.histogram(vecs, len(codes)) # count occurrences

    index_max = scipy.argmax(counts) # find most frequent
    peak = codes[index_max]

    r = int(peak[0])
    g = int(peak[1])
    b = int(peak[2])

    rgb_color = (r, g, b)
    hex_color = rgb_to_hex(r, g, b)

    actual_name, closest_name = get_colour_name(rgb_color)

    closest_name_rgb = wb.name_to_rgb(closest_name)

    closet_name_r = closest_name_rgb[0]
    closet_name_g = closest_name_rgb[1]
    closet_name_b = closest_name_rgb[2]

    return rgb_color, r, g, b, hex_color, actual_name, closest_name, closet_name_r, closet_name_g, closet_name_b


def retrieve_colors():
    start_time = time.perf_counter()

    # delete the output file
    if os.path.exists(FILE_OUTPUT):
        os.remove(FILE_OUTPUT)

    df_images = pd.DataFrame(columns=['image_to_process', 'rgb_color', 'r', 'g', 'b', 'hex_color',
                                      'actual_name', 'closest_name', 'closet_name_r', 'closet_name_g', 'closet_name_b'])

    images_to_process = get_filename(JERSEYS_DIR, True)
    print(len(images_to_process), " images to process")
    i = 0
    for image_to_process in images_to_process:
        try:
            rgb_color, r, g, b, hex_color, actual_name, closest_name, closet_name_r, closet_name_g, closet_name_b = get_main_color(
                image_to_process)
            df_images.loc[
                i] = image_to_process, rgb_color, r, g, b, hex_color, actual_name, closest_name, closet_name_r, closet_name_g, closet_name_b
            # print ('image',i+1, 'processed:',image_to_process)
            i = i + 1
        except:
            print('image', i + 1, 'ERROR:', image_to_process)

    print(df_images.head(20))
    # output is a csv file with Image Caption, RGB, Hexa and CSS color
    df_images.to_csv(FILE_OUTPUT, sep=';', index=False)

    end_time = time.perf_counter()
    print("Program executed in {:,.2f} s".format(end_time - start_time))


def cluster_colors():
    df_colors = pd.read_csv(FILE_OUTPUT, sep=';',usecols  =['rgb_color', 'r', 'g', 'b'])
    print(list(df_colors))
    print(df_colors.shape[0])
    #remove dupplicate
    df_colors.drop_duplicates(inplace=True)
    print(df_colors.shape[0])
    X = df_colors[['r', 'g', 'b']].values


    kmeans = KMeans(n_clusters=16, random_state=0).fit(X)
    y_kmeans = kmeans.predict(X)
    centers = kmeans.cluster_centers_
    print(centers)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=X/255.0, s=20, edgecolors='none')
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], c=centers/255, s=200, alpha=0.5, edgecolors='black',
               label="test")
    # label = " ".join(centers[:, :]))
    plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=8, bbox_to_anchor=(0, 0))

    plt.show()


def main():
    # retrieve_colors()
    cluster_colors()

main()