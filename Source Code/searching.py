from flask import Flask
import json
import data

def search_for( phrase, price_min, price_max ):
  results = []
  with open ('data/offers.json') as data_file:
    base = json.load(data_file)
  acc = data.get_number()
  for x in range( acc ):
    if (phrase in base['offers'][x]['title']) or (phrase in
    base['offers'][x]['desc']):
      results.append( x )
  return results


# A function that returns numbers of all offers published by a particular user.
def find_all_published( user ):
  results = []
  with open ('data/offers.json') as data_file:
    base = json.load(data_file)
  acc = data.get_number()
  for x in range( acc ):
    if (user in base['offers'][x]['seller']):
      results.append( x )
  return results

