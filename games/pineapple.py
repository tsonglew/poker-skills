#!/usr/bin/env python3
"""Pineapple Poker - Similar to Hold'em but with 3 cards, discard 1."""

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

def hand_rank(hole, community):
    """Evaluate best 5-card hand from 2 hole + 5 community."""
    from itertools import combinations
    all_cards = hole + community
    
    best = None
    for combo in combinations(all_cards, 5):
        rank = evaluate_hand(list(combo))
        if best is None or rank > best:
            best = rank
    return best

def evaluate_hand(cards):
    """Evaluate 5-card hand strength."""
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
            ranks = [5, 4, 3, 2, 1]
    
    count = {}
    for r in ranks:
        count[r] = count.get(r, 0) + 1
    counts = sorted(count.values(), reverse=True)
    
    if straight and flush:
        return (8, max(ranks), "Straight Flush")
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
        return (1, max(count, key=count.get), "One Pair")
    return (0, max(ranks), "High Card")

class PineappleGame:
    def __init__(self):
        self.deck = []
        self.players = []
        self.community = []
        self.pot = 0
        
    def deal(self, num_players=4):
        self.deck = create_deck()
        self.players = []
        self.community = []
        
        # Deal 3 cards to each player
        for i in range(num_players):
            player = {
                'name': f'Player {i+1}',
                'cards': [],
                'discarded': None,
                'chips': 1000,
                'folded': False
            }
            for _ in range(3):
                player['cards'].append(self.deck.pop())
            self.players.append(player)
        
        self.players[0]['name'] = 'You'
        
        # Auto-discard worst card for AI
        for player in self.players[1:]:
            # Simple: discard lowest card
            cards = player['cards']
            min_idx = min(range(3), key=lambda i: RANK_VALUES[cards[i][0]])
            player['discarded'] = cards.pop(min_idx)
        
        # Deal community cards
        for _ in range(5):
            self.community.append(self.deck.pop())
    
    def show_hand(self, player_idx=0):
        player = self.players[player_idx]
        cards = ' '.join([card_str(c) for c in player['cards']])
        print(f"\n{player['name']}'s hole cards: {cards}")
        
        if player['discarded']:
            print(f"Discarded: {card_str(player['discarded'])}")
        
        community = ' '.join([card_str(c) for c in self.community])
        print(f"Community: {community}")
        
        rank = hand_rank(player['cards'], self.community)
        print(f"Best hand: {rank[2]}")
    
    def evaluate_winner(self):
        best = None
        winner = None
        
        for player in self.players:
            if not player['folded']:
                rank = hand_rank(player['cards'], self.community)
                if best is None or rank > best:
                    best = rank
                    winner = player
        
        if winner:
            print(f"\n🏆 {winner['name']} wins with {best[2]}!")
            return winner
        return None

def main():
    print("\n" + "="*50)
    print("           🍍 PINEAPPLE POKER 🍍")
    print("="*50)
    print("\nSimilar to Texas Hold'em, but:")
    print("- You get 3 hole cards (not 2)")
    print("- You must discard 1 card before the flop")
    print("- Use your 2 remaining cards + 5 community cards\n")
    
    game = PineappleGame()
    game.deal(4)
    
    # Show your cards before discard
    print("\nYour 3 cards:")
    for i, card in enumerate(game.players[0]['cards']):
        print(f"  [{i}] {card_str(card)}")
    
    # For demo, auto-discard lowest
    cards = game.players[0]['cards']
    min_idx = min(range(3), key=lambda i: RANK_VALUES[cards[i][0]])
    game.players[0]['discarded'] = cards.pop(min_idx)
    print(f"\nAuto-discarded: {card_str(game.players[0]['discarded'])}")
    
    # Show all hands
    for i in range(len(game.players)):
        game.show_hand(i)
    
    # Determine winner
    game.evaluate_winner()

if __name__ == '__main__':
    main()
