from blackjack_bot  import outcome,score_of_cards, get_score, Ace_in_hand

def test_outcome(): 
    player_cards = ["ace of spades", "king of diamonds"]
    dealer_cards = ["king of diamonds", "5 of spades", "6 of hearts"]
    assert outcome(player_cards, dealer_cards) == "Blackjack"

    player_cards = ["9 of clubs", "7 of spades", "2 of diamonds"]
    dealer_cards = ["ace of diamonds", "6 of hearts"]
    assert outcome(player_cards, dealer_cards) == "You win !"

    player_cards = ["9 of clubs", "7 of spades", "2 of diamonds"]
    dealer_cards = ["ace of diamonds", "7 of hearts"]
    assert outcome(player_cards, dealer_cards) == "It's a push..."

    player_cards = ["9 of clubs", "7 of spades", "2 of diamonds"]
    dealer_cards = ["ace of diamonds", "9 of hearts"]
    assert outcome(player_cards, dealer_cards) == "You lose :("

def test_score_of_cards(): 
    assert score_of_cards("ace of spades") == 1 
    assert score_of_cards("king of hearts") == 10 
    assert score_of_cards("7 of diamonds") == 7 
    assert score_of_cards("3 of clubs") == 3

def test_Ace_in_hand() : 
    player_cards = ["ace of spades", "2 of hearts"]
    dealer_cards = ["7 of spades, 3 of diamonds"]
    assert Ace_in_hand(player_cards, dealer_cards) == {"Ace in player cards" : True, "Ace in dealer cards" : False}

def test_get_score(): 
    player_cards = ["ace of spades", "7 of hearts"]
    dealer_cards = ["4 of clubs", "10 of diamonds", "3 of spades"]
    assert get_score(player_cards, dealer_cards) == {"player score" : 18, "dealer score" : 17}