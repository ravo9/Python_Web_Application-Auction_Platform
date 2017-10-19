import json
import bcrypt
from flask import session, url_for, redirect

def get_number():
  with open('data/users.json') as data_file0:
    data0 = json.load(data_file0)
  acc = 0
  for row in data0["users"]:
    acc += 1
  return acc

def read_user( number ):
  with open('data/users.json') as data_file:
    users = json.load(data_file)
    user = []
    attributes = ["address", "code", "country", "email", "fname", "login",
    "password", "phone", "sname", "town"]
    for item in attributes:
      user.append(users["users"][number][item])
  return user

# gensalt() is an encrypting function, right?
def add_user ( user ):
  with open ('data/users.json') as data_file:
    users = json.load(data_file)
    # Password encrypting.
    user['password'] = bcrypt.hashpw(user['password'], bcrypt.gensalt())
    users['users'].extend( [user] )
  with open('data/users.json', 'w') as outfile:
    json.dump(users, outfile, sort_keys=True)
  return;

# Should I use a decorator structure if it seems to be simpler now?
# Should I add here redirection to the requested page after login?
def check_if_logged_in(f):
  status = session.get('logged_in', False)
  if status == True:
    return "ok"
  else:
    return "notok"

# There is sth I don't understand. Why in decoding function we need to use
# that 'encode' and why do we need to pass the password from db as the second
# argument?
# Why can't we just compare encoded db password with password entered by user,
# encoded exactly in the same way ( I have checked and it didn't work )???
def check_credentials ( login, password ):
  with open('data/users.json') as data_file:
    users = json.load(data_file)
  for row in users["users"]:
    if row['login'] == login:
      if row['password'] == bcrypt.hashpw(password.encode('utf-8'), row['password']):
        return 'true'
  return 'false'
