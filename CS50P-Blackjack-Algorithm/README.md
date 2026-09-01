# Optimized Blackjack Algorithm
    #### Video Demo:  https://www.youtube.com/watch?v=XlawP6wcd0s
    #### Description:

    This optimized blackjack playing algorithm aims to maximize returns on an initial investment utilizing two main strategies. Firstly using the blackjack "basic strategy" also called "perfect strategy", which is mathematical model indicating what is the optimal move based on the player and dealer hand, mainly the player and dealer score. The algorithm accesses the optimal move through separate csv files. Secondly, the algorithm uses card counting to adjust the betting quantities. This allows to bet more tokens (or money) when the cards left in the deck are favorable to the player. Below is a step by step guide as to how the algorithm works.

    The first step is to generate all the cards that make up the 6 decks we will be using. This is achieved by repeating 6 times through a "for loop" which each creates a full deck. Inside this loop are two lists, one with colours, one with numbers (or faces), which are cycled through by utilizing two other "for loops" to create all the possible cards.

    For the simplicity of the following explanations, suppose multiple hands have already been played.

    Once the deck is created, the betting phase occurs. A counting_cards function tracks every time a card is distributed from the deck (and removed from the deck list), and checks what card it is. Each card is associated with a value (-1,0, or +1), depending on whether it is a high, neutral, or low card. The function then adds the corresponding value of the card to the running count. The true count is then calculated from the running counts and the number of cards left in the deck.
    Depending on the true count, a betting function will assess how many tokens to bet this round. A minimum and maximum bet limit is in place to not risk too much, or miss out on wins. If the bet wanted by the algorithm is between the maximum and minimum bets, then the following formula determines how many tokens to bet : tokens_bet = betting_unit*(true_count-1).
    In this case the betting unit used was 100 tokens (10 000 total tokens).

    Following the bet being placed, the game is initiliased. A random_card function takes a random card from the deck and then deletes it from the deck list. Using this function, two cards are distributed to the player, and one card to the dealer.

    Once the game is initialised, it is time for the algorithm to make a decision on what to do (hit/stand/double/split). The algorithm utilizes the blackjack basic strategy to limit the amount of hands lost to the house.
    These ideal moves are stored in three different csv files based on what hand the algorithm is dealt. One is for a hard hand (no Ace), one is for a soft hand (Ace), and one is for a split hand (two of the same cards). A function allows to determine whether an Ace is in the algorithm's hand. The algorithm then accesses the csv file associated with its hand. The csv file is structured as a table, with the player score and dealer score as rows and columns.
    Using a DictReader, the program goes through a "for loop" until the actual player score and dealer score match a specific location in the table. The letter is then returned (h = hit, s = stand, d = double, p = split). After the algorithm knows what action to take, a separate function (players_round) acts accordingly. Inside the players_round function is an infite "while True loop" such that the program can keep hitting, or splitting until it stands or doubles, or surpasses a score of 21. If the program stands, the loop breaks. If the program doubles, one last card is distributed to the algorithm's hand before the loop breaks. If the program hits, a card is simply distributed to its hand. Finally if the programm splits, a separate function is opened (split), where the value of the cards is stored, but two new rounds are initialized (each with one of the stored algorithm's cards), and the dealer's hand remains the same for both hands. The players_round function is then called within the split function to make a decision for each of the two hands being played simultaneously.

    After the algorithm has finished making decisions, the dealer is distributed cards until its score is greater or equal to 17.

    Then, an outcome function determines which of the algorithm or dealer won the hand. After, a separate tokens_managment function adds/deduces the tokens bet from the total tokens depending on who won the hand.

    At the end of each hand, a plotting_tracking function stores the values of the current number of hands played, and the current total tokens in lists.

    Finally, a shuffling function checks how many cards are left in the deck. If less than 30 cards remain in the deck, then the deck is re-initialized and back to containing all 6 decks. If there are more than 30 cards remaining, then the game continues without reshuffling.

    To conclude, this whole process is repeated 1000 times inside a for loop in order to simulate 1000 hands. At the end of the simulation, a plot is created with the evolution of the total number of tokens against the number of hands played. Two lines are present on this graph, one which implements the card counting strategy, and one which always betts the betting unit(100). For the betting without card counting, the tokens are simply determined by bypassing the betting function and assuming the bet is 100 units. Finally, key metrics such as the number of wins, losses, pushes, blackjacks, the average tokens at any instant, the maximum/minimum tokens, the houses' edge per hand, the average return per hand, and the end tokens are all stored in a dictionary and printed at the end. This allows to better analyze the performance of the algorithm at the end of the simulation, and could help potentially improving the algortithm by including a stop loss and cash out value (so telling the algorithm when to stop instead of blindly simulating 1000 hands).

    This was my CS50P graduation project on an optimized blackjack algorithm ! Thank you for reading.
