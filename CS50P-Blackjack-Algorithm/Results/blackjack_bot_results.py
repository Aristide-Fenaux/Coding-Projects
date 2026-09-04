import pandas as pd
import numpy as np

df = pd.read_csv(r"blackjack_bot_results.csv")

column_averages = df.mean(numeric_only=True)

print(column_averages)

#getting average return per hand
total_profit = sum(df["total_profit"])
total_bets = sum(df["total_bets"])

net_return_per_hand_percentage = total_profit*100/total_bets
print(f"return per hand : {net_return_per_hand_percentage} %")

#getting std deviation
returns = df["total_profit"]/df["total_bets"]

std_return = np.std(returns,ddof=1)

print(f"standard deviation : {std_return}")

#getting average return per hand without card counting (flat bet of 100 tokens every hand)
total_profit_no_count = sum(df["end_tokens_without_card_counting"] - 10000)
total_bets_no_count = 100*sum(df["number_wins"] + df["number_losses"] + df["number_pushes"])

net_return_per_hand_percentage_no_count = total_profit_no_count*100/total_bets_no_count
print(f"return per hand without count : {net_return_per_hand_percentage_no_count} %")

#getting number of busted sessions (went below 0 tokens at some point)
busted_sessions = sum(df["end_tokens"] <= 0)
busted_sessions_no_count = sum(df["min_tokens_without_card_counting"] <= 0)

print(f"Busted sessions with card counting: {busted_sessions} / {len(df)}")
print(f"Busted sessions without card counting: {busted_sessions_no_count} / {len(df)}")



