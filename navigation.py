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
    :return: True if the probe has been successfully launched, False if the probe didn't reach it's target
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

    # create a dictionary object from the returned movements
    movements_dict = eval(spacecraft_movements)

    if movements_dict["Directions"][0] == 'FORWARD':
        # if the first direction is a forward then we know the spacecraft started in one of three starting positions
        # and for each potential starting position we then know the corresponding direction the craft is facing
        print "\nThe spacecraft moved forward for it's first direction, we can attempt to find it's position " \
              "by using one of three potential starting positions"
        known_starts = {"1": ["0", "0", "N"],
                        "2": ["1", "1", "W"],
                        "3": ["0", "2", "S"]
                        }
    else:
        # if the first direction is not forward then it is a left or a right. We know the starting position of the
        # spacecraft, but not which direction it was originally facing
        print "\nThe spacecraft turned 90 degrees for it's first direction, we can attempt to find it's position " \
              "by using one of four potential starting directions"
        known_starts = {"1": ["0", "1", "N"],
                        "2": ["0", "1", "E"],
                        "3": ["0", "1", "S"],
                        "4": ["0", "1", "W"],
                        }

    # try each of the potential starting positions to see if it produces a valid output
    # after all the movements have been made
    attempt = 1
    for i in known_starts:

        x = known_starts[i][0]
        y = known_starts[i][1]
        d = known_starts[i][2]

        print "\nattempt", attempt, "will start with: x = " + x + " y = " + y + " direction = " + d

        # call the tracking method to find the final location of the spacecraft
        final_spacecraft_location = __track_spacecraft(movements_dict, x, y, d)

        # if the tracking method returned a valid location then attempt to send this to the server,
        # otherwise try the next starting locations
        if final_spacecraft_location:
            x = final_spacecraft_location[0]
            y = final_spacecraft_location[1]
            print "tracked spacecraft location is: x = " + x + " y = " + y

            print "sending location to server..."
            api_response = __send_coordinates(email, x, y)

            print api_response

            return True
        else:
            print "This starting position was definitely not correct as it caused the spacecraft to go outside " \
                  "of the known universe, trying the next starting position..."

        attempt += 1

    return False


def __track_spacecraft(movements_dict, x, y, d):
    """
    Method to follow a set of given movements and track the final location of the spacecraft
    :param movements_dict: the list of movements that the spacecraft has taken
    :param x: the starting x coordinate
    :param y: the starting y coordinate
    :param d: the starting direction
    :return: final x and y coordinates of the spacecraft
    """
    # enumerate through the list of movements
    for movement in movements_dict["Directions"]:
        if movement == "FORWARD":
            x, y = __direction_forward(x, y, d)
            print "FORWARD action taken"

        if movement == "LEFT":
            d = __direction_left(d)
            print "LEFT action taken"

        if movement == "RIGHT":
            d = __direction_right(d)
            print "RIGHT action taken"

        print x, y

        # check that the spacecraft position is still within the known universe i.e. the last action hasn't
        # meant that this potential starting position is definitely wrong
        if int(x) > 9 or int(y) > 9 or int(x) < 0 or int(y) < 0:
            return ''

    return [x, y]


def __direction_forward(x, y, d):
    """
    Method for advancing the spacecraft forward one unit
    :param x: x coordinate
    :param y: y coordinate
    :param d: direction that spacecraft is currently facing
    :return: updated x & y coordinates
    """
    x = int(x)
    y = int(y)

    if d == 'N':
        y += 1
    if d == 'S':
        y -= 1
    if d == 'E':
        x += 1
    if d == 'W':
        x -= 1

    return str(x), str(y)


def __direction_right(d):
    """
    Method for turning the spacecraft 90 degrees to the right
    :param d: the current direction of the spacecraft
    :return: the updated direction of the spacecraft
    """
    if d == 'N':
        d = 'E'
    elif d == 'S':
        d = 'W'
    elif d == 'E':
        d = 'S'
    elif d == 'W':
        d = 'N'

    return d


def __direction_left(d):
    """
    Method for turning the spacecraft 90 degrees to the left
    :param d: the current direction of the spacecraft
    :return: the updated direction of the spacecraft
    """
    if d == 'N':
        d = 'W'
    elif d == 'S':
        d = 'E'
    elif d == 'E':
        d = 'N'
    elif d == 'W':
        d = 'S'

    return d


def __get_movements(email):
    """
    Method to send a GET request to the space probe API and retrieve the spacecraft's movements
    :param email: email supplied by the user
    :return: movements: the movements of the spacecraft
    """
    movements = ''

    # creates the full url to get data from
    getdata_url = BASE_URL + '/api/spaceprobe/getdata/' + email

    print "\nRetrieving spacecraft movements from the API..."
    try:
        movements = urllib2.urlopen(getdata_url).read()
    except IOError:
        print 'A connection to the server could not be made'
        raise
    except Exception as e:
        print "An unforeseen problem occurred while retrieving the spacecraft's movements"
        raise

#    # Built a quick test version that returns the same json response that the API should
#    # so that i didn't have to query the API every time I ran the script
#    example_movements_file = '/Users/chris/projects/navigation/real_movements.json'
#    if os.path.exists(example_movements_file):
#        # Retrieve the movements from the json file
#        with open(example_movements_file, "r") as open_file:
#            movements = open_file.read()

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

    print submitdata_url

#    response = 'this is a test_response from __send_coordinates'

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
    success = navigation(args.email)

    # print the final outcome of the script
    if success:
        print '\nSCRIPT COMPLETED SUCCESSFULLY\n'
    else:
        print "\nSCRIPT FAILED - YOU SUCK CHRIS!\n"


(__name__ == '__main__' and main())

