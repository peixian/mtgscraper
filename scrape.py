import requests
import numpy as np
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
        for item in mbList.find_all("li"):
            mainboard.append([int(item.text[0]), item.text[2:]])
    
    sideboard = []
    for sbItem in deck.find("div", class_="deck_sideboard").find_all("li"):
        sideboard.append([int(sbItem.text[0]), sbItem.text[2:]])
    
    assert sum([card[0] for card in mainboard]) >= 60 and sum(card[0] for card in sideboard) <= 15
    
    return (deck, name, player, place, mainboard, sideboard)
    
grabSCGDeck("http://sales.starcitygames.com//deckdatabase/displaydeck.php?DeckID=97570")

