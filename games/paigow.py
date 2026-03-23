#!/usr/bin/env python3
"""Pai Gow Poker - Chinese domino game adapted to cards."""

import random
from itertools import combinations

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i+2 for i, r in enumerate(RANKS)}

def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    # Add joker
    deck.append(('Joker', '🃏'))
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def rank_value(card):
    if card[0] == 'Joker':
        return 15  # Joker is highest
    return RANK_VALUES[card[0]]

def hand_rank_2(cards):
    """Rank 2-card hand (low hand)."""
    if len(cards) != 2:
        return None
    
    vals = sorted([rank_value(c) for c in cards])
    
    # Pair
    if vals[0] == vals[1]:
        return (2, vals[0])
    
    # High card
    return (1, vals[1], vals[0])

def hand_rank_5(cards):
    """Rank 5-card hand (high hand)."""
    vals = sorted([rank_value(c) for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    
    flush = len(set(suits)) == 1
    unique = sorted(set(vals), reverse=True)
    
    straight = False
    if len(unique) == 5:
        if unique[0] - unique[4] == 4:
            straight = True
    
    count = {}
    for v in vals:
        count[v] = count.get(v, 0) + 1
    counts = sorted(count.values(), reverse=True)
    
    if straight and flush:
        return (7, max(vals))
    if counts == [4, 1]:
        return (6, max(count, key=count.get))
    if counts == [3, 2]:
        return (5, max(count, key=count.get))
    if flush:
        return (4, max(vals))
    if straight:
        return (3, max(vals))
    if counts == [3, 1, 1]:
        return (2, max(count, key=count.get))
    if counts == [2, 2, 1]:
        return (1, max(count, key=count.get))
    if counts == [2, 1, 1, 1]:
        return (0, max(count, key=count.get))
    return (-1, max(vals))

class PaiGowPoker:
    def __init__(self):
        self.deck = []
        self.player_cards = []
        self.dealer_cards = []
        self.player_high = []
        self.player_low = []
        self.dealer_high = []
        self.dealer_low = []
        
    def deal(self):
        self.deck = create_deck()
        # Deal 7 cards each
        self.player_cards = [self.deck.pop() for _ in range(7)]
        self.dealer_cards = [self.deck.pop() for _ in range(7)]
        
    def show_hand(self):
        cards = ' '.join([card_str(c) for c in self.player_cards])
        print(f"\nYour 7 cards: {cards}")
        
    def set_hands_auto(self):
        """Auto-arrange hands (simple: put highest 2 in low hand)."""
        sorted_cards = sorted(self.player_cards, key=rank_value, reverse=True)
        self.player_low = sorted_cards[:2]
        self.player_high = sorted_cards[2:]
        
        sorted_dealer = sorted(self.dealer_cards, key=rank_value, reverse=True)
        self.dealer_low = sorted_dealer[:2]
        self.dealer_high = sorted_dealer[2:]
    
    def compare_hands(self):
        """Compare both hands."""
        low_rank_p = hand_rank_2(self.player_low)
        low_rank_d = hand_rank_2(self.dealer_low)
        high_rank_p = hand_rank_5(self.player_high)
        high_rank_d = hand_rank_5(self.dealer_high)
        
        print("\n--- Low Hand (2 cards) ---")
        print(f"You: {' '.join([card_str(c) for c in self.player_low])}")
        print(f"Dealer: {' '.join([card_str(c) for c in self.dealer_low])}")
        
        print("\n--- High Hand (5 cards) ---")
        print(f"You: {' '.join([card_str(c) for c in self.player_high])}")
        print(f"Dealer: {' '.join([card_str(c) for c in self.dealer_high])}")
        
        wins = 0
        if low_rank_p > low_rank_d:
            print("\n✓ You win low hand")
            wins += 1
        elif low_rank_p < low_rank_d:
            print("\n✗ Dealer wins low hand")
            wins -= 1
        else:
            print("\n= Low hand tie (dealer wins)")
            wins -= 1
        
        if high_rank_p > high_rank_d:
            print("✓ You win high hand")
            wins += 1
        elif high_rank_p < high_rank_d:
            print("✗ Dealer wins high hand")
            wins -= 1
        else:
            print("= High hand tie (dealer wins)")
            wins -= 1
        
        return wins

def main():
    print("\n" + "="*50)
    print("         🀄 PAI GOW POKER 🀄")
    print("="*50)
    print("\nRules:")
    print("- Get 7 cards")
    print("- Split into 5-card (high) + 2-card (low)")
    print("- High hand must beat low hand")
    print("- Win both to win, tie goes to dealer\n")
    
    game = PaiGowPoker()
    game.deal()
    game.show_hand()
    
    print("\n>>> Auto-arranging hands...")
    game.set_hands_auto()
    
    print("\n" + "="*50)
    result = game.compare_hands()
    
    if result > 0:
        print("\n🏆 You WIN!")
    elif result < 0:
        print("\n💀 Dealer WINS")
    else:
        print("\n🤝 TIE (dealer wins)")
    
    print("="*50)

if __name__ == '__main__':
    main()
