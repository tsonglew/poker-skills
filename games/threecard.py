#!/usr/bin/env python3
"""Three Card Poker - Casino table game."""

import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i+2 for i, r in enumerate(RANKS)}

def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def hand_rank_3(cards):
    """Evaluate 3-card hand."""
    ranks = sorted([RANK_VALUES[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    
    flush = len(set(suits)) == 1
    unique = sorted(set(ranks), reverse=True)
    
    # Straight (including A-2-3)
    straight = False
    if len(unique) == 3:
        if unique[0] - unique[2] == 2:
            straight = True
        if unique == [14, 3, 2]:  # A-2-3
            straight = True
    
    # Three of a kind
    if len(unique) == 1:
        return (6, ranks[0], "Three of a Kind")
    
    # Straight flush
    if straight and flush:
        return (5, max(ranks), "Straight Flush")
    
    # Straight
    if straight:
        return (4, max(ranks), "Straight")
    
    # Flush
    if flush:
        return (3, max(ranks), "Flush")
    
    # Pair
    if len(unique) == 2:
        pair_val = [r for r in ranks if ranks.count(r) == 2][0]
        return (2, pair_val, "Pair")
    
    # High card
    return (1, max(ranks), "High Card")

class ThreeCardPoker:
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.pot = 0
        self.ante = 0
        self.play_bet = 0
        
    def deal(self, ante=10):
        self.deck = create_deck()
        self.player_hand = [self.deck.pop() for _ in range(3)]
        self.dealer_hand = [self.deck.pop() for _ in range(3)]
        self.ante = ante
        self.pot = ante * 2  # Ante + Play
        
    def show_hands(self, show_dealer=False):
        player_cards = ' '.join([card_str(c) for c in self.player_hand])
        print(f"\nYour hand: {player_cards}")
        print(f"Hand rank: {hand_rank_3(self.player_hand)[2]}")
        
        if show_dealer:
            dealer_cards = ' '.join([card_str(c) for c in self.dealer_hand])
            print(f"\nDealer's hand: {dealer_cards}")
            print(f"Dealer rank: {hand_rank_3(self.dealer_hand)[2]}")
    
    def dealer_qualifies(self):
        """Dealer needs Queen-high or better to qualify."""
        rank = hand_rank_3(self.dealer_hand)
        return rank[0] > 1 or (rank[0] == 1 and rank[1] >= 12)
    
    def play(self):
        player_rank = hand_rank_3(self.player_hand)
        dealer_rank = hand_rank_3(self.dealer_hand)
        
        print("\n" + "="*50)
        
        if not self.dealer_qualifies():
            print("Dealer does not qualify (needs Queen-high)")
            print(f"You win ante: ${self.ante}")
            print(f"Play bet is pushed: ${self.ante}")
            return self.ante * 2
        
        # Compare hands
        if player_rank > dealer_rank:
            print(f"You win! {player_rank[2]} beats {dealer_rank[2]}")
            print(f"You win: ${self.ante * 2}")
            return self.ante * 2
        elif player_rank < dealer_rank:
            print(f"Dealer wins! {dealer_rank[2]} beats {player_rank[2]}")
            print(f"You lose: ${self.ante * 2}")
            return -self.ante * 2
        else:
            print("Push! Hands are equal")
            return 0

def main():
    print("\n" + "="*50)
    print("         🃏 THREE CARD POKER 🃏")
    print("="*50)
    print("\nRules:")
    print("- Place ante bet")
    print("- Get 3 cards")
    print("- Fold or Play (match ante)")
    print("- Dealer needs Queen-high to qualify")
    print("- Beat dealer to win\n")
    
    game = ThreeCardPoker()
    game.deal(ante=10)
    
    print(f"Ante: $10")
    game.show_hands()
    
    print("\nOptions:")
    print("  [P] Play (match ante $10)")
    print("  [F] Fold (lose ante)")
    
    # Auto-play for demo
    print("\n>>> Auto-playing...")
    print("You choose to PLAY ($10)")
    
    result = game.play()
    game.show_hands(show_dealer=True)
    
    print("\n" + "="*50)

if __name__ == '__main__':
    main()
