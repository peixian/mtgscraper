import requests
from bs4 import BeautifulSoup

def grabSCGDeck(scgUrl):
    """takes url for a starcity decklist, grabs the deck"""
    page = BeautifulSoup(requests.get(scgUrl).content, 'lxml')
    deck = page.find(id="article_content")
    name = deck.find_all("header", class_="deck_title")[0].a.text
    player = deck.find("header", class_="player_name").a.text
    place = deck.find("header", class_="deck_played_placed").text
    mainboard = []
    for mbList in deck.find("div", class_="deck_card_wrapper").find_all("ul")[:-1]:
        for li in mbList:
            print(li.text)
            print(type(li))
            # mainboard.append(li)
        # prin
        # mainboard.append((int(li[0].text), li[1:]))

    # print(deck.prettify())
    print(name)
    print(player)
    print(place)
    print(mainboard)
    
grabSCGDeck("http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID=97570")

