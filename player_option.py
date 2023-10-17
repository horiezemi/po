# プレイヤーに行動選択の入力を求めるプログラムです。
import math

# 各ラウンドで最初にプレイヤーが行動選択を入力する関数
def first_option(computer_behavior, bet_amount, player_chips, pot):
    if computer_behavior == "チェック":
        player_bet = input(f"あなたのターン:チェックする場合は 'c', オールインする場合は 'a', ベットする場合は金額({math.ceil(pot / 2)}~{player_chips})を入力: ")
    elif bet_amount * 2 < player_chips:#コンピューターがベッドした額の二倍以上チップを持っていないとレイズできない
        player_bet = input(f"あなたのターン:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a', レイズする場合は金額({bet_amount * 2}~{player_chips - 1})を入力: ")#player_chips - 1はオールインさせない為、レイズ額が指定されている
    else:
        player_bet = input("あなたのターン:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a'を入力: ")
    
    while True:
        try:
            if player_bet in ['c', 'f', 'a']:
                break
            # レイズの場合　
            else:
                player_bet = int(player_bet)
                if player_bet < bet_amount * 2 or player_bet > player_chips - 1:
                    raise ValueError #ValueErrorを発生させる
            break
        except ValueError:#レイズできない額をしたときのエラー処理
            if computer_behavior == "チェック":
                player_bet = input(f"無効な入力です:チェックする場合は 'c', オールインする場合は 'a', ベットする場合は金額({math.ceil(pot / 2)}~{player_chips})を入力: ")
            elif bet_amount * 2 < player_chips:
                player_bet = input(f"無効な入力です:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a', レイズする場合は金額({bet_amount * 2}~{player_chips - 1})を入力: ")
            else:
                player_bet = input("無効な入力です:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a'を入力: ")
    return player_bet

# リレイズに対してプレイヤーが行動選択を入力する関数
def option_to_reraise(new_bet, player_bet, player_chips, errored):
    if not errored:
        if new_bet * 2 < player_bet + player_chips:
            raised_player_bet = input(f"あなたのターン:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a', レイズする場合は金額({new_bet * 2}~{player_bet + player_chips - 1})を入力: ")
        else:
            raised_player_bet = input("あなたのターン:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a'を入力: ")
    else:
        if new_bet * 2 < player_bet + player_chips:
            raised_player_bet = input(f"無効な入力です:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a', レイズする場合は金額({new_bet * 2}~{player_bet + player_chips - 1})を入力: ")
        else:
            raised_player_bet = input("無効な入力です:コールする場合は 'c', フォールドする場合は 'f', オールインする場合は 'a'を入力: ")

    return raised_player_bet

# オールインに対してプレイヤーが行動選択を入力する関数
def option_to_allin():
    player_bet = input("あなたのターン:フォールドする場合は 'f', オールインする場合は 'a': ")#コンピューターがオールインしたらｆかａしかできない

    # 例外処理
    while True:
        if player_bet not in ['f', 'a']:
            player_bet = input("無効な入力です:フォールドする場合は 'f', オールインする場合は 'a': ")
        else:
            break
    return player_bet
