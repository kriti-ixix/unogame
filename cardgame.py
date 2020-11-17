import random

"""
To generate a deck of 108 UNO cards
Parameters: None
Return values: deck -> list
"""
def buildDeck():
    deck = []
    colours = ["Red", "Green", "Yellow", "Blue"]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "Draw Two", "Skip", "Reverse"]
    wilds = ["Wild", "Wild Draw Four"]
    
    for colour in colours:
        for value in values:
            cardVal = "{} {}".format(colour, value)
            deck.append(cardVal)
            if value != 0:
                deck.append(cardVal)
    
    for i in range(4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    
    return deck

"""
To shuffle the deck of cards
Parameters: deck -> list
Return values: deck -> list
"""
def shuffleDeck(deck):
    for cardPos in range(len(deck)):
        randPos = random.randint(0, 107)
        deck[cardPos], deck[randPos] = deck[randPos], deck[cardPos]
    return deck

"""
Draws a specified number of cards off the top of the deck
Parameters: numCards -> integer
Return: cardsDrawn -> list
"""

def drawCards(numCards):
    cardsDrawn = []
    for x in range (numCards):
        cardsDrawn.append(unoDeck.pop(0))
    return cardsDrawn

"""
Print formatted list of player's hand
Parameters: player -> integer, playerHand -> list
Return: none
"""
def showHand(player, playerHand):
    print("{}'s turn".format(player))
    print("Your Hand")
    print("-----------------------------")
    y = 1
    for card in playerHand:
        print("{}) {}".format(y, card))
        y += 1
    print("")

"""
Checking whether player is able to play a card or not
Parameters: colour -> string, value -> string, playerHand -> list
Return: boolean
"""
def canPlay(colour, value, playerHand):
    for card in playerHand:
        if "Wild" in card:
            return True
        elif colour in card or value in card:
            return True
    return False

"""
Displaying the rules of the game when --help is entered
Parameters: none
Return: none
"""
def showRules():
    print("")
    print("The game is for 2-4 players. Every player starts with seven cards, and they are dealt face down. The rest of the cards are placed in a Draw Pile face down. Next to the pile a space should be designated for a Discard Pile. The top card should be placed in the Discard Pile, and the game begins!")
    print("You have to match either by the number, color, or the symbol/Action. For instance, if the Discard Pile has a red card that is an 8 you have to place either a red card or a card with an 8 on it. You can also play a Wild card (which can alter current color in play).")
    print("Enter the number of the card you wish to play.")
    print("")
    input("Enter --resume to resume the game: ")

def checkInput(userInput):
    if userInput == "--help":
        showRules()
    elif userInput == "--resume":
        pass
    else:
        pass
    

unoDeck = buildDeck()
unoDeck = shuffleDeck(unoDeck)
discards = []

players = [] #List to store player cards
playerNames = [] #List to store player names
colours = ["Blue", "Red", "Green", "Yellow"]
numPlayers = None
print("Enter --help to display the rules of the game\n")

numPlayers = input("How many players? ")
if numPlayers == "--help" or numPlayers == "--resume":
    checkInput(numPlayers)
else:
    numPlayers = int(numPlayers)
    while len(playerNames) < numPlayers:
        tempName = input("Enter player's name: ")
        if tempName == "--help" or tempName == "--resume":
            checkInput(tempName)
        else:
            playerNames.append(tempName)
            players.append(drawCards(5))

print("The cards are:")
for (x,y) in zip(playerNames, players):
    print("Player {} has {}".format(x, y))
print("")

playerTurn = 0
playDirection = 1
playing = True
winner = None
discards.append(unoDeck.pop(0))
splitCard = discards[0].split(" ", 1)
currentColour = splitCard[0]
if currentColour != "Wild":
    cardVal = splitCard[1]
else:
    cardVal = "Any"

while playing:
    showHand(playerNames[playerTurn], players[playerTurn])
    print("Cards in discard pile: {}".format(discards[-1]))
    
    if canPlay(currentColour, cardVal, players[playerTurn]):
        cardChosen = input("Enter the number of the card you wish to play: ")
        while (cardChosen=="--help" or cardChosen=="--resume"):
            checkInput(cardChosen)
            showHand(playerNames[playerTurn], players[playerTurn])
            print("Cards in discard pile: {}".format(discards[-1]))
            cardChosen = input("Enter the number of the card you wish to play: ")
        cardChosen = int(cardChosen)    
        
        while not canPlay(currentColour, cardVal, [players[playerTurn][cardChosen-1]]):
            cardChosen = input("Invalid card. Enter the number of the card you wish to play: ")
            while (cardChosen=="--help" or cardChosen=="--resume"):
                checkInput(cardChosen)
                showHand(playerNames[playerTurn], players[playerTurn])
                print("Cards in discard pile: {}".format(discards[-1]))
                cardChosen = input("Invalid card. Enter the number of the card you wish to play: ")
            cardChosen = int(cardChosen)    

        print("You played {}".format(players[playerTurn][cardChosen-1])) 
        discards.append(players[playerTurn].pop(cardChosen-1))
        
        #Check if player won
        if len(players[playerTurn]) == 0:
            playing = False
            winner = playerNames.index(playerTurn+1)
        else:   
            #Check for special cards
            splitCard = discards[-1].split(" ", 1)
            currentColour = splitCard[0]
            if len(splitCard) == 1:
                cardVal = "Any"
            else:
                cardVal = splitCard[1]
            if currentColour == "Wild":
                for x in range(len(colours)):
                    print("{}) {}".format(x+1, colours[x]))
                newColour = input("Enter the number of the colour you wish to choose: ")
                while (newColour == "--help" or newColour == "--resume"):
                    checkInput(newColour)
                    newColour = input("Enter the number of the colour you wish to choose: ")
                
                while newColour<1 or newColour<4:
                    newColour = input("Invalid. Enter the number of the colour you wish to choose: ")
                    while (newColour == "--help" or newColour == "--resume"):
                        checkInput(newColour)
                        newColour = input("Enter the number of the colour you wish to choose: ")
                newColour = int(newColour)
                currentColour = colours[newColour-1]
            
            if cardVal == "Reverse":
                playDirection = playDirection * -1
            elif cardVal == "Skip":
                playerTurn += playDirection
                if playerTurn >= numPlayers:
                    playerTurn = 0
                elif playerTurn < 0:
                    playerTurn = numPlayers-1
            elif cardVal == "Draw Two":
                playerDraw = playerTurn + playDirection
                if playerDraw == numPlayers:
                    playerDraw = 0
                elif playerDraw < 0:
                    playerDraw = numPlayers-1
                players[playerTurn].extend(drawCards(2))
            elif cardVal == "Draw Four":
                playerDraw = playerTurn + playDirection
                if playerDraw == numPlayers:
                    playerDraw = 0
                elif playerDraw < 0:
                    playerDraw = numPlayers-1
                players[playerTurn].extend(drawCards(4))
            print("")
    
    else:
        temp = input("You can't play. Press enter to draw a card: ")
        if temp == "--help" or temp == "--resume":
            checkInput(temp)
        players[playerTurn].extend(drawCards(1))
    
    playerTurn += playDirection
    if playerTurn >= numPlayers:
        playerTurn = 0
    elif playerTurn < 0:
        playerTurn = numPlayers-1

print("Game Over!")
print("{} is the winner!".format(winner))
