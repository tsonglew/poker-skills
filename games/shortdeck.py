#!/usr/bin/env python3
"""Short Deck Hold'em (6+) - Texas Hold'em with 2-5 removed."""

import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i+6 for i, r in enumerate(RANKS)}

def create_deck():
    """36-card deck (2-5 removed)."""
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def hand_rank(hole, community):
    """Evaluate best 5-card hand."""
    from itertools import combinations
    all_cards = hole + community
    
    best = None
    for combo in combinations(all_cards, 5):
        rank = evaluate_hand(list(combo))
        if best is None or rank > best:
            best = rank
    return best

def evaluate_hand(cards):
    """Evaluate 5-card hand (short deck rules)."""
    ranks = sorted([RANK_VALUES[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    
    flush = len(set(suits)) == 1
    unique = sorted(set(ranks), reverse=True)
    
    # In short deck, A-6-7-8-9 is a straight (not A-5-6-7-8)
    straight = False
    if len(unique) == 5:
        if unique[0] - unique[4] == 4:
            straight = True
        # Wheel: A-6-7-8-9
        if unique == [14, 9, 8, 7, 6]:
            straight = True
    
    count = {}
    for r in ranks:
        count[r] = count.get(r, 0) + 1
    counts = sorted(count.values(), reverse=True)
    
    # Short deck: Flush beats Full House
    if straight and flush:
        return (9, max(ranks), "Straight Flush")
    if counts == [4, 1]:
        return (8, max(count, key=count.get), "Four of a Kind")
    if flush:
        return (7, max(ranks), "Flush")
    if counts == [3, 2]:
        return (6, max(count, key=count.get), "Full House")
    if straight:
        return (5, max(ranks), "Straight")
    if counts == [3, 1, 1]:
        return (4, max(count, key=count.get), "Three of a Kind")
    if counts == [2, 2, 1]:
        return (3, max(count, key=count.get), "Two Pair")
    if counts == [2, 1, 1, 1]:
        return (2, max(count, key=count.get), "One Pair")
    return (1, max(ranks), "High Card")

class ShortDeckHoldem:
    def __init__(self):
        self.deck = []
        self.players = []
        self.community = []
        
    def deal(self, num_players=4):
        self.deck = create_deck()
        self.players = []
        self.community = []
        
        for i in range(num_players):
            player = {
                'name': f'Player {i+1}',
                'cards': [self.deck.pop() for _ in range(2)],
                'chips': 1000,
                'folded': False
            }
            self.players.append(player)
        
        self.players[0]['name'] = 'You'
        
        # Deal community
        for _ in range(5):
            self.community.append(self.deck.pop())
    
    def show_hands(self):
        for player in self.players:
            cards = ' '.join([card_str(c) for c in player['cards']])
            print(f"{player['name']}: {cards}")
            
            rank = hand_rank(player['cards'], self.community)
            print(f"  Best hand: {rank[2]}\n")
    
    def find_winner(self):
        best = None
        winner = None
        
        for player in self.players:
            if not player['folded']:
                rank = hand_rank(player['cards'], self.community)
                if best is None or rank > best:
                    best = rank
                    winner = player
        
        return winner, best

def main():
    print("\n" + "="*50)
    print("      🃏 SHORT DECK HOLD'EM (6+) 🃏")
    print("="*50)
    print("\nRules:")
    print("- 36-card deck (2-5 removed)")
    print("- Flush beats Full House")
    print("- A-6-7-8-9 is the lowest straight")
    print("- More action, bigger hands!\n")
    
    game = ShortDeckHoldem()
    game.deal(4)
    
    community = ' '.join([card_str(c) for c in game.community])
    print(f"Community: {community}\n")
    
    game.show_hands()
    
    winner, best = game.find_winner()
    print("="*50)
    print(f"🏆 {winner['name']} wins with {best[2]}!")
    print("="*50)

if __name__ == '__main__':
    main()
