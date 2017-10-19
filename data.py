import json

def get_number():
  with open('data/offers.json') as data_file0:
    data0 = json.load(data_file0)
  acc = 0
  for row in data0["offers"]:
    acc += 1
  return acc

def read_offer( number ):
  with open('data/offers.json') as data_file:
    data = json.load(data_file)
    offer = []
    attributes = ["desc", "endDate", "endPrice", "id", "seller", "startDate",
    "startPrice", "title"]
    for item in attributes:
      offer.append(data["offers"][number][item])
  return offer

def add_offer ( offer ):
  with open ('data/offers.json') as data_file:
    data = json.load(data_file)
    data['offers'].extend( [offer] )
  with open('data/offers.json', 'w') as outfile:
    json.dump(data, outfile, sort_keys=True)
  return;

# Should I use here any other HTTP request than POST or GET?
def delete_offer ( id ):
  with open ('data/offers.json') as data_file:
    data = json.load(data_file)
    for x in range (0, get_number()):
      if data['offers'][x]['id'] == id:
        data['offers'].pop(x)
  with open('data/offers.json', 'w') as outfile:
    json.dump(data, outfile, sort_keys=True)
  return;

