import json

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

def add_user ( user ):
  with open ('data/users.json') as data_file:
    users = json.load(data_file)
    users['users'].extend( [user] )
  with open('data/users.json', 'w') as outfile:
    json.dump(users, outfile, sort_keys=True)
  return;

def check_credentials ( login, password ):
  with open('data/users.json') as data_file:
    users = json.load(data_file)
  for row in users["users"]:
    if row['login'] == login:
      if row['password'] == password:
        return 'true'
  return 'false'
