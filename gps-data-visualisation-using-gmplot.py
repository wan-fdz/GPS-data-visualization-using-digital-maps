""" gps-data-visualisation-using-gmplot.py

    Author: Vanessa Fernández
    Contact: vfernandezv6@gmail.com
    First created: 09/21/20
    Last updated: 09/25/20
"""

#Import standard libraries
import gmplot
import time
import numpy as np
import pandas as pd


def read_apikey(apikey_file):
    """
    Read the apikey from file.

    :param apikey_file: path and apikey file name
    :return: apikey: apikey required by gmplot
    """

    # open and read apikey from file
    with open(apikey_file, 'r') as f:
        apikey = f.readline()

    # return apikey
    return apikey


def read_gps_logger_data(gps_logger_file):
    """
    Read raw GPS data from file.
    :param gps_logger_file: path and filename of raw gps data file
    :return:
        lats: list with latitudes
        longs: list with longitudes
        alts: list with altitudes
    """
    # try to read the 'gps_logger_file'
    try:
        file_id = open(gps_logger_file,'r')

    # if an exception is raised
    except OSError:
        print("ERROR: file " + gps_logger_file + "couldn't be read")
        
        # close file object
        file_id.close()

        exit(-1)

    # otherwise
    else:
        # read gps logger file as pandas-type data frame
        df = pd.read_csv(gps_logger_file)

        # retrieve latitude, longitude and altitude
        lats = df["latitude"]
        longs = df["longitude"]
        alts = df["altitude(m)"]

        # close file object
        file_id.close()

    # return latitudes, longitudes, and altitudes
    return lats, longs, alts


def create_map_plotter(lats, longs, alts, apikey, zoom=10, map_type="roadmap"):
    """
    Creates the empty map in which the latitudes and longitudes will be plotted
    :param lats: list with latitudes
    :param longs: list with longitudes
    :param alts: list with altitudes
    :param apikey: apikey required by gmplot
    :param zoom: zoom resolution of the map
    :param map_type: types of maps you can display using the Maps JavaScript API (roadmap, satellite, hybrid and terrain)
    :return:
        gmap: Map object
    """
    lats_mean = np.mean(lats)
    longs_mean = np.mean(longs)
    alts_mean = np.mean(alts)

    # create the map plotter:
    gmap = gmplot.GoogleMapPlotter(lat=lats_mean, lng=longs_mean, zoom=zoom,
                                   map_type=map_type, apikey=apikey)
    return gmap


def add_points_to_map(gmap, lats, longs, alts):
    """
    Plots the latitudes and longitudes in the map
    :param gmap: Map object
    :param lats: list with latitudes
    :param longs: list with longitudes
    :param alts: list with altitudes
    :return:
        gmap: Map object with a plotted polyline
    """
    # add points to the map as a path
    gmap.plot(lats=lats, lngs=longs, edge_width=7, color='red')

    # return the updated map
    return gmap


def write_map(gmap, filename="map.html"+str(time.time())):
    """
    Draws the HTML map to a file
    :param gmap: Map object with a plotted polyline
    :param filename: name of file to write to
    :return:
       Nothing to return
    """

    # Draw the map:
    gmap.draw(file=filename)

    # nothing to return
    return None


def main():
    """
    This function calls the following functions in order to read the GPS data and visualize it using gmplot:
        read_apikey(apikey_file), 
        read_gps_logger_data(gps_logger_file), 
        create_map_plotter(lats, longs, alts, apikey, zoom=10, map_type="roadmap"),
        add_points_to_map(gmap, lats, longs, alts),
        and write_map(gmap, filename="map.html"+str(time.time()))
    :param:
        No parameters
    :return:
        Nothing to return
    """


    # read apikey
    # (make sure your APIKEY has been written in the apikey.txt file)
    apikey = read_apikey("apikey.txt")

    # read gps data
    gps_logger_file = "20200923-210519.txt" #file with the YYYYMMDD-HHMMSS.txt format
    lats, longs, alts = read_gps_logger_data(gps_logger_file=gps_logger_file)

    # create map plotter
    gmap = create_map_plotter(lats, longs, alts, apikey, zoom=18, map_type="roadmap")

    # add points to map
    gmap = add_points_to_map(gmap=gmap, lats=lats, longs=longs, alts=alts)

    # write html map
    write_map(gmap=gmap, filename="map-gmplot-"+str(time.time())+".html")

    # return None
    return None


# call main function
main()
