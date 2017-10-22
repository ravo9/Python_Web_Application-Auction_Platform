import json
import bcrypt
from flask import session, url_for, redirect

# A function returning a total number of users.
def get_number():
  with open('data/users.json') as data_file0:
    data0 = json.load(data_file0)
  acc = 0
  for row in data0["users"]:
    acc += 1
  return acc


# A function that returns a number of a user with given login.
def find_user( login ):
  with open('data/users.json') as data_file:
    users = json.load(data_file)
    acc = 0
    for user in users['users']:
      if user['login'] == login:
        return acc
      acc += 1
  return -1


# A function that returns a user of a given number.
def read_user( number ):
  with open('data/users.json') as data_file:
    users = json.load(data_file)
    user = []
    attributes = ["address", "code", "country", "email", "fname", "login",
    "password", "phone", "sname", "town"]
    for item in attributes:
      user.append(users["users"][number][item])
  return user


def add_user ( user ):
  with open ('data/users.json') as data_file:
    users = json.load(data_file)
    # Password encrypting.
    user['password'] = bcrypt.hashpw(user['password'], bcrypt.gensalt())
    users['users'].extend( [user] )
  with open('data/users.json', 'w') as outfile:
    json.dump(users, outfile, sort_keys=True)
  return;


# A function checking login credentials.
def check_credentials ( login, password ):
  with open('data/users.json') as data_file:
    users = json.load(data_file)
  for row in users["users"]:
    if row['login'] == login:
      if row['password'] == bcrypt.hashpw(password.encode('utf-8'), row['password']):
        return 'true'
  return 'false'
