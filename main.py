# Main Program for JBVK Astro Pi Project
# Helpful information:
# https://projects.raspberrypi.org/en/projects/code-for-your-astro-pi-mission-space-lab-experiment/2

import csv
from pathlib import Path
from datetime import datetime, timedelta
from logzero import logger, logfile
#from picamera import PiCamera
#from orbit import ISS
#from skyfield.api import load
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
#ephemeris = load('de421.bsp') TODO - uncomment to run on astropi
#timescale = load.timescale() TODO - uncomment to run on astropi

# Set up the camera
#camera = PiCamera() TODO - uncomment to run on astropi
#camera.resolution = (1296,972) TODO - uncomment to run on astropi


def create_csv(data_file):
    """
    this function creates a new .csv file and puts the titles in.

    csv files done by Ben Alexander

    :param data_file:
    :return:
    """
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Time", "Day_or_Night", "Latitude", "Longitude", "Cloud_Percent", "Photo_Link")
        writer.writerow(header)


# results


def add_results_to_csv(data_file, Time, Day_or_Night, Latitude, Longitude, Cloud_Percent, Photo_Link):
    """
    this function puts the data in a .csv file.
    
    csv files done by Ben Alexander

    :param data_file:
    :param Time:
    :param Day_or_Night:
    :param Latitude: 
    :param Longitude: 
    :param Cloud_Percent:
    :param Photo_Link: 
    :return: 
    """
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        result = (Time, Day_or_Night, Latitude, Longitude, Cloud_Percent, Photo_Link)
        writer.writerow(result)


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


def get_cloud_percent(photo):
    # TODO - lots of work to do!
    return 20


# Set up the output file
create_csv(data_file)
counter =1

# Main program loop for 3 hours
while (now_time < start_time + timedelta(minutes=2)): #TODO change to 175 minutes
    # Take a photo and save it
    camera.start_preview()
    sleep(2) # Camera warm-up time
    camera.capture(f"{base_folder}/pic_{counter:04}.jpg")
    # Get measurements
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    day_or_night = get_day_night()
    iss_position = get_iss_position()
    cloud_percent = get_cloud_percent(f"{base_folder}/pic_{counter:04}.jpg")

    # Write the results to CSV file
    add_results_to_csv(data_file, current_datetime, day_or_night, iss_position[0], iss_position[1], cloud_percent,"PHOTO1.JPG")

    # Log the event
    logger.info(f"main loop counter: {counter}")
    counter += 1
    sleep(6) # 1 minute sleep #TODO - check how long to sleep for

    # Update the current time and counter
    now_time = datetime.now()
    counter = counter + 1
