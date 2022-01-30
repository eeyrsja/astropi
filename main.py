# Main Program for JBVK Astro Pi Project
# Helpful information:
# https://projects.raspberrypi.org/en/projects/code-for-your-astro-pi-mission-space-lab-experiment/2

import csv
from pathlib import Path
from datetime import datetime, timedelta
from logzero import logger, logfile
from picamera import PiCamera
from orbit import ISS
from skyfield.api import load
from time import sleep

# Running time information
start_time = datetime.now()
now_time = datetime.now()
counter = 1

# Set up base folder and files
base_folder = Path(__file__).parent.resolve()
data_file = base_folder/'data.csv'
logfile(base_folder/"events.log")

# Parameters for ISS position finding
ephemeris = load('de421.bsp')
timescale = load.timescale()

# Set up the camera
camera = PiCamera()
camera.resolution = (1296,972)


def create_csv(data_file):
    """
    this function creates a new .csv file and puts the titles in.

    csv files done by Ben Alexander

    :param data_file:
    :return:
    """
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Time", "Latitude", "Longitude", "Cloud_Percent", "Closest_Town", "Photo_Link")
        writer.writerow(header)


# results


def add_results_to_csv(data_file, Time, Latitude, Longitude, Cloud_Percent, Closest_Town, Photo_Link)
    """
    this function puts the data in a .csv file.
    
    csv files done by Ben Alexander
    
    :param data_file: 
    :param Time: 
    :param Latitude: 
    :param Longitude: 
    :param Cloud_Percent: 
    :param Closest_Town: 
    :param Photo_Link: 
    :return: 
    """
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        header = (Time, Latitude, Longitude, Cloud_Percent, Closest_Town, Photo_Link)
        writer.writerow(header)


def get_iss_position():
    location = ISS.coordinates()
    latitude = location.latitude.degrees
    longitude = location.longitude.degrees
    return latitude, longitude


def get_day_night():
    t = timescale.now()
    if ISS.at(t).is_sunlit(ephemeris):
        return "day"
    else:
        return "night"


def get_nearby_town(latitude, longitude):
    # TODO Write this function!
    return("Balsall Common")


# Set up the output file
create_csv(data_file)

# Main program loop for 3 hours
while (now_time < start_time + timedelta(minutes=2)):

    # Get measurements
    iss_position = get_iss_position()
    day_night = get_day_night()
    nearby_town = get_nearby_town()

    # Write the results to CSV file
    row = (counter, datetime.now(), sense.temperature, sense.humidity) #TODO this is wrong!
    add_csv_data(data_file, row)

    # Log the event
    logger.info(f"main loop counter: {counter}")
    counter += 1
    sleep(60)

    # Update the current time
    now_time = datetime.now()
