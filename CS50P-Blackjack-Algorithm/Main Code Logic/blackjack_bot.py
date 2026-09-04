import random
import csv
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Choose whether you want 1 or 500 games played (1 = plotting, 500 = adding results to csv)
#number_games = 1 
number_games = 500

for _ in range(number_games) :

    # Defining file paths for accessing optimal strategy through external csv files
    split_file_path = r"perfect_blackjack_split.csv"
    hard_file_path = r"perfect_blackjack_hard.csv"
    soft_file_path = r"perfect_blackjack_soft.csv"


    # Initialising 
    cards = []

    card_counting_values = {"ace" : -1, "2" : 1, "3" : 1, "4" : 1, "5" : 1, "6" : 1, "7" : 0, "8" : 0, "9" : 0, "10" : -1, "king" : -1, "queen" : -1, "jack" : -1 }

    player_distributed_cards, dealer_distributed_cards  = [], []

    number_wins, number_losses, number_pushes, number_blackjack = 0, 0, 0, 0

    total_tokens = 10000
    basic_total_tokens = 10000
    basic_tokens_bet = 100 
    total_number_simulations = 1000

    tokens_tracking = [total_tokens]
    bets_tracking = []
    basic_tokens_tracking = [basic_total_tokens]
    number_plays = 0
    number_plays_list = [0]

    def generate_deck(): 
        global number_decks 
        number_decks = 6
        numbers = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
        colours = ["spades", "hearts", "diamonds", "clubs"] 
        for _ in range(number_decks) : 
            for i in range(len(numbers)) : 
                for j in range(len(colours)) : 
                    cards.append(f"{numbers[i]} of {colours[j]}")

    generate_deck()

    def shuffling():
        global player_distributed_cards, dealer_distributed_cards, cards 
        if len(cards) >= 30 : 
            return None 
        else : 
            player_distributed_cards.clear()
            dealer_distributed_cards.clear()
            cards.clear()
            generate_deck()
            return None

    def random_card():
        while True : 
            number = random.randint(0,len(cards)-1)
            card = cards[number]
            cards.remove(card)
            return card

    def outcome(player_cards, dealer_cards): 
        score = get_score(player_cards, dealer_cards)
        player_score = score["player score"]
        dealer_score = score["dealer score"]
        if player_score > 21 : 
            return "You lose :("
        elif dealer_score > 21 : 
            return "You win !"
        elif player_score == 21 and dealer_score != 21 and len(player_cards) == 2 :
            return "Blackjack"
        elif player_score == 21 and dealer_score == 21 and len(player_cards) ==2 and len(dealer_cards) != 2 : 
            return "Blackjack"
        elif player_score > dealer_score : 
            return "You win !"
        elif player_score < dealer_score : 
            return "You lose :("
        else : 
            return "It's a push..."

    def score_of_cards(card):
        if "king" == card.split(" of ")[0] or "queen" == card.split(" of ")[0] or "jack" == card.split(" of ")[0]: 
            score_of_card = 10
        elif "ace" == card.split(" of ")[0] : 
            score_of_card = 1
        else : 
            score_of_card = int(card.split(" of ")[0])
        return score_of_card

    def Ace_in_hand (player_cards, dealer_cards) : 
        Ace_in_player_cards, Ace_in_dealer_cards = False, False
        for player_card in player_cards : 
            if "ace" in player_card.split(" of ")[0] : 
                Ace_in_player_cards = True
        for dealer_card in dealer_cards : 
            if "ace" in dealer_card.split(" of ")[0] : 
                Ace_in_dealer_cards = True 
        return {"Ace in player cards" : Ace_in_player_cards, "Ace in dealer cards" : Ace_in_dealer_cards}

    def get_score(player_cards, dealer_cards): 
        player_score = 0
        dealer_score = 0
        for player_card in player_cards : 
                player_score += score_of_cards(player_card)
        for dealer_card in dealer_cards :  
                dealer_score += score_of_cards(dealer_card)
        if Ace_in_hand(player_cards, dealer_cards)["Ace in player cards"] == True : 
            if player_score + 10 <= 21 : 
                player_score += 10  
        if Ace_in_hand(player_cards, dealer_cards)["Ace in dealer cards"] == True : 
            if dealer_score + 10 <= 21 : 
                dealer_score += 10 
        return {"player score" : player_score, "dealer score" : dealer_score}

    def game_initilisation(): 
        global player_distributed_cards_this_round
        global dealer_distributed_cards_this_round
        player_distributed_cards_this_round = [] 
        dealer_distributed_cards_this_round = []
        for _ in range(2) :
            player_card = random_card()
            player_distributed_cards.append(player_card)
            player_distributed_cards_this_round.append(player_card)
        dealer_card = random_card()
        dealer_distributed_cards.append(dealer_card)
        dealer_distributed_cards_this_round.append(dealer_card)

    def players_round(): 
        global tokens_bet, total_tokens, split_impossible
        split_impossible = False # i..e you can split
        def hit(): 
            player_card = random_card()
            player_distributed_cards.append(player_card)
            player_distributed_cards_this_round.append(player_card)
        def double():
            global tokens_bet 
            tokens_bet *= 2
            player_card = random_card()
            player_distributed_cards.append(player_card)
            player_distributed_cards_this_round.append(player_card)
        while True : 
            score = get_score(player_distributed_cards_this_round, dealer_distributed_cards_this_round)
            if score["player score"] > 21 : 
                return "You lose :("
            elif score["player score"] == 21 and len(player_distributed_cards_this_round) == 2 : 
                return "Blackjack"
            else : 
                answer = bot_decision()
                if answer == "h" :
                    hit()
                elif answer == "s" :
                    break
                elif "d" in answer : 
                    if len(player_distributed_cards_this_round) > 2 or total_tokens < 2*tokens_bet:
                        if "h" in answer : 
                            hit()
                        elif "s" in answer : 
                            break
                    else : 
                        double()
                        break
                elif answer == "p" and total_tokens >= 2*tokens_bet: 
                    return "split"
                elif answer == "p" and total_tokens < 2*tokens_bet:
                    split_impossible = True # splitting requires at least double the amount of tokens initially bet
                elif answer == "No decision found": 
                    sys.exit("This does not work")

    def split(): 
        global number_losses, number_wins, number_pushes, total_tokens, player_distributed_cards_this_round, dealer_distributed_cards_this_round
        split_cards = player_distributed_cards_this_round
        player_distributed_cards_this_round = []
        player_distributed_cards_this_round.append(split_cards[0])
        card = random_card()
        player_distributed_cards_this_round.append(card)
        player_distributed_cards.append(card)

        players_round()
        dealers_round()

        dealer_split_cards = dealer_distributed_cards_this_round
        dealer_distributed_cards_this_round = []
        dealer_distributed_cards_this_round.append(dealer_split_cards[0])
        
        tokens_managment()
        plotting_tracking()

        player_distributed_cards_this_round = []
        player_distributed_cards_this_round.append(split_cards[1])
        card = random_card()
        player_distributed_cards_this_round.append(card)
        player_distributed_cards.append(card)

        players_round()

        for i in range(len(dealer_split_cards)-1) : 
            dealer_distributed_cards_this_round.append(dealer_split_cards[i+1])

        tokens_managment()
        plotting_tracking()

    def dealers_round(): 
        while True : 
            dealer_card = random_card()
            dealer_distributed_cards.append(dealer_card)
            dealer_distributed_cards_this_round.append(dealer_card)
            score = get_score(player_distributed_cards_this_round, dealer_distributed_cards_this_round)
            dealer_score = score["dealer score"]
            if dealer_score == 21 and len(dealer_distributed_cards_this_round) == 2 : 
                return "Dealer Blackjack"
            elif dealer_score >= 17 : 
                break
            else : 
                pass

    def counting_cards(): 
        running_count = 0
        number_of_decks_remaining = len(cards)/52
        for player_card in player_distributed_cards : 
            for card in card_counting_values : 
                if player_card.split(" of ")[0] == card : 
                    running_count += card_counting_values[card]
        for dealer_card in dealer_distributed_cards : 
            for card in card_counting_values : 
                if dealer_card.split(" of ")[0] == card : 
                    running_count += card_counting_values[card]
        true_count = round(2*(running_count/number_of_decks_remaining))/2
        return true_count

    def bot_decision(): 
        score = get_score(player_distributed_cards_this_round, dealer_distributed_cards_this_round)
        player_score = score["player score"]
        dealer_score = score["dealer score"]
        if len(player_distributed_cards_this_round) == 2 and player_distributed_cards_this_round[0].split(" of ")[0] == player_distributed_cards_this_round[1].split(" of ")[0] and split_impossible==False :
            with open(split_file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows : 
                    if player_distributed_cards_this_round[0].split(" of ")[0] == row["double card"].strip() : 
                        return row[f"dealer {dealer_score}"]
                return "No decision found"
        else : 
            if Ace_in_hand(player_distributed_cards_this_round, dealer_distributed_cards_this_round)["Ace in player cards"] == False : 
                with open (hard_file_path, "r", encoding="utf-8") as file :
                    reader = csv.DictReader(file)
                    rows = list(reader)
                    for row in rows : 
                        if player_score == int(row["player score"].strip()) : 
                            return row[f"dealer {dealer_score}"]
                    return "No decision found"
            elif Ace_in_hand(player_distributed_cards_this_round, dealer_distributed_cards_this_round)["Ace in player cards"] == True : 
                with open(soft_file_path, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)
                    for row in rows : 
                        if player_score == int(row["player score"].strip()) : 
                            return row[f"dealer {dealer_score}"]
                    return "No decision found"

    def betting(): 
        global tokens_bet, betting_unit 
        betting_unit = 100
        true_count = counting_cards()
        max_bet = 4*betting_unit
        if true_count > 5 : 
            tokens_bet = max_bet
        elif 5 >= true_count >=2 :
            tokens_bet = betting_unit*(true_count-1)
        else :
            tokens_bet = betting_unit
        tokens_bet = min(tokens_bet, total_tokens) # never bet more tokens than are left
        return tokens_bet

    def tokens_managment() : 
        global total_tokens, tokens_bet, basic_total_tokens, basic_tokens_bet, number_wins, number_losses, number_pushes, number_blackjack
        outcome_game = outcome(player_distributed_cards_this_round, dealer_distributed_cards_this_round)
        if outcome_game == "Blackjack" : 
            number_wins += 1 
            number_blackjack += 1
            total_tokens += tokens_bet*1.5
            basic_total_tokens += basic_tokens_bet*1.5
        elif outcome_game == "You win !" : 
            number_wins += 1
            total_tokens += tokens_bet
            basic_total_tokens += basic_tokens_bet
        elif outcome_game == "It's a push..." : 
            number_pushes += 1
        elif outcome_game == "You lose :(" : 
            number_losses += 1
            total_tokens -= tokens_bet
            basic_total_tokens -= basic_tokens_bet

    def plotting_tracking():
        global number_plays
        tokens_tracking.append(total_tokens)
        bets_tracking.append(tokens_bet)
        basic_tokens_tracking.append(basic_total_tokens)
        number_plays += 1
        number_plays_list.append(number_plays)

    def plotting(): 
        plt.plot(number_plays_list, tokens_tracking, color = "blue", alpha = 0.7, label = "With card counting betting strategy")
        plt.plot(number_plays_list, basic_tokens_tracking, color = "red", alpha = 0.7, label = "No card counting betting strategy")
        plt.xlabel("Number of hands played")
        plt.ylabel("Total number of tokens")
        plt.title("Blakcjack algorithm performance")
        plt.legend()
        plt.show()

    def main():
        global number_wins, number_losses, number_pushes, total_tokens
        for _ in range(total_number_simulations) :
            if total_tokens <= 0 :
                break
            shuffling()
            game_initilisation()
            betting()
            player_move = players_round()
            if player_move == "split" :
                split()
            else :
                dealers_round()
                tokens_managment()
                plotting_tracking()
        simulation_performance()
        if number_games == 1 : 
            plotting()

    def simulation_performance(): 
        global number_wins, number_losses, number_pushes, total_tokens, tokens_tracking, bets_tracking
        performance_dictionary = {
            "number_wins" : number_wins,
            "number_losses" : number_losses,
            "number_pushes" : number_pushes,
            "number_blackjack" : number_blackjack,
            "house_advantage_%" : 100*((number_losses-number_wins)/len(tokens_tracking)),
            "end_tokens" : total_tokens,
            "max_tokens" : max(tokens_tracking),
            "min_tokens" : min(tokens_tracking),
            "average_tokens" : np.mean(tokens_tracking),
            "total_profit" : tokens_tracking[-1] - tokens_tracking[0],
            "total_bets" : sum(bets for bets in bets_tracking),
            "average_return_per_hand" : (tokens_tracking[-1] - tokens_tracking[0])/sum(bets for bets in bets_tracking),
            "end_tokens_without_card_counting" : basic_total_tokens,
            "min_tokens_without_card_counting" : min(basic_tokens_tracking)
        }

        if number_games > 1 : 
            csv_file = r"blackjack_bot_results.csv"
            file_is_new = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
            with open (csv_file, mode = "a", newline = "") as file :
                writer = csv.DictWriter(file, fieldnames = performance_dictionary.keys())
                if file_is_new :
                    writer.writeheader()
                writer.writerow(performance_dictionary)
        else : 
            print(performance_dictionary)
        return performance_dictionary

    if __name__ == "__main__" : 
        main()