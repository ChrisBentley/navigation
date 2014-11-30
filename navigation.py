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


def navigation(args):
    """
    Method for navigating a probe to the correct coordinates
    :param args: the arguments passed into the script by the user
    """

    # set local email variable to be the email specified by the user provided arguments
    email = args.email

    # check the email is a valid email address format
    if check_email(email) is False:
        print 'The email address you have entered is not valid. Please enter a valid email address'
        sys.exit(0)
    else:
        print 'The email address is valid'

    ship_movements = get_movements(email)

    print ship_movements


def get_movements(email):
    """
    Method to send a GET request to the space probe API and retrieve the spacecraft's movements
    :param email: email supplied by the user
    :return: movements: the movements of the spacescraft
    """
    movements = 'Failed to get movements!'

    url = BASE_URL + '/api/spaceprobe/getdata/' + email



    ##########
    # Built a quick test version that returns the same json response that the API should
    example_movements_file = '/Users/chris/projects/navigation/example_movements.json'
    if os.path.exists(example_movements_file):
        # Retrieve the movements from the json file
        with open(example_movements_file, "r") as open_file:
            movements = open_file.read()
    ##########

    return movements


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
    navigation(args)

    # debug message letting me know the script ended
    print '\nPROGRAM COMPLETE\n'


(__name__ == '__main__' and main())

