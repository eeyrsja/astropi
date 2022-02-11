# Main Python Script for JBVK Astro Pi Project
# --------------------------------------------
# JBVK are:
#   Jack McKinnon
#   Ben Alexander
#   Victor Florek
#   Kieran Pennalls

# Hello from Balsall Common and Coventry!


# Import libraries - ** only astropi libraries allowed! **
import csv
from pathlib import Path
from datetime import datetime, timedelta
from logzero import logger, logfile
from picamera import PiCamera
from orbit import ISS
from skyfield.api import load
import reverse_geocoder
from time import sleep
from numpy import array, percentile, clip
from PIL import Image

# Set up base folder and files
base_folder = Path(__file__).parent.resolve()
data_file = base_folder/'data.csv'
logfile(base_folder/"events.log")
logger.info(f"Base folder: {base_folder}")

# Run time information
start_time = datetime.now()
now_time = datetime.now()
counter = 1
logger.info(f"Started running: {start_time}")

# Parameters for ISS position finding
ephemeris = load('de421.bsp')
timescale = load.timescale()

# Set up the camera
camera = PiCamera()
camera.resolution = (1440, 1080)


def create_csv(data_file):
    """
    this function creates a new .csv file and puts the titles in.

    csv files done by Ben Alexander

    :param data_file: the name of the file to save the results in
    :return: True or false if it can make the new file
    """
    logger.info(f"Function: create_csv")
    try:
        with open(data_file, 'w') as f:
            writer = csv.writer(f)
            header = ("Time", "Day_or_Night", "Latitude", "Longitude", "Nearest City", "Cloud_Percent", "Photo_File")
            writer.writerow(header)
        return True
    except:
        logger.error(f"Could not make a new CSV")
        return False


def add_results_to_csv(data_file, time, day_or_night, latitude, longitude, nearest_city, cloud_percent, photo_file):
    """
    this function puts the data in a .csv file.
    
    csv files done by Ben Alexander

    :param data_file: the name of the file to save the results in
    :param time: the actual time when data collected
    :param day_or_night: is it daytime or night time?
    :param latitude: location of ISS
    :param longitude: location of ISS
    :param nearest_city: closest city to the ISS now
    :param cloud_percent: our estimate of the cloud cover in the photo
    :param photo_file: link to the photo
    :return: True or false if it can add the result to the file
    """
    logger.info(f"Function: add_results_to_csv")
    try:
        with open(data_file, 'a') as f:
            writer = csv.writer(f)
            result = (time, day_or_night, latitude, longitude, nearest_city, cloud_percent, photo_file)
            writer.writerow(result)
        return True
    except:
        logger.error(f"Could not add data to CSV")
        return False


def get_iss_position():
    """
    this function uses the ISS library to get the current latitude and longitude of the ISS in degrees

    :return: lat, long
    """
    logger.info(f"Function: get_iss_position")
    location = ISS.coordinates()
    latitude = location.latitude.degrees
    longitude = location.longitude.degrees
    return latitude, longitude


def get_nearest_city(latlong):
    """
    this function finds out the closest city to the ISS.

    Sometimes when over the ocean we found out the ISS can be a long way from the city though!
    :param latlong: latitude and longitude of ISS
    :return: the name of the closest city
    """
    logger.info(f"Function: get_nearest_city")
    location = reverse_geocoder.search((latlong[0], latlong[1]))
    return(f"{location['name']} : {location['admin1']} : {location['admin2']}")


def get_day_night():
    """
    this function uses the is_sunlit function to find out if it is day or night

    :return: day or night
    """
    logger.info(f"Function: get_day_night")
    t = timescale.now()
    if ISS.at(t).is_sunlit(ephemeris):
        return "day"
    else:
        return "night"


def get_cloud_percent(photo):
    """
    This function opens a photo and tries to estimate how much of the picture is covered by cloud.

    :param photo: the filename of the photo
    :return: the percentage of cloud cover in the photo
    """
    logger.info(f"Function: get_cloud_percent")

    #open the image
    image = Image.open(photo)

    # rotate the picture - we think it is upside down?!
    image = image.rotate(180)

    # Crop the photo to remove the window frame
    width = image.size[0]
    height = image.size[1]
    image = image.crop((width * 0.15, height * 0.15, width * 0.85, height * 0.85))

    # Convert from R,G,B colour to H,S,V
    # WWe want to find clouds which have low "S"aturation and high "V"alue (or brightness)
    image_hsv = array(image.convert("HSV"))

    # Get the Saturation and Brightness parts
    saturation = image_hsv[:,:,1] / 255  # saturation is how colourful the pixel is - clouds are not colourful so saturation is low
    brightness = image_hsv[:, :, 2] / 255 # brightness of clouds is high

    # Increase the photo contrast - make the whites whiter and the blacks blacker
    # this is copied from https://stackoverflow.com/questions/48406578/adjusting-contrast-of-image-purely-with-numpy
    minval = percentile(brightness, 5)
    maxval = percentile(brightness, 95)
    brightness = clip(brightness, minval, maxval)
    brightness = ((brightness - minval) / (maxval - minval))

    # Apply threshold - if the number is less than saturation threshold AND more than brightness threshold then we treat it as cloud
    clouds = (saturation < 0.3) & (brightness > 0.5)

    # Work out the percentage cloud cover by adding up all the cloud pixels and dividing by total pixels
    cloud_pixel_count = clouds.sum()
    total_pixel_count = clouds.size
    cloud_percent = 100.0 * cloud_pixel_count / total_pixel_count

    return cloud_percent


# MAIN LOOP
# ---------

# Set up the output file
create_csv(data_file)
counter = 1

# Main program loop for just less than 3 hours (180 minutes)
while (now_time < start_time + timedelta(minutes=2)):  #TODO change to 175 minutes
    logger.info(f"Main loop counter: {counter}")
    try:
        # Take a photo and save it
        photo_file = str(base_folder/f'photo_{counter:04}.jpg')
        camera.start_preview(alpha=128)  # Semi-see-through
        sleep(2)  # Camera warm-up time
        camera.capture(photo_file)
        camera.stop_preview()

        # Get measurements
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        day_or_night = get_day_night()
        iss_position = get_iss_position()
        nearest_city = get_nearest_city(iss_position)
        cloud_percent = get_cloud_percent(photo_file)

        # Write the results to CSV file
        add_results_to_csv(data_file, current_datetime, day_or_night, iss_position[0], iss_position[1], nearest_city, cloud_percent, photo_file)

        # Log the event
        sleep(6)  # 1 minute sleep  #TODO - check how long to sleep for

        # Update the current time and counter
        now_time = datetime.now()
        counter = counter + 1
    except:
        logger.error(f"Error in loop: {counter}")
