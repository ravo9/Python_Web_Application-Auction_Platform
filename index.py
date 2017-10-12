from flask import Flask, render_template, url_for

import data

app = Flask(__name__)

@app.route("/")
def index():
  acc = data.get_number()
  offer1 = data.read_offer(acc - 1)
  offer2 = data.read_offer(acc - 2)
  offer3 = data.read_offer(56)
  return render_template('index.html', offer1 = offer1, offer3 = offer3)

@app.route("/sell", methods=['POST', 'GET'])
def sell():
  if request.method == 'POST':
    return render_template('sell.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

