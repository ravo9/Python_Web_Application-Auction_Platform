from flask import Flask, render_template, url_for, request, redirect, session
import data
import searching
import users
import bcrypt
from functools import wraps
from datetime import datetime

app = Flask(__name__)
# How should I secure that key?
app.secret_key = 'abc'

@app.route("/")
@app.route("/page/<num>")
def index(num=1):
  last_index = data.get_number() - 1
  if last_index == -1:
    return "There are no offers yet :( "

  fresh_offers = []

  # Page number
  num = int(num)
  i = (num * 10) - 10
  
  for x in range(i, i+10):
    try:
      if (last_index-x) >= 0:
        fresh_offers.append( data.read_offer(last_index-x) )
    except:
      print "reading error"

  # Page number has to be incremented, because the button "next page" needs this
  # number.
  num +=1

  # A flag indicating that there are no more elements and there's no need to
  # implement "next page" button anymore.
  last_page = 0
  if fresh_offers[-1] == data.read_offer(0):
    last_page = 1
  
  # A variable telling the html file if the user is logged in or not (needed
  # to display a correct version of the nav toolbar.
  status = session.get('logged_in', False)

  return render_template('index.html', fresh_offers = fresh_offers, num = num,
  last_page = last_page, status=status)

# Doesn't work.
def check_if_logged_in(f):
  status = session.get('logged_in', False)
  if status == True:
    return "ok"
  else:
    return "notok"

# Works but I don't get it.
# 1. Why does it have such recursive structure. 
# 2. What about the arguments.
# 3. What the wraps means?
# ---
# Should I add here a redirection to the requested page after login?
# Why the first version doesn't work?
def check_if_logged(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    status = session.get('logged_in', False)
    if status == True:
      return f(*args, **kwargs)
    else:
      return redirect('/login')
  return decorated

@app.route("/sell", methods=['POST', 'GET'])
@check_if_logged
def sell():
  if request.method == 'POST':
    id = "AXN000"+str(data.get_number()+1)
    title = request.form['title']
    desc = request.form['desc']
    startDate = datetime.now().strftime("%d.%m.%Y %H:%M")
    endDate = request.form['endDate']
    startPrice = request.form['startPrice']
    endPrice = request.form['endPrice']
    seller = session['user']
    photo = request.files['photo']
    photo.save('static/uploads/'+id+'.png')  
    offer = {'id': id, 'title': title, 'desc': desc, 'startDate': startDate,
    'endDate': endDate, 'startPrice':startPrice, 'endPrice':endPrice,
    'seller': seller}
    data.add_offer( offer )
    return redirect('/published')

  else:
    # A variable telling the html file if the user is logged in or not (needed
    # to display a correct version of the nav toolbar.
    status = session.get('logged_in', False)

    return render_template('sell.html', status=status)

@app.route("/published")
def published():
  return render_template('published.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    login = request.form['login']
    password = request.form['password']
    result = users.check_credentials( login, password )
    if result == 'true':
      session['logged_in'] = True
      session['user'] = login
      return redirect('/')
    else:
      return render_template('login.html')
  else:
    return render_template('login.html')

@app.route("/logout")
def log_out():
  session['logged_in'] = False
  session['user'] = ""
  return render_template('logout.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
  if request.method == 'POST':
    login = request.form['login']
    password = request.form['password']
    email = request.form['email']
    fname = request.form['fname']
    sname = request.form['sname']
    phone = request.form['phone']
    address = request.form['address']
    town = request.form['town']
    code = request.form['code']
    country = request.form['country']
    user = {'address': address, 'code': code, 'country': country, 'email':
    email, 'fname': fname, 'login': login, 'password': password, 'phone':
    phone, 'sname': sname, 'town': town}
    users.add_user( user )
    session['logged_in'] = True
    session['user'] = login
    return redirect('/')
  else:
    return render_template('register.html')

@app.route("/account", methods=['POST', 'GET'])
@check_if_logged
def account():
  if request.method == 'POST':
    return redirect('/')
  else:
    # User has to be read here to supply proper user data to be displayed.
    user_id = users.find_user( session['user'] )
    user = users.read_user ( user_id )

    # Here I am looking for offers that this particular user has published.
    published_offers_numbers = searching.find_all_published( session['user'] )
    published_offers = []

    for x in published_offers_numbers:
      try:
        published_offers.append( data.read_offer( x  ))
      except:
        print x

    return render_template('account.html', user=user,
    published_offers=published_offers)

@app.route("/search", methods=['POST', 'GET'])
def search():
  if request.method == 'POST':
    phrase = request.form['phrase']
    price_min = request.form['price_min']
    price_max = request.form['price_max']
    results_numbers = searching.search_for( phrase, price_min, price_max )
    results = []

    for x in results_numbers:
      try:
        results.append( data.read_offer( x  )  )
      except:
        print "reading error"
        
    # A variable telling the html file if the user is logged in or not (needed
    # to display a correct version of the nav toolbar.
    status = session.get('logged_in', False)

    return render_template('results.html', results = results, status=status)

  else:

    # A variable telling the html file if the user is logged in or not (needed
    # to display a correct version of the nav toolbar.
    status = session.get('logged_in', False)

    return render_template('search.html', status=status)

# Should I use any other command than POST, GET here?
@app.route("/buy/<id>")
def buy(id=None):
  data.delete_offer(id)
  return redirect("/")

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

