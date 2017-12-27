import json, os

# A function that returns all offers number.
def get_number():
  with open('data/offers.json') as data_file0:
    data0 = json.load(data_file0)
  acc = 0
  for row in data0["offers"]:
    acc += 1
  return acc


# A function that returns an offer of a given number.
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


# A function that moves a bought item from 'offers' to 'archive' json file.
def move_to_archive ( offer ):
  with open ('data/archive.json') as data_file:
    data = json.load(data_file)
    data['offers'].extend( [offer] )
  with open('data/archive.json', 'w') as outfile:
    json.dump(data, outfile, sort_keys=True) 
  return;


# A function removing an offer from 'offers' json file.
def delete_offer ( id ):
  with open ('data/offers.json') as data_file:
    data = json.load(data_file)
    for x in range (0, get_number()):
      if data['offers'][x]['id'] == id:
        data['offers'].pop(x)
        try:
          os.remove('static/uploads/'+id+'.png')
        except:
          pass
        break
  with open('data/offers.json', 'w') as outfile:
    json.dump(data, outfile, sort_keys=True)
  return;

