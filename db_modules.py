from tinydb import TinyDB, Query
from tinydb.operations import add, set

db = TinyDB('db.json')
User = Query()

def getBalance(user):
    user = db.search(User.username == str(user))[0]
    return user['balance']

def addBalance(user, val):
    first = db.search(User.username == str(user))[0]
    total = int(first['balance'])+int(val)
    db.update(set('balance', total ), User.username == str(user))
    return getBalance(user)

def subtractBalance(user,val):
    first = db.search(User.username == str(user))[0]
    total = int(first['balance'])-int(val)
    db.update(set('balance', total ), User.username == str(user))
    return getBalance(user)

def addUser(username, bal = 100):
    db.insert({
    'username': str(username), 
    'balance': bal
    })

def checkUser(username):
    if len(db.search(User.username == str(username)))>0:
      return True
    else:
      addUser(username)
      return False