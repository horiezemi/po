# コンピュータが行動選択を行うためのプログラムです。
import random
from collections import Counter
from itertools import combinations


# コンピュータの希望追加ベット額を期待値から求める関数
def simulate_holdem(hole_cards, community_cards, current_bet, raised_chip, pot, num_opponents=1, num_trials=3000):
    deck = [r + s for r in "23456789TJQKA" for s in "♠♣♢♡" if r + s not in hole_cards + community_cards]
    
    def hand_strength(hand):#カードの役の強さの指標を示す関数
        hand = sorted(hand, key=lambda c: "23456789TJQKA".index(c[0]), reverse=True)#手札を数字が強い順に並べる
        counts = Counter([card[0] for card in hand])
        count_vals = list(reversed(sorted(counts.values())))#手札と場に出てるカードの種類の枚数のカウント数
        groups = sorted(list(counts.items()), key=lambda c: (c[1], "23456789TJQKA".index(c[0])), reverse=True)
        
        if len(set([card[1] for card in hand])) == 1 and "AKQJT" in "".join([card[0] for card in hand]):#ロイヤルストレートフラッシュ
            return (9, ) + tuple("23456789TJQKA".index(r) for r, _ in groups)#max(combnations())で使う組み合わせ、指標
        elif len(set([card[1] for card in hand])) == 1 and "".join([card[0] for card in hand]) in "AKQJT98765432":#ストレートフラッシュ
            return (8, ) + tuple("23456789TJQKA".index(r) for r, _ in groups)
        elif count_vals == [4, 1]:#フォーカード
            primary, kicker = groups[0][0], groups[1][0]
            return (7, "23456789TJQKA".index(primary), "23456789TJQKA".index(kicker))
        elif count_vals == [3, 2]:#フルハウス
            primary, secondary = groups[0][0], groups[1][0]
            return (6, "23456789TJQKA".index(primary), "23456789TJQKA".index(secondary))
        elif len(set([card[1] for card in hand])) == 1:#フラッシュ
            return (5, ) + tuple("23456789TJQKA".index(r) for r, _ in groups)
        elif "".join([card[0] for card in hand]) in "AKQJT98765432":#ストレート
            return (4, ) + tuple("23456789TJQKA".index(r) for r, _ in groups)
        #elif "A5432" in "".join([card[0] for card in hand]):# Aを最低ランクとして使える場合の例外処理
            #return (4, 3, 2, 1, 0, -1)
        elif count_vals == [3, 1, 1]:#スリーカード
            primary, kicker1, kicker2 = groups[0][0], groups[1][0], groups[2][0]
            return (3, "23456789TJQKA".index(primary), "23456789TJQKA".index(kicker1), "23456789TJQKA".index(kicker2))
        elif count_vals == [2, 2, 1]:#ツーペア
            primary, secondary, kicker = groups[0][0], groups[1][0], groups[2][0]
            return (2, "23456789TJQKA".index(primary), "23456789TJQKA".index(secondary), "23456789TJQKA".index(kicker))
        elif count_vals == [2, 1, 1, 1]:#ワンペア
            primary, kicker1, kicker2, kicker3 = groups[0][0], groups[1][0], groups[2][0], groups[3][0]
            return (1, "23456789TJQKA".index(primary), "23456789TJQKA".index(kicker1), "23456789TJQKA".index(kicker2), "23456789TJQKA".index(kicker3))
        else:
            return (0, ) + tuple("23456789TJQKA".index(r) for r, _ in groups)#役なし　ハイカード
        
    def best_hand(cards):
        return max(combinations(cards, 5), key=hand_strength)
    
    def trial():#勝かどうか判定する式かつ条件式
        random.shuffle(deck)
        my_cards = hole_cards + community_cards + deck[:5 - len(community_cards)]
        my_best_hand = best_hand(my_cards)
        opponent_hands = [deck[i:i+2] for i in range(5 - len(community_cards), 5 - len(community_cards) + 2 * num_opponents, 2)]
        opponent_best_hands = [best_hand(opponent_hand + community_cards + deck[:5 - len(community_cards)])for opponent_hand in opponent_hands]

        num_better_hands = sum(1 for opponent_best_hand in opponent_best_hands if hand_strength(opponent_best_hand) > hand_strength(my_best_hand))
        return num_better_hands == 0 #0が勝ち　1が負け
    
    num_wins = sum(1 for _ in range(num_trials) if trial())#trial()を3000回シミュレーションして勝った合計数、trial()が０なった時だけカウントする
    odds = num_wins / num_trials#勝つ確率
    desired_bet = int(odds * pot / (1 - odds)) - (current_bet - raised_chip)
    return desired_bet

# 希望追加ベット額と場の状況からコンピュータの意思決定を行う関数
def computer_handler(raised, current_bet, raised_chip, computer_chips, pot, hole_cards, community_cards):
    # 最初のベットの場合
    if not raised:
        desired_bet = simulate_holdem(hole_cards, community_cards, 0, 0, pot)
        if desired_bet < pot / 2:
            behavior = "チェック"
        elif desired_bet >= pot / 2 and desired_bet < computer_chips:
            behavior = desired_bet
        # 希望追加ベット額が所持チップよりも大きい場合
        else:
            behavior = "オールイン"

    # プレイヤーのレイズ以降
    if raised:
        desired_bet = simulate_holdem(hole_cards, community_cards, current_bet, raised_chip, pot)
        if desired_bet < raised_chip:
            behavior = "フォールド"
        elif desired_bet >= raised_chip and desired_bet < current_bet + raised_chip:
            behavior = "コール"
        elif desired_bet >= current_bet + raised_chip and desired_bet < computer_chips:
            behavior = desired_bet
        # 希望ベット額が所持チップよりも大きい場合
        else:
            behavior = "オールイン"

    return behavior