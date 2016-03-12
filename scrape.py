import requests
import numpy as np
from bs4 import BeautifulSoup

def grabSCGDeck(scgUrl):
    """takes url for a starcity decklist, grabs the deck"""
    page = BeautifulSoup(requests.get(scgUrl).content, 'lxml')
    deck = page.find(id="article_content")
    deckName = deck.find_all("header", class_="deck_title")[0].a.text
    player = deck.find("header", class_="player_name").a.text
    place = deck.find("header", class_="deck_played_placed").text[1:]

    mainboard = []
    for mbList in deck.find("div", class_="deck_card_wrapper").find_all("ul")[:-1]:
        for item in mbList.find_all("li"):
            mainboard.append([int(item.text[0]), item.text[2:]])
    
    sideboard = []
    for sbItem in deck.find("div", class_="deck_sideboard").find_all("li"):
        sideboard.append([int(sbItem.text[0]), sbItem.text[2:]])
    
    assert sum([card[0] for card in mainboard]) >= 60 and sum(card[0] for card in sideboard) <= 15
    
    return (deckName, player, place, mainboard, sideboard)

def grabSCGTournament(scgTournamentUrl):
    """returns an array of scg deck urls"""
    deckUrls = []
    page = BeautifulSoup(requests.get(scgTournamentUrl).content, 'lxml')
    lists = page.find_all("tr")
    for row in lists:
        deck = row.find_all("td", {"class": ["deckdbbody", "deckdbbody2"]})
        if deck:
            deckUrl = deck[0].find_all("a")[0].get("href")
            if "DeckID" in deckUrl:
                deckUrls.append(deckUrl)
    return deckUrls
# grabSCGDeck("http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID=97570")

tournament  = grabSCGTournament("http://sales.starcitygames.com/deckdatabase/deckshow.php?event_ID=36&t[event]=28&start_date=2016-02-27&end_date=2016-02-28&city=&order_1=finish&limit=8&t_num=1&action=Show+Decks")

with open("test.csv", "w") as file:
    file.write("deckName,player,place,mainboard,sideboard\n")

for deckUrl in tournament:
    deckName, player, place, mainboard, sideboard = grabSCGDeck(deckUrl)
    with open("test.csv", "a") as file:
        file.write("{},{},{},{},{}\n".format(deckName, player, place, mainboard, sideboard))
