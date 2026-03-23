#!/usr/bin/env python3
"""Chinese Poker (十三张) - Arrange 13 cards into 3 hands."""

import random
from itertools import combinations

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i+2 for i, r in enumerate(RANKS)}

def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def hand_rank_5(cards):
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

def hand_rank_3(cards):
    """Evaluate 3-card hand."""
    ranks = sorted([RANK_VALUES[c[0]] for c in cards], reverse=True)
    unique = sorted(set(ranks), reverse=True)
    
    if len(unique) == 1:
        return (3, ranks[0], "Three of a Kind")
    if len(unique) == 2:
        return (2, max(unique), "One Pair")
    return (1, max(ranks), "High Card")

class ChinesePoker:
    def __init__(self):
        self.deck = []
        self.players = []
        
    def deal(self, num_players=4):
        self.deck = create_deck()
        self.players = []
        
        for i in range(num_players):
            cards = [self.deck.pop() for _ in range(13)]
            player = {
                'name': f'Player {i+1}',
                'cards': cards,
                'back': [],    # 5 cards (strongest)
                'middle': [],  # 5 cards
                'front': []    # 3 cards (weakest)
            }
            self.players.append(player)
        
        self.players[0]['name'] = 'You'
    
    def arrange_auto(self, player):
        """Auto-arrange cards into 3 hands."""
        sorted_cards = sorted(player['cards'], key=lambda c: RANK_VALUES[c[0]], reverse=True)
        
        # Simple arrangement: first 5 = back, next 5 = middle, last 3 = front
        player['back'] = sorted_cards[:5]
        player['middle'] = sorted_cards[5:10]
        player['front'] = sorted_cards[10:13]
    
    def show_hands(self):
        for player in self.players:
            print(f"\n{player['name']}:")
            back_rank = hand_rank_5(player['back'])
            middle_rank = hand_rank_5(player['middle'])
            front_rank = hand_rank_3(player['front'])
            
            print(f"  Back (5): {' '.join([card_str(c) for c in player['back']])} - {back_rank[2]}")
            print(f"  Middle (5): {' '.join([card_str(c) for c in player['middle']])} - {middle_rank[2]}")
            print(f"  Front (3): {' '.join([card_str(c) for c in player['front']])} - {front_rank[2]}")
    
    def compare_players(self, p1, p2):
        """Compare two players, return p1's points."""
        points = 0
        
        # Back
        if hand_rank_5(p1['back']) > hand_rank_5(p2['back']):
            points += 1
        elif hand_rank_5(p1['back']) < hand_rank_5(p2['back']):
            points -= 1
        
        # Middle
        if hand_rank_5(p1['middle']) > hand_rank_5(p2['middle']):
            points += 1
        elif hand_rank_5(p1['middle']) < hand_rank_5(p2['middle']):
            points -= 1
        
        # Front
        if hand_rank_3(p1['front']) > hand_rank_3(p2['front']):
            points += 1
        elif hand_rank_3(p1['front']) < hand_rank_3(p2['front']):
            points -= 1
        
        return points
    
    def calculate_scores(self):
        """Calculate total scores."""
        scores = {p['name']: 0 for p in self.players}
        
        for i, p1 in enumerate(self.players):
            for j, p2 in enumerate(self.players):
                if i < j:
                    pts = self.compare_players(p1, p2)
                    scores[p1['name']] += pts
                    scores[p2['name']] -= pts
        
        return scores

def main():
    print("\n" + "="*50)
    print("        🇨🇳 CHINESE POKER (十三张) 🇨🇳")
    print("="*50)
    print("\nRules:")
    print("- Get 13 cards")
    print("- Arrange into 3 hands: Back (5) ≥ Middle (5) ≥ Front (3)")
    print("- Win points by beating opponents in each hand\n")
    
    game = ChinesePoker()
    game.deal(4)
    
    # Auto-arrange all hands
    for player in game.players:
        game.arrange_auto(player)
    
    # Show your cards first
    print("\nYour 13 cards:")
    print(' '.join([card_str(c) for c in game.players[0]['cards']]))
    
    print("\n>>> Auto-arranging...")
    game.show_hands()
    
    # Calculate scores
    print("\n" + "="*50)
    print("SCORES:")
    scores = game.calculate_scores()
    for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {score:+d}")
    
    print("="*50)

if __name__ == '__main__':
    main()
