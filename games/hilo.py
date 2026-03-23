#!/usr/bin/env python3
"""Hi-Lo - Simple guessing game."""

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

class HiLo:
    def __init__(self):
        self.deck = []
        self.current_card = None
        self.chips = 1000
        self.streak = 0
        
    def new_card(self):
        if not self.deck:
            self.deck = create_deck()
        return self.deck.pop()
    
    def play_round(self, bet=10):
        self.current_card = self.new_card()
        print(f"\nCurrent card: {card_str(self.current_card)}")
        print(f"Streak: {self.streak} | Chips: ${self.chips}")
        
        # Auto-guess for demo
        current_val = RANK_VALUES[self.current_card[0]]
        
        if current_val <= 7:
            guess = 'H'
            print(">>> Guessing: HIGHER")
        else:
            guess = 'L'
            print(">>> Guessing: LOWER")
        
        next_card = self.new_card()
        next_val = RANK_VALUES[next_card[0]]
        
        print(f"Next card: {card_str(next_card)}")
        
        if (guess == 'H' and next_val > current_val) or \
           (guess == 'L' and next_val < current_val):
            self.streak += 1
            win = bet * (2 ** self.streak)
            print(f"✓ Correct! Streak: {self.streak}")
            print(f"Win ${win} (2^{self.streak} x {bet})")
            
            print("\n[C] Collect | [R] Risk again")
            print(">>> Auto: Collecting")
            self.chips += win
            self.streak = 0
            return win
        else:
            print(f"✗ Wrong! Lose ${bet * (2 ** self.streak) if self.streak > 0 else bet}")
            self.chips -= bet
            self.streak = 0
            return -bet

def main():
    print("\n" + "="*50)
    print("             🎰 HI-LO 🎰")
    print("="*50)
    print("\n规则:")
    print("- 猜下一张牌比当前高还是低")
    print("- 连续猜对，奖金翻倍")
    print("- 随时可以收钱\n")
    
    game = HiLo()
    
    for i in range(5):
        print(f"\n--- Round {i+1} ---")
        game.play_round(10)
    
    print(f"\nFinal chips: ${game.chips}")
    print("="*50)

if __name__ == '__main__':
    main()
