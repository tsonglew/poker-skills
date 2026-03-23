#!/usr/bin/env python3
"""Caribbean Stud Poker - Casino table game."""

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

def hand_rank(cards):
    """Evaluate 5-card hand."""
    ranks = sorted([RANK_VALUES[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    
    flush = len(set(suits)) == 1
    unique = sorted(set(ranks), reverse=True)
    
    straight = False
    if len(unique) == 5:
        if unique[0] - unique[4] == 4:
            straight = True
        if unique == [14, 5, 4, 3, 2]:
            straight = True
    
    count = {}
    for r in ranks:
        count[r] = count.get(r, 0) + 1
    counts = sorted(count.values(), reverse=True)
    
    if straight and flush:
        return (8, max(ranks), "Royal Flush" if max(ranks) == 14 else "Straight Flush")
    if counts == [4, 1]:
        return (7, max(count, key=count.get), "Four of a Kind")
    if counts == [3, 2]:
        return (6, max(count, key=count.get), "Full House")
    if flush:
        return (5, max(ranks), "Flush")
    if straight:
        return (4, max(ranks), "Straight")
    if counts == [3, 1, 1]:
        return (3, max(count, key=count.get), "Three of a Kind")
    if counts == [2, 2, 1]:
        return (2, max(count, key=count.get), "Two Pair")
    if counts == [2, 1, 1, 1]:
        return (1, max(count, key=count.get), "Pair")
    return (0, max(ranks), "High Card")

class CaribbeanStud:
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        
    def deal(self, ante=10):
        self.deck = create_deck()
        self.player_hand = [self.deck.pop() for _ in range(5)]
        self.dealer_hand = [self.deck.pop() for _ in range(5)]
        self.ante = ante
        
    def show_hands(self, show_dealer=False):
        player_cards = ' '.join([card_str(c) for c in self.player_hand])
        print(f"\nYour hand: {player_cards}")
        print(f"Hand: {hand_rank(self.player_hand)[2]}")
        
        if show_dealer:
            dealer_cards = ' '.join([card_str(c) for c in self.dealer_hand])
            print(f"\nDealer's hand: {dealer_cards}")
            print(f"Dealer: {hand_rank(self.dealer_hand)[2]}")
    
    def dealer_qualifies(self):
        """Dealer needs Ace-King or better."""
        rank = hand_rank(self.dealer_hand)
        return rank[0] >= 1  # Pair or better
    
    def payout(self):
        """Calculate payout based on hand strength."""
        rank = hand_rank(self.player_hand)
        
        payouts = {
            0: 1,  # High card - 1:1
            1: 1,  # Pair - 1:1
            2: 2,  # Two pair - 2:1
            3: 3,  # Three of a kind - 3:1
            4: 4,  # Straight - 4:1
            5: 5,  # Flush - 5:1
            6: 7,  # Full house - 7:1
            7: 20, # Four of a kind - 20:1
            8: 50  # Straight flush - 50:1
        }
        
        return payouts.get(rank[0], 1)

def main():
    print("\n" + "="*50)
    print("        🏝️  CARIBBEAN STUD POKER 🏝️")
    print("="*50)
    print("\nRules:")
    print("- Place ante bet")
    print("- Get 5 cards, dealer shows 1")
    print("- Fold or Raise (2x ante)")
    print("- Dealer needs Ace-King to qualify")
    print("- Progressive payouts for strong hands\n")
    
    game = CaribbeanStud()
    game.deal(ante=10)
    
    print(f"Ante: $10")
    print("\nDealer shows one card:")
    print(f"  {card_str(game.dealer_hand[0])} ?? ?? ?? ??")
    
    game.show_hands()
    
    print("\nOptions:")
    print("  [R] Raise (2x ante = $20)")
    print("  [F] Fold (lose ante)")
    
    # Auto-play for demo
    print("\n>>> Auto-raising...")
    print("You RAISE $20")
    
    print("\n" + "="*50)
    game.show_hands(show_dealer=True)
    
    player_rank = hand_rank(game.player_hand)
    dealer_rank = hand_rank(game.dealer_hand)
    
    if not game.dealer_qualifies():
        print("\nDealer does not qualify!")
        print(f"You win ante: $10")
    elif player_rank > dealer_rank:
        payout = game.payout()
        win = 10 + (20 * payout)
        print(f"\n✓ You WIN! Payout {payout}:1 = ${win}")
    elif player_rank < dealer_rank:
        print(f"\n✗ Dealer wins. You lose $30")
    else:
        print("\nPush! Bet returned.")
    
    print("="*50)

if __name__ == '__main__':
    main()
