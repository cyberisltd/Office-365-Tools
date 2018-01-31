#!/usr/bin/python3
import csv, sys

filename = sys.argv[1]
users = {}

with open(filename, newline='') as f:
    reader = csv.DictReader(f)
    try:
        for row in reader:

            if row['Operations'] == 'UserLoggedIn':
                try:
                    user = row['UserIds']
                    country = row['Country']

                    if user in users:
                        if country in users[user]:
                            users[user][country] = users[user][country] + 1
                        else:
                            users[user][country] = 1
                    else:
                        users[user] = {}
                        users[user][country] = 1

                except KeyError:
                    pass 
        for user in users:
              if len(users[user]) > 1:
                   print("User: {} - {}".format(user,users[user]))


    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
