# authors: cedric, marco

import random
from db_modules import *


cardDict = {
  1 : "A",
  2 : "2",
  3 : "3",
  4 : "4",
  5 : "5",
  6 : "6",
  7 : "7",
  8 : "8",
  9 : "9",
  10 : "10",
  11 : "J",
  12 : "Q",
  13 : "K",
}

totalDict = {
  "A" : 11,
  "2" : 2,
  "3" : 3,
  "4" : 4,
  "5" : 5,
  "6" : 6,
  "7" : 7,
  "8" : 8,
  "9" : 9,
  "10" : 10,
  "J" : 10,
  "Q" : 10,
  "K" : 10,
}

suitDict = {
  1 : "\u2667", #clubs
  2 : "\u2664", #spades
  3 : "\u2661", #heart
  4 : "\u2662", #diamond
}

# ------------ CLASSES -------------


class Card:
  def __init__(self, num, suit):
    self.number = cardDict[num]
    self.suit = suitDict[suit]

  def __repr__(self):
    return str(self.number)+str(self.suit)


class Player:
  def __init__(self, cardList):
    self.cards = cardList

  def generateTotal(self):
    self.total = 0
    for card in self.cards:
      if card.number == "A":
        self.total += 11
      
      else:
        self.total += totalDict[card.number]

    if self.total > 21:
      self.total = 0
      for card in self.cards:
        if card.number == "A":
          self.total += 1
        
        else:
          self.total += totalDict[card.number]

    return self.total

  # def checkSplit(self):
  #   return totalDict[self.cards[0].number] == totalDict[self.cards[1].number]

# --------- FUNCTIONS ------------


def generateCard():
  return Card(random.randint(1,13),random.randint(1,4))

def generateHand(size = 1):
  Hand = []
  while len(Hand) < size:
    Hand.append(generateCard())
  return Hand

def playerHit(player):
  player.cards.append(generateCard())

 # def playerSplit():

def checkWin(player,dealer):
  if player.generateTotal() > 21:
    return 2

  while dealer.generateTotal() < player.generateTotal():
    dealer.cards.append(generateCard())
    print("Dealer's Hand: "+str(dealer.cards).strip("[]"))
    print("Dealer's Total: "+str(dealer.generateTotal()))
  
  if dealer.generateTotal() == player.generateTotal():
    return 3
  elif dealer.generateTotal() > player.generateTotal():
      if dealer.generateTotal()> 21:
        return 1
      else:
        return 2

def checkPlayerBj(player):
  if player.generateTotal() == 21:
    return True
  else:
    return False

# --------------- MAIN ------------------

def main():

  user = input ("Hi who are you ").lower()
  print ("You currently have " + str(getBalance(user)))

  bet = int(input ("How much do you bet "))
  subtractBalance(user, bet)
  print ("Your bet is " + str(bet) + " Your current balance is " + str(getBalance(user)) )

  
  dealers_hand = generateHand(2)
  players_hand = generateHand(2)


  dealer = Player(dealers_hand)
  player = Player(players_hand)

  print("Dealer has ? and " + str(dealers_hand[1]))
  print("Dealers total so far = "+str(totalDict[dealer.cards[1].number]))
  print("Player has "+str(players_hand).strip("[]"))
  print("Your total ="+str(player.generateTotal()))

  while True:
    if checkPlayerBj(player) == True:
      print("Congrats Blackjack!")
      addBalance(user, bet*3)
      print("You now have " + str(getBalance(user)))
      break

    a = input("Hit(h) or Stand(s)? ").lower()

    if a == "h":
      playerHit(player)
      print("Player has "+str(players_hand).strip("[]"))
      print("Your total = "+str(player.generateTotal()))
      if player.generateTotal() == 21 :
        a = "s"
      elif player.generateTotal() > 21:
        print("\nPlayer loses, Dealer wins.")
        break
 

    if a == "s":
      print("Dealer has " + str(dealers_hand).strip("[]"))
      print("Dealers total = "+str(dealer.generateTotal()))
      print("Player has "+str(players_hand).strip("[]"))
      print("Your total ="+str(player.generateTotal()))

      if checkWin(player,dealer) == 1:
        print("\nPlayer Wins!")
        addBalance(user, bet*2)
        print("You now have " + str(getBalance(user)))
      
      elif checkWin(player,dealer) == 2:
        print("\nPlayer loses, Dealer wins.")

      elif checkWin(player,dealer) == 3:
        print("\nIts a Tie!")
        addBalance(user, bet)
        print("You now have " + str(getBalance(user)))
      break


if __name__ == "__main__":
    main()
