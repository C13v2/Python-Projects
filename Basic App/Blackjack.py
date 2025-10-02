import random
import time

# Creazione del mazzo
suits = ["spades", "clubs", "hearts", "diamonds"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
cards = [(suit, rank) for suit in suits for rank in ranks]

def shuffle():
    random.shuffle(cards)

def deal(number):
    return [cards.pop() for _ in range(number) if cards]

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for _, rank in hand:
        if rank in ["J", "Q", "K"]:
            value += 10
        elif rank == "A":
            value += 11
            aces += 1
        else:
            value += int(rank)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def display_hand(player, hand, hide=False):
    if hide:
        print(f"{player}'s hand: [Carte nascoste]")
    else:
        print(f"{player}'s hand: {', '.join([f'{rank} of {suit}' for suit, rank in hand])}")

def player_turn(player, hand):
    input(f"{player}, premi Invio quando sei pronto a vedere le tue carte...")
    print("\n" * 50)  # Pulisce lo schermo simulando uno spazio vuoto
    while True:
        display_hand(player, hand)
        value = calculate_hand_value(hand)
        print(f"{player}'s total: {value}\n")
        if value > 21:
            print(f"{player} busts!\n")
            return value
        choice = input(f"{player}, vuoi pescare una carta? (h/s): ").lower()
        if choice == 'h':
            hand.extend(deal(1))
        else:
            break
    return value

def dealer_turn(dealer_hand):
    print("Il dealer gioca...")
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.extend(deal(1))
        time.sleep(1)
    return calculate_hand_value(dealer_hand)

def play_round(players):
    shuffle()
    hands = {player: deal(2) for player in players}
    dealer_hand = deal(2)
    
    values = {}
    for player in players:
        values[player] = player_turn(player, hands[player])
        input("Passa il turno al prossimo giocatore e premi Invio...")
        print("\n" * 50)
    
    dealer_value = dealer_turn(dealer_hand)
    
    print("Final results:")
    for player in players:
        display_hand(player, hands[player])
        print(f"{player} total: {values[player]}\n")
    display_hand("Dealer", dealer_hand)
    print(f"Dealer total: {dealer_value}\n")
    
    round_winner = max((p for p in players if values[p] <= 21), key=lambda p: values[p], default=None)
    if dealer_value > 21 or (round_winner and values[round_winner] > dealer_value):
        print(f"{round_winner} wins!")
        return round_winner
    else:
        print("Dealer wins!")
        return "Dealer"

def blackjack():
    while True:
        try:
            num_players = int(input("Quanti giocatori siedono al tavolo? (1-4): "))
            if 1 <= num_players <= 4:
                break
        except ValueError:
            pass
        print("Scelta non valida, inserisci un numero tra 1 e 4.")
    
    players = [f"Player {i+1}" for i in range(num_players)]
    players.append("Dealer")
    
    while True:
        best_of = input("Vuoi giocare al meglio di 3 o 5? (3/5): ")
        if best_of in ["3", "5"]:
            best_of = int(best_of)
            break
        print("Scelta non valida, inserisci 3 o 5.")
    
    scores = {player: 0 for player in players}
    required_wins = (best_of // 2) + 1
    
    while max(scores.values()) < required_wins:
        winner = play_round(players[:-1])
        if winner:
            scores[winner] += 1
        
        print("Punteggio attuale:")
        for player, score in scores.items():
            print(f"{player} - {score}")
    
    overall_winner = max(scores, key=scores.get)
    print(f"{overall_winner} ha vinto il match al meglio di {best_of}!")

# Avvia il gioco
blackjack()
