import random
from odds_calculate import computer_handler
from determine_winner import determine_winner
from player_option import first_option, option_to_reraise, option_to_allin

suits = ['♠', '♣', '♢', '♡']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']



class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank}{self.suit}'


def create_deck():
    deck = [Card(suit, rank) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


def deal_hands(deck):
    player_hand = [deck.pop(), deck.pop()]
    computer_hand = [deck.pop(), deck.pop()]
    return player_hand, computer_hand


def deal_community_cards(deck):
    return [deck.pop() for _ in range(5)]


def show_hands(player_hand, community_cards, revealed, computer_hand=None):
    print(f"あなたの手札: {', '.join(str(card) for card in player_hand)}")
    print(f"コミュニティカード: {', '.join(str(card) if i < revealed else 'X' for i, card in enumerate(community_cards))}")#enumerateは要素番号を示す　iは各々の要素番号
    if computer_hand:
        print(f"コンピュータの手札: {', '.join(str(card) for card in computer_hand)}")
    else:
        print("コンピュータの手札: 非公開")
        
def betting_round(player_chips, computer_chips, pot, game_over, folder):
    # コンピュータのベット
    # プリフロップの場合
    if pot == 0:
        bet_amount = 10
        print(f"コンピュータは{bet_amount}チップをベットしました。")
        computer_behavior = 10
    # フロップ以降
    else:
        computer_behavior = computer_handler(False, 0, 0, computer_chips, pot, computer_hand_str, community_cards_str)
        if computer_behavior == "チェック":
            bet_amount = 0
            print("コンピュータはチェックしました。")
        elif computer_behavior == "オールイン":
            bet_amount = computer_chips
            print("コンピュータはオールインしました。")
        else:
            bet_amount = computer_behavior
            print(f"コンピュータは{bet_amount}チップをベットしました。")
    computer_chips -= bet_amount
    pot += bet_amount
    print(f"現在のポット: {pot}チップ")

    # レイズ変数の設定
    raised = False
    # プレイヤーの行動選択の入力
    player_bet = first_option(computer_behavior, bet_amount, player_chips, pot)
    
    # プレイヤーがフォールドした場合
    if player_bet == 'f':
        computer_chips += pot
        pot = 0
        game_over = True
        folder = "player"
        print("あなたがフォールドしました。コンピュータが勝ちました。")
        return player_chips, computer_chips, pot, game_over, folder
    
    # プレイヤーがオールインした場合
    elif player_bet == 'a':
        pot += player_chips
        player_chips = 0
        current_bet = pot - bet_amount
        print("あなたはオールインしました。")
        # コンピュータの行動選択
        computer_behavior = computer_handler(True, current_bet, current_bet - bet_amount, computer_chips, pot, computer_hand_str, community_cards_str)
        if computer_behavior != "フォールド":
            computer_behavior = "オールイン"
        if computer_behavior == "フォールド":
            player_chips += pot
            pot = 0
            game_over = True
            folder = "computer"
            print("コンピュータがフォールドしました。あなたの勝ちです。")
            return player_chips, computer_chips, pot, game_over, folder
        # オールインの場合
        else:
            pot += computer_chips
            computer_chips = 0
            game_over = True
            print("コンピュータはオールインしました。")
            return player_chips, computer_chips, pot, game_over, folder
    
    # プレイヤーがコールした場合
    elif player_bet == 'c':
        player_chips -= bet_amount#コンピューターが賭けた額
        pot += bet_amount
        print("あなたはコールしました。次のラウンドに進みます。")
        return player_chips, computer_chips, pot, game_over, folder
    
    # プレイヤーがレイズした場合
    else:
        player_chips -= player_bet
        pot += player_bet
        print(f"現在のポット: {pot}チップ")
        raise_amount = player_bet - bet_amount
        raised = True
        # コンピュータの行動選択
        while raised:
            computer_behavior = computer_handler(True, player_bet, raise_amount, computer_chips, pot, computer_hand_str, community_cards_str)

            if computer_behavior == "フォールド":
                player_chips += pot
                pot = 0
                game_over = True
                folder = "computer"
                print("コンピュータがフォールドしました。あなたの勝ちです。")
                break
            elif computer_behavior == "コール":
                computer_chips -= raise_amount
                pot += raise_amount
                print("コンピュータはコールしました。")
                break
            elif computer_behavior == "オールイン":
                pot += computer_chips
                computer_chips = 0
                print("コンピュータはオールインしました。")

                # プレイヤーの行動選択の入力
                player_bet = option_to_allin()
                if player_bet == 'a':
                    pot += player_chips
                    player_chips = 0
                    game_over = True
                    print("あなたはオールインしました。")
                    break
                # フォールドの場合
                else:
                    computer_chips += pot
                    pot = 0
                    game_over = True
                    folder = "player"
                    print("あなたがフォールドしました。コンピュータの勝ちです。")
                    break
            # リレイズの処理
            else:
                new_bet = computer_behavior
                computer_chips -= new_bet - bet_amount
                pot += new_bet - bet_amount
                bet_amount = new_bet
                print(f"コンピュータは{new_bet}チップにリレイズしました。")
                # プレイヤーの行動選択の入力
                raised_player_bet = option_to_reraise(new_bet, player_bet, player_chips, False)
                while True:
                    try:
                        if raised_player_bet == 'a':
                            pot += player_chips
                            current_bet = player_bet + player_chips
                            player_chips = 0
                            print("あなたがオールインしました。")
                             # コンピュータの行動選択
                            computer_behavior = computer_handler(True, current_bet, current_bet - new_bet, computer_chips, pot, computer_hand_str, community_cards_str)
                            if computer_behavior != "フォールド":
                                computer_behavior = "オールイン"

                            if computer_behavior == "フォールド":
                                player_chips += pot
                                pot = 0
                                game_over = True
                                folder = "computer"
                                print("コンピュータがフォールドしました。あなたの勝ちです。")
                            # オールインの場合
                            else:
                                pot += computer_chips
                                computer_chips = 0
                                game_over = True
                                print("コンピュータはオールインしました。")
                            break
                        
                        elif raised_player_bet == 'f':
                            game_over = True
                            folder = "player"
                            computer_chips += pot
                            pot = 0
                            print("あなたがフォールドしました。コンピュータが勝ちました。")
                            break
                        
                        elif raised_player_bet == 'c':
                            player_chips -= new_bet - player_bet
                            pot += new_bet - player_bet
                            raised = False
                            print("あなたがコールしました")
                            break
                        
                        # レイズの場合
                        else:
                            raised_player_bet = int(raised_player_bet)
                            if raised_player_bet < new_bet * 2 or raised_player_bet > player_bet + player_chips - 1:
                                raise ValueError
                            else:
                                player_chips -= raised_player_bet - player_bet
                                pot += raised_player_bet - player_bet
                                player_bet = raised_player_bet
                                break
                    except ValueError:
                        raised_player_bet = option_to_reraise(new_bet, player_bet, player_chips, True)
                        
        return player_chips, computer_chips, pot, game_over, folder

def main():
    # 初期設定
    player_chips = 1000
    computer_chips = 1000
    pot = 0
    game_over = False
    folder = "None"
    deck = create_deck()
    
    #グローバル変数の宣言
    global player_hand, computer_hand, community_cards, revealed
    player_hand, computer_hand = deal_hands(deck)
    community_cards = deal_community_cards(deck)
    global player_hand_str, computer_hand_str, community_cards_str
    player_hand_str = [str(card) for card in player_hand]
    computer_hand_str = [str(card) for card in computer_hand]
    full_community_cards_str = [str(card) for card in community_cards]
    
    #各ラウンドの実施
    print("\nプリフロップベッティングラウンド")
    revealed = 0 #revealedは明らかにする場のカードの枚数を示す
    community_cards_str = full_community_cards_str[0:revealed]
    show_hands(player_hand, community_cards, revealed)
    player_chips, computer_chips, pot, game_over, folder = betting_round(player_chips, computer_chips, pot, game_over, folder)
    
    # game_over が False の場合のみ次のラウンドを実行
    if not game_over: #game_overがtrueじゃない
        print("\nフロップ")
        revealed = 3
        community_cards_str = full_community_cards_str[0:revealed]
        show_hands(player_hand, community_cards, revealed)
        player_chips, computer_chips, pot, game_over, folder = betting_round(player_chips, computer_chips, pot, game_over, folder)

    if not game_over:
        print("\nターン")
        revealed = 4
        community_cards_str = full_community_cards_str[0:revealed]
        show_hands(player_hand, community_cards, revealed)
        player_chips, computer_chips, pot, game_over, folder = betting_round(player_chips, computer_chips, pot, game_over, folder)

    if not game_over:
        print("\nリバー")
        revealed = 5
        community_cards_str = full_community_cards_str[0:revealed]
        show_hands(player_hand, community_cards, revealed)
        player_chips, computer_chips, pot, game_over, folder = betting_round(player_chips, computer_chips, pot, game_over, folder)

    if folder == "None": #降りた人が誰もいなかった場合
        print("\nショーダウン")
        revealed = 5
        show_hands(player_hand, community_cards, revealed, computer_hand) #互いの手札を見せあう
    else:#降りた人がいた場合
        print("\nショーダウンは行われませんでした。")

    # 勝者判定
    if folder == "None":
        result = determine_winner(player_hand_str, computer_hand_str, full_community_cards_str)
        print(result)
        if result == "プレイヤーの勝ち":
            player_chips += pot
            pot = 0
        elif result == "コンピュータの勝ち":
            computer_chips += pot
            pot = 0
        else:#引き分けの場合
            player_chips += int(pot / 2)
            computer_chips += int(pot / 2)
            pot = 0

# 結果発表
    print(f"最終結果: プレイヤー {player_chips}チップ, コンピュータ {computer_chips}チップ")
    
main()

    
    












                        



