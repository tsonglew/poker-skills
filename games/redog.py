#!/usr/bin/env python3
"""Red Dog - Simple casino card game."""

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

def spread(card1, card2):
    """Calculate spread between two cards."""
    val1 = RANK_VALUES[card1[0]]
    val2 = RANK_VALUES[card2[0]]
    
    diff = abs(val1 - val2) - 1  # -1 because consecutive = 0 spread
    return max(0, diff)

def payout(spread):
    """Payout based on spread."""
    if spread == 0:
        return 4  # Consecutive
    elif spread == 1:
        return 5
    elif spread == 2:
        return 4
    elif spread == 3:
        return 2
    elif spread == 4:
        return 2
    else:
        return 1  # 5+ spread

class RedDog:
    def __init__(self):
        self.deck = []
        self.chips = 1000
        
    def play_round(self, bet=10):
        if len(self.deck) < 10:
            self.deck = create_deck()
        
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        
        val1 = RANK_VALUES[card1[0]]
        val2 = RANK_VALUES[card2[0]]
        
        print(f"\nFirst card: {card_str(card1)}")
        print(f"Second card: {card_str(card2)}")
        
        # Pair
        if val1 == val2:
            print("\n Pair! Third card...")
            card3 = self.deck.pop()
            print(f"Third card: {card_str(card3)}")
            
            if RANK_VALUES[card3[0]] == val1:
                print(f"✓ Three of a kind! You win ${bet * 11}")
                return bet * 11
            else:
                print("✗ No match. Push.")
                return 0
        
        s = spread(card1, card2)
        
        if s == 0:
            print("\nConsecutive cards - Push!")
            return 0
        
        print(f"\nSpread: {s}")
        pay = payout(s)
        print(f"Payout: {pay}:1")
        print("\n[R] Raise (double bet)")
        print("[S] Stay (original bet)")
        
        # Auto-stay for demo
        print(">>> Auto: STAY")
        
        # Draw third card
        card3 = self.deck.pop()
        print(f"\nThird card: {card_str(card3)}")
        
        val3 = RANK_VALUES[card3[0]]
        min_val = min(val1, val2)
        max_val = max(val1, val2)
        
        if min_val < val3 < max_val:
            win = bet * pay
            print(f"✓ IN BETWEEN! You win ${win}")
            return win
        else:
            print(f"✗ OUTSIDE! You lose ${bet}")
            return -bet

def main():
    print("\n" + "="*50)
    print("            🐕 RED DOG 🐕")
    print("="*50)
    print("\nRules:")
    print("- Two cards are dealt")
    print("- Bet if third card falls between them")
    print("- Smaller spread = bigger payout")
    print("- Consecutive = push, Pair = 11:1\n")
    
    game = RedDog()
    
    # Play 3 rounds
    for i in range(3):
        print(f"\n--- Round {i+1} ---")
        result = game.play_round(10)
        game.chips += result
        print(f"Chips: ${game.chips}")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    main()
