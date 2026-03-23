#!/usr/bin/env python3
"""Casino War - Simplest card game."""

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

class CasinoWar:
    def __init__(self):
        self.deck = []
        self.chips = 1000
        
    def play_round(self, bet=10):
        if len(self.deck) < 10:
            self.deck = create_deck()
        
        player_card = self.deck.pop()
        dealer_card = self.deck.pop()
        
        player_val = RANK_VALUES[player_card[0]]
        dealer_val = RANK_VALUES[dealer_card[0]]
        
        print(f"\nYour card: {card_str(player_card)}")
        print(f"Dealer's card: {card_str(dealer_card)}")
        
        if player_val > dealer_val:
            print(f"✓ You WIN ${bet}!")
            return bet
        elif player_val < dealer_val:
            print(f"✗ You LOSE ${bet}")
            return -bet
        else:
            print("⚔️  WAR! Cards are equal!")
            print("\nOptions:")
            print("  [S] Surrender (lose half bet)")
            print("  [G] Go to War (double bet)")
            
            # Auto go to war for demo
            print("\n>>> Auto-going to WAR...")
            return self.go_to_war(bet)
    
    def go_to_war(self, original_bet):
        # Burn 3 cards each
        for _ in range(3):
            if self.deck:
                self.deck.pop()
            if self.deck:
                self.deck.pop()
        
        # New cards
        player_card = self.deck.pop()
        dealer_card = self.deck.pop()
        
        print(f"\nWar card - You: {card_str(player_card)}")
        print(f"War card - Dealer: {card_str(dealer_card)}")
        
        player_val = RANK_VALUES[player_card[0]]
        dealer_val = RANK_VALUES[dealer_card[0]]
        
        if player_val >= dealer_val:
            # Win original bet (not the war bet)
            print(f"✓ You WIN the war! +${original_bet}")
            return original_bet
        else:
            print(f"✗ You LOSE the war! -${original_bet * 2}")
            return -original_bet * 2

def main():
    print("\n" + "="*50)
    print("            ⚔️  CASINO WAR ⚔️")
    print("="*50)
    print("\nSimplest card game:")
    print("- Higher card wins")
    print("- Tie = WAR (double or surrender)")
    print("- Win war = win original bet\n")
    
    game = CasinoWar()
    
    # Play 3 rounds for demo
    for i in range(3):
        print(f"\n--- Round {i+1} ---")
        result = game.play_round(10)
        game.chips += result
        print(f"Chips: ${game.chips}")
    
    print("\n" + "="*50)

if __name__ == '__main__':
    main()
