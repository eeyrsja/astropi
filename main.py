# Main Python Script for JBVK Astro Pi Project
# --------------------------------------------
# JBVK:
#   Jack McKinnon
#   Ben Alexander
#   Victor Florek
#   Kieran Pennalls

# Hello from Balsall Common!

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
camera.resolution = (1296, 972)


def create_csv(data_file):
    """
    this function creates a new .csv file and puts the titles in.

    csv files done by Ben Alexander

    :param data_file: the name of the file to save the results in
    :return: True or false if it can make the new file
    """
    try:
        with open(data_file, 'w') as f:
            writer = csv.writer(f)
            header = ("Time", "Day_or_Night", "Latitude", "Longitude", "Cloud_Percent", "Photo_File")
            writer.writerow(header)
        return True
    except:
        #the file could not be made
        return False


def add_results_to_csv(data_file, time, day_or_night, latitude, longitude, cloud_percent, photo_file):
    """
    this function puts the data in a .csv file.
    
    csv files done by Ben Alexander

    :param data_file: the name of the file to save the results in
    :param time: the actual time when data collected
    :param day_or_night: is it daytime or night time?
    :param latitude: location of ISS
    :param longitude: location of ISS
    :param cloud_percent: our estimate of the cloud cover in the photo
    :param photo_file: link to the photo
    :return: True or false if it can add the result to the file
    """
    try:
        with open(data_file, 'a') as f:
            writer = csv.writer(f)
            result = (time, day_or_night, latitude, longitude, cloud_percent, photo_file)
            writer.writerow(result)
        return True
    except:
        # the data could not be added
        return False


def get_iss_position():
    """
    this function uses the ISS library to get the current latitude and longitude of the ISS in degrees

    :return: lat, long
    """
    location = ISS.coordinates()
    latitude = location.latitude.degrees
    longitude = location.longitude.degrees
    return latitude, longitude


def get_day_night():
    """
    this function uses the is_sunlit function to find out if it is day or night

    :return: day or night
    """
    t = timescale.now()
    if ISS.at(t).is_sunlit(ephemeris):
        return "day"
    else:
        return "night"


def get_cloud_percent(photo):
    # TODO - lots of work to do!
    return 20


# MAIN TASK
# ---------

# Set up the output file
create_csv(data_file)
counter =1

# Main program loop for just less than 3 hours (180 minutes)
while (now_time < start_time + timedelta(minutes=2)): #TODO change to 175 minutes
    # Take a photo and save it
    photo_file = base_folder/f'photo_{counter:04}.jpg'
    camera.start_preview()
    sleep(2) # Camera warm-up time
    camera.capture()

    # Get measurements
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
    day_or_night = get_day_night()
    iss_position = get_iss_position()
    cloud_percent = get_cloud_percent(photo_file)

    # Write the results to CSV file
    add_results_to_csv(data_file, current_datetime, day_or_night, iss_position[0], iss_position[1], cloud_percent, photo_file)

    # Log the event
    logger.info(f"main loop counter: {counter}")
    counter += 1
    sleep(6) # 1 minute sleep #TODO - check how long to sleep for

    # Update the current time and counter
    now_time = datetime.now()
    counter = counter + 1
