#!/usr/bin/env python3
"""Let It Ride - Casino poker game."""

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
    """Evaluate final 5-card hand."""
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
        return (8, "Royal Flush" if max(ranks) == 14 else "Straight Flush")
    if counts == [4, 1]:
        return (7, "Four of a Kind")
    if counts == [3, 2]:
        return (6, "Full House")
    if flush:
        return (5, "Flush")
    if straight:
        return (4, "Straight")
    if counts == [3, 1, 1]:
        return (3, "Three of a Kind")
    if counts == [2, 2, 1]:
        return (2, "Two Pair")
    if counts == [2, 1, 1, 1]:
        return (1, "Pair of 10s+")
    
    # Check for pair of 10s or better
    for r, c in count.items():
        if c == 2 and r >= 10:
            return (1, "Pair of 10s+")
    
    return (0, "No qualifying hand")

def payout(rank):
    """Payout table."""
    payouts = {
        8: 1000,  # Royal Flush
        7: 50,    # Four of a Kind
        6: 11,    # Full House
        5: 8,     # Flush
        4: 6,     # Straight
        3: 3,     # Three of a Kind
        2: 2,     # Two Pair
        1: 1      # Pair of 10s+
    }
    return payouts.get(rank, 0)

class LetItRide:
    def __init__(self):
        self.deck = []
        self.player_cards = []
        self.community = []
        self.bets = [0, 0, 0]  # Three equal bets
        
    def deal(self, bet=10):
        self.deck = create_deck()
        self.player_cards = [self.deck.pop() for _ in range(3)]
        self.community = [self.deck.pop() for _ in range(2)]
        self.bets = [bet, bet, bet]
        
    def show_hand(self, show_community=0):
        cards = ' '.join([card_str(c) for c in self.player_cards])
        print(f"\nYour cards: {cards}")
        
        if show_community > 0:
            comm = ' '.join([card_str(c) for c in self.community[:show_community]])
            print(f"Community: {comm}")
    
    def play(self):
        print("\n=== First Decision ===")
        self.show_hand()
        print("\n[1] Let It Ride (keep all bets)")
        print("[2] Pull Bet (remove first bet)")
        print(">>> Auto: Let It Ride")
        
        print("\n=== Reveal First Community Card ===")
        self.show_hand(show_community=1)
        print("\n[1] Let It Ride")
        print("[2] Pull Bet")
        print(">>> Auto: Let It Ride")
        
        print("\n=== Reveal Second Community Card ===")
        self.show_hand(show_community=2)
        
        # Evaluate final hand
        all_cards = self.player_cards + self.community
        rank = hand_rank(all_cards)
        
        print(f"\nFinal hand: {rank[1]}")
        
        total_bet = sum(self.bets)
        pay = payout(rank[0])
        
        if pay > 0:
            win = total_bet * pay
            print(f"✓ You WIN! {pay}:1 = ${win}")
            return win
        else:
            print(f"✗ No win. You lose ${total_bet}")
            return -total_bet

def main():
    print("\n" + "="*50)
    print("          🎰 LET IT RIDE 🎰")
    print("="*50)
    print("\nRules:")
    print("- Place 3 equal bets")
    print("- Get 3 cards + 2 community")
    print("- After each card, pull or let ride")
    print("- Need pair of 10s+ to win\n")
    
    game = LetItRide()
    game.deal(bet=10)
    
    print("Bets: $10 x 3 = $30")
    result = game.play()
    
    print("\n" + "="*50)

if __name__ == '__main__':
    main()
