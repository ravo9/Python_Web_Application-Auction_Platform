import json

def get_number():
  with open('data/offers.json') as data_file:
    data = json.load(data_file)
  acc = 0
  for row in data["offers"]:
    acc += 1
  return acc

def read_last():
  with open('data/offers.json') as data_file:
    data = json.load(data_file)
    last_number = get_number() - 1
    last_offer = data["offers"][last_number]
  return last_offer

def read_offer( number ):
  with open('data/offers.json') as data_file:
    data = json.load(data_file)
    offer = data["offers"][number]
  return offer
