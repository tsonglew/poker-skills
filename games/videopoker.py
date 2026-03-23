#!/usr/bin/env python3
"""Video Poker - Single player poker machine."""

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
        if max(ranks) == 14 and min(ranks) == 10:
            return (9, "Royal Flush")
        return (8, "Straight Flush")
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
        pair_val = [r for r, c in count.items() if c == 2][0]
        if pair_val >= 11:  # Jacks or better
            return (1, "Jacks or Better")
    return (0, "No Win")

def payout(rank, bet):
    """Payout table (Jacks or Better)."""
    payouts = {
        9: 800,  # Royal Flush
        8: 50,   # Straight Flush
        7: 25,   # Four of a Kind
        6: 9,    # Full House
        5: 6,    # Flush
        4: 4,    # Straight
        3: 3,    # Three of a Kind
        2: 2,    # Two Pair
        1: 1     # Jacks or Better
    }
    return payouts.get(rank, 0) * bet

class VideoPoker:
    def __init__(self):
        self.deck = []
        self.hand = []
        self.credits = 1000
        
    def deal(self, bet=5):
        self.deck = create_deck()
        self.hand = [self.deck.pop() for _ in range(5)]
        self.bet = bet
        
    def show_hand(self):
        for i, card in enumerate(self.hand):
            print(f"  [{i}] {card_str(card)}")
        
        rank = hand_rank(self.hand)
        print(f"\nCurrent: {rank[1]}")
    
    def draw(self, keep):
        """Replace cards not in keep list."""
        for i in range(5):
            if i not in keep:
                self.hand[i] = self.deck.pop()
    
    def play_round(self, bet=5):
        print(f"\n{'='*50}")
        print(f"CREDITS: ${self.credits}  |  BET: ${bet}")
        print('='*50)
        
        self.deal(bet)
        self.show_hand()
        
        print("\nSelect cards to KEEP (0-4), or 'all' to keep all:")
        print(">>> Auto: Keeping best cards...")
        
        # Simple auto-strategy: keep pairs and better
        keep = []
        rank = hand_rank(self.hand)
        
        if rank[0] >= 1:  # Already have a winning hand
            # Keep all winning cards
            count = {}
            for i, card in enumerate(self.hand):
                r = card[0]
                if r not in count:
                    count[r] = []
                count[r].append(i)
            
            for r, indices in count.items():
                if len(indices) >= 2:
                    keep.extend(indices)
        
        if not keep:
            # Keep high cards
            for i, card in enumerate(self.hand):
                if RANK_VALUES[card[0]] >= 12:  # Q or higher
                    keep.append(i)
        
        keep = list(set(keep))
        print(f"Keeping: {keep}")
        
        self.draw(keep)
        
        print("\n--- DRAW ---")
        self.show_hand()
        
        final_rank = hand_rank(self.hand)
        win = payout(final_rank[0], bet)
        
        if win > 0:
            self.credits += win
            print(f"\n✓ WIN ${win}!")
        else:
            self.credits -= bet
            print(f"\n✗ No win")
        
        print(f"Credits: ${self.credits}")

def main():
    print("\n" + "="*50)
    print("         📺 VIDEO POKER 📺")
    print("="*50)
    print("\nJacks or Better:")
    print("- Get 5 cards")
    print("- Keep any cards")
    print("- Draw new cards")
    print("- Need Jacks or Better to win\n")
    
    game = VideoPoker()
    
    # Play 3 rounds
    for _ in range(3):
        game.play_round(5)
    
    print("\n" + "="*50)

if __name__ == '__main__':
    main()
