#!/Users/chris/projects/venv/bin/python

# Program to find the x,y coordinates of a spacecraft
# Author: Chris Bentley

import argparse
import re
import sys
import os
import urllib2

# Global variable for the base url of the space probe API
BASE_URL = 'http://goserver.cloudapp.net:3000'


def navigation(email):
    """
    Method for navigating a probe to the correct coordinates
    :param email: the email address passed into the script by the user
    """

    # check the email provided is in a valid email address format and stop the script if it's invalid
    if check_email(email) is False:
        print '\nThe email address you have entered is not valid. Please enter a valid email address\n'
        sys.exit(0)

    # Call the get_movements method to retrieve the spacecraft's movements
    spacecraft_movements = __get_movements(email)

    # stop the script here if for any reason the movements could not be retrieved
    if not spacecraft_movements:
        print "\nThe spacecraft's movements could not be retrieved, the script must end."
        sys.exit(0)

    # debug message to print the ships movements
    print "\nThe spacecraft's movements are:"
    print spacecraft_movements


def __get_movements(email):
    """
    Method to send a GET request to the space probe API and retrieve the spacecraft's movements
    :param email: email supplied by the user
    :return: movements: the movements of the spacecraft
    """
    movements = ''

    # creates the full url to get data from
    getdata_url = BASE_URL + '/api/spaceprobe/getdata/' + email

    print "Retrieving spacecraft movements from the API..."
#    try:
#        movements = urllib2.urlopen(getdata_url).read()
#    except IOError:
#        print 'A connection to the server could not be made'
#        raise
#    except Exception as e:
#        print "An unforeseen problem occurred while retrieving the spacecraft's movements"
#        raise

    # Built a quick test version that returns the same json response that the API should
    # so that i didn't have to query the API every time I ran the script
    example_movements_file = '/Users/chris/projects/navigation/example_movements.json'
    if os.path.exists(example_movements_file):
        # Retrieve the movements from the json file
        with open(example_movements_file, "r") as open_file:
            movements = open_file.read()

    return movements


def __send_coordinates(email, x, y):
    """
    Method to send a GET request to the space probe API with the final coordinates and receive a response
    :param email: the email address to send the coordinates with
    :param x: the x coordinate to send
    :param y: the y coordinate to send
    :return: response: the response of the probe API
    """

    # creates the full url to submit data to
    submitdata_url = BASE_URL + '/spaceprobe/submitdata/' + email + '/' + x + '/' + y

    print "Submitting the final coordinates to the space probe API..."
    try:
        response = urllib2.urlopen(submitdata_url).read()
    except IOError:
        print 'A connection to the server could not be made'
        raise
    except Exception as e:
        print "An unforeseen problem occurred while sending the coordinates"
        raise

    return response


def check_email(email):
    """
    Method to check that an email is valid e.g. john@example.com
    :param email: the email supplied by the user
    :return: True if the regex matches and False if it does not
    """

    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True

    return False


def main():

    def __init__():
        parser = argparse.ArgumentParser(description='This is a script to navigate a '
                                                     'probe to the location of a spaceship')
        parser.add_argument('-e','--email', help='An email address to make GET requests with', required=True)
        return parser.parse_args()

    # calls the initialisation function of main to read the command line arguments
    args = __init__()

    # calls the navigation functionality while passing in the command line arguments
    navigation(args.email)

    # debug message letting me know the script has reached the end
    print '\nSCRIPT COMPLETED\n'


(__name__ == '__main__' and main())

