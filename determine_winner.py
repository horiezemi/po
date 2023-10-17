# 勝者を判定するプログラムです。

from itertools import combinations
from collections import Counter

def hand_strength(hand):
    hand = sorted(hand, key=lambda c: "23456789TJQKA".index(c[0]), reverse=True)
    counts = Counter([card[0] for card in hand])
    count_vals = list(reversed(sorted(counts.values())))
    groups = sorted(list(counts.items()), key=lambda c: (c[1], "23456789TJQKA".index(c[0])), reverse=True)

    if len(set([card[1] for card in hand])) == 1 and "AKQJT" in "".join([card[0] for card in hand]):
        return (9, ) + tuple("23456789TJQKA".index(r) for r, _ in groups), "ロイヤルストレートフラッシュ"
    elif len(set([card[1] for card in hand])) == 1 and "".join([card[0] for card in hand]) in "AKQJT98765432":
        return (8, ) + tuple("23456789TJQKA".index(r) for r, _ in groups), "ストレートフラッシュ"
    elif count_vals == [4, 1]:
        primary, kicker = groups[0][0], groups[1][0]
        return (7, "23456789TJQKA".index(primary), "23456789TJQKA".index(kicker)), "フォーカード"
    elif count_vals == [3, 2]:
        primary, secondary = groups[0][0], groups[1][0]
        return (6, "23456789TJQKA".index(primary), "23456789TJQKA".index(secondary)), "フルハウス"
    elif len(set([card[1] for card in hand])) == 1:
        return (5, ) + tuple("23456789TJQKA".index(r) for r, _ in groups), "フラッシュ"
    elif "".join([card[0] for card in hand]) in "AKQJT98765432":
        return (4, ) + tuple("23456789TJQKA".index(r) for r, _ in groups), "ストレート"
    #elif "A5432" in "".join([card[0] for card in hand]):# Aを最低ランクとして使える場合の例外処理
        #return (4, 3, 2, 1, 0, -1), "ストレート"
    elif count_vals == [3, 1, 1]:
        primary, kicker1, kicker2 = groups[0][0], groups[1][0], groups[2][0]
        return (3, "23456789TJQKA".index(primary), "23456789TJQKA".index(kicker1), "23456789TJQKA".index(kicker2)), "スリーカード"
    elif count_vals == [2, 2, 1]:
        primary, secondary, kicker = groups[0][0], groups[1][0], groups[2][0]
        return (2, "23456789TJQKA".index(primary), "23456789TJQKA".index(secondary), "23456789TJQKA".index(kicker)), "ツーペア"
    elif count_vals == [2, 1, 1, 1]:
        primary, kicker1, kicker2, kicker3 = groups[0][0], groups[1][0], groups[2][0], groups[3][0]
        return (1, "23456789TJQKA".index(primary), "23456789TJQKA".index(kicker1), "23456789TJQKA".index(kicker2), "23456789TJQKA".index(kicker3)), "ワンペア"
    else:
        return (0, ) + tuple("23456789TJQKA".index(r) for r, _ in groups), "ハイカード"

# 最も強い手札を選ぶ関数
def best_hand(cards):
    return max(combinations(cards, 5), key=lambda hand: hand_strength(hand)[0])#変数handにはcombinations(cards, 5)の一つ一つが代入される

# 出力時のフォーマット修正を行う関数
def format_hand(hand):
    hand_str = ", ".join([card[0] + card[1] for card in hand])
    return "({})".format(hand_str)


# 勝敗判定を行い、役名と最強の５枚のカードを表示する関数
def determine_winner(player_hand, computer_hand, community_cards):
    player_best_hand = best_hand(player_hand + community_cards)
    computer_best_hand = best_hand(computer_hand + community_cards)

    player_strength, player_hand_name = hand_strength(player_best_hand)
    computer_strength, computer_hand_name = hand_strength(computer_best_hand)

    result = ""
    if player_strength > computer_strength:
        result = "プレイヤーの勝ち"
    elif player_strength < computer_strength:
        result = "コンピュータの勝ち"
    else:
        result = "引き分け"

    print("プレイヤーの手札: {} 役: {}".format(format_hand(player_best_hand), player_hand_name))
    print("コンピュータの手札: {} 役: {}".format(format_hand(computer_best_hand), computer_hand_name))

    return result

