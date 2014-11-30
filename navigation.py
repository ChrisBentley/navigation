#!/Users/chris/projects/venv/bin/python

#  Program to find the x,y coordinates of a spaceship

import argparse
import re

parser = argparse.ArgumentParser(description='This is a script to navigate a probe to th location of a spaceship')
parser.add_argument('-e','--email', help='An email address to make GET requests with', required=True)
args = parser.parse_args()


def main(email=args.email):
    print email
    print '\nend of script\n'

if __name__ == "__main__":
    main()

