from flask import Flask, render_template, url_for, request
import data
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
  last_index = data.get_number() - 1
  fresh_offers = []

  for x in range(10):
    try:
      if (last_index-x) >= 0:
        fresh_offers.append( data.read_offer(last_index-x) )
    except:
      print "reading error"

  return render_template('index.html', fresh_offers = fresh_offers)

@app.route("/sell", methods=['POST', 'GET'])
def sell():
  if request.method == 'POST':
    id = "AXN000"+str(data.get_number()+1)
    title = request.form['title']
    desc = request.form['desc']
    startDate = datetime.now().strftime("%d.%m.%Y %H:%M")
    endDate = request.form['endDate']
    startPrice = request.form['startPrice']
    endPrice = request.form['endPrice']
    seller = "Sylvester Omsky"
    photo = request.files['photo']
    photo.save('static/uploads/'+id+'.png')
    offer = {'id': id, 'title': title, 'desc': desc, 'startDate': startDate,
    'endDate': endDate, 'startPrice':startPrice, 'endPrice':endPrice,
    'seller':seller}
    data.add_offer( offer )
    return "Done"
  else:
    return render_template('sell.html')

@app.route("/search", methods=['POST', 'GET'])
def search():
  if request.method =='POST':
    print "ok"
  else:
    return render_template('search.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

