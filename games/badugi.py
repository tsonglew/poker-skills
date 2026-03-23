#!/usr/bin/env python3
"""Badugi - Korean lowball poker game."""

import random
from itertools import combinations

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
RANK_VALUES = {r: i+1 for i, r in enumerate(RANKS)}

def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def badugi_hand(cards):
    """Find best 4-card Badugi hand (all different suits and ranks)."""
    best = None
    
    for combo in combinations(cards, 4):
        ranks = [c[0] for c in combo]
        suits = [c[1] for c in combo]
        
        # All ranks and suits must be unique
        if len(set(ranks)) == 4 and len(set(suits)) == 4:
            rank_vals = sorted([RANK_VALUES[r] for r in ranks])
            if best is None or rank_vals < best:
                best = rank_vals
    
    return best

class BadugiGame:
    def __init__(self):
        self.deck = []
        self.players = []
        
    def deal(self, num_players=4):
        self.deck = create_deck()
        self.players = []
        
        for i in range(num_players):
            player = {
                'name': f'Player {i+1}',
                'cards': [],
                'chips': 1000,
                'folded': False
            }
            # Deal 4 cards
            for _ in range(4):
                player['cards'].append(self.deck.pop())
            self.players.append(player)
        
        self.players[0]['name'] = 'You'
        
    def show_hand(self, player_idx=0):
        player = self.players[player_idx]
        cards = ' '.join([card_str(c) for c in player['cards']])
        print(f"\n{player['name']}'s cards: {cards}")
        
        badugi = badugi_hand(player['cards'])
        if badugi:
            print(f"Badugi: {'-'.join([RANKS[v-1] for v in badugi])}")
        else:
            print("No Badugi (need 4 cards of different suits and ranks)")
    
    def evaluate_winner(self):
        best = None
        winner = None
        
        for player in self.players:
            if not player['folded']:
                bg = badugi_hand(player['cards'])
                if bg:
                    if best is None or bg < best:
                        best = bg
                        winner = player
        
        if winner:
            bg_str = '-'.join([RANKS[v-1] for v in best])
            print(f"\n🏆 {winner['name']} wins with Badugi: {bg_str}")
        else:
            print("\nNo one has a Badugi!")
            
        return winner

def main():
    print("\n" + "="*50)
    print("           🇰🇷 BADUGI (Korean Lowball) 🇰🇷")
    print("="*50)
    print("\nGoal: Make 4 cards with all different suits AND ranks")
    print("Lowest hand wins (A-2-3-4 is best)\n")
    
    game = BadugiGame()
    game.deal(4)
    
    # Show all hands
    for i in range(len(game.players)):
        game.show_hand(i)
    
    # Determine winner
    game.evaluate_winner()

if __name__ == '__main__':
    main()
