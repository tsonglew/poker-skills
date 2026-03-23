#!/usr/bin/env python3
"""Razz - Lowball poker game."""

import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
RANK_VALUES = {r: i+1 for i, r in enumerate(RANKS)}

def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def low_hand(cards):
    """Get best 5-card low hand (A is low)."""
    ranks = sorted([RANK_VALUES[c[0]] for c in cards])
    # Take 5 lowest unique ranks
    unique = []
    for r in ranks:
        if r not in unique:
            unique.append(r)
        if len(unique) == 5:
            break
    return unique if len(unique) == 5 else None

class RazzGame:
    def __init__(self):
        self.deck = []
        self.players = []
        self.pot = 0
        self.current_bet = 0
        
    def deal(self, num_players=4):
        self.deck = create_deck()
        self.players = []
        
        for i in range(num_players):
            player = {
                'name': f'Player {i+1}',
                'cards': [],
                'chips': 1000,
                'bet': 0,
                'folded': False
            }
            # Deal 7 cards
            for _ in range(7):
                player['cards'].append(self.deck.pop())
            self.players.append(player)
        
        self.players[0]['name'] = 'You'
        self.pot = 0
        
    def show_hand(self, player_idx=0):
        player = self.players[player_idx]
        cards = ' '.join([card_str(c) for c in player['cards']])
        print(f"\n{player['name']}'s cards: {cards}")
        low = low_hand(player['cards'])
        if low:
            print(f"Best low: {' '.join([RANKS[r-1] for r in low])}")
        
    def evaluate_winner(self):
        best_low = None
        winner = None
        
        for player in self.players:
            if not player['folded']:
                low = low_hand(player['cards'])
                if low:
                    if best_low is None or low < best_low:
                        best_low = low
                        winner = player
        
        if winner:
            low_str = ' '.join([RANKS[r-1] for r in best_low])
            print(f"\n🏆 {winner['name']} wins with low: {low_str}")
            return winner
        return None

def main():
    print("\n" + "="*50)
    print("            🃏 RAZZ (Lowball Poker) 🃏")
    print("="*50)
    print("\nGoal: Make the lowest 5-card hand")
    print("Aces are low, straights/flushes don't count against you\n")
    
    game = RazzGame()
    game.deal(4)
    
    # Show all hands
    for i in range(len(game.players)):
        game.show_hand(i)
    
    # Determine winner
    game.evaluate_winner()

if __name__ == '__main__':
    main()
