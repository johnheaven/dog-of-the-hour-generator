import time
import requests
import random
import csv
import sys
import os

# get dognames from env var, otherwise set default
dogs = os.environ.get('DOGNAMES', 'Sniff,Juci,Eddie,Cosmo').split(',')
csv_path = os.environ.get('CSV_PATH', '.').rstrip('/') + '/dogofthehour.csv'

query = {'num': 1, 'min': 0, 'max': len(dogs) - 1, 'col': 1, 'base': 10, 'format': 'plain', 'rnd': 'new'}

# Get a random number from random.org API
API_attempts = 0
http_response = 503

# Records whether we got a "truly random" number from the API ("no" means it's taken from the Python pseudo-random generator)
truly_random = 'no'

# Try 5 times to get a random number from random.org and if it doesn't work,
# then get a random number using Python's pseudo-random number generator
# but log the fact that it wasn't truly random.
while http_response == 503:
    dog_number_request = requests.get(url='https://www.random.org/integers/', params=query, timeout=2)
    http_response = dog_number_request.status_code
    print ('HTTP response: ', http_response)
    # 200 means success
    if http_response == 200:
        truly_random = 'yes'
        dog_number = int(dog_number_request.text.strip())

    # give up if we required more than 4 attempts to get a random number
    if API_attempts > 4:
        random.seed()
        dog_number = random.randrange(len(dogs))
        break
    API_attempts += 1
    time.sleep(2)

# Get the dog's name from the dictionary
dogname = dogs[dog_number]

# Get a timestamp
dateandtime = time.localtime()

# Put values into a dictionary
doth_latest = {}
doth_latest['Date'] = time.strftime('%Y%m%d',dateandtime)
doth_latest['Hour'] = time.strftime('%H', dateandtime)
doth_latest['Timezone'] = time.strftime('%Z', dateandtime)
doth_latest['dogname'] = dogname
doth_latest['truly_random'] = truly_random

# Add to a CSV file.

# If parameter exists - create a new file to record values. Otherwise, append to existing.
mode, newfile = ('w', True) if "--new-file" in sys.argv else ('a', False)

with open(csv_path, mode, newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(doth_latest))
    if newfile:
        writer.writeheader()
    writer.writerow(doth_latest)
