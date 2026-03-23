#!/usr/bin/env python3
"""Big Two (大老二) - Hong Kong card game."""

import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
RANK_VALUES = {r: i for i, r in enumerate(RANKS)}
SUIT_VALUES = {'♦': 0, '♣': 1, '♥': 2, '♠': 3}

def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def card_value(card):
    """Card value: rank first, then suit."""
    return (RANK_VALUES[card[0]], SUIT_VALUES[card[1]])

class BigTwo:
    def __init__(self):
        self.deck = []
        self.players = []
        self.current_player = 0
        self.last_play = None
        
    def deal(self, num_players=4):
        self.deck = create_deck()
        self.players = []
        
        for i in range(num_players):
            cards = [self.deck.pop() for _ in range(13)]
            cards.sort(key=card_value)
            player = {
                'name': f'Player {i+1}',
                'cards': cards
            }
            self.players.append(player)
        
        self.players[0]['name'] = 'You'
        
        # Find who has 3♦ (lowest card)
        for i, player in enumerate(self.players):
            if ('3', '♦') in player['cards']:
                self.current_player = i
                break
    
    def show_hand(self):
        print(f"\nYour cards:")
        for i, card in enumerate(self.players[0]['cards']):
            print(f"  [{i}] {card_str(card)}")
    
    def can_play(self, cards, last_play):
        """Check if cards can beat last play."""
        if last_play is None:
            return True
        
        if len(cards) != len(last_play):
            return False
        
        # Compare highest card
        max_card = max(cards, key=card_value)
        max_last = max(last_play, key=card_value)
        
        return card_value(max_card) > card_value(max_last)
    
    def auto_play(self, player_idx):
        """Simple AI."""
        player = self.players[player_idx]
        
        if self.last_play is None:
            if player['cards']:
                card = player['cards'].pop(0)
                self.last_play = [card]
                print(f"{player['name']}: {card_str(card)}")
                return [card]
        else:
            needed = len(self.last_play)
            if len(player['cards']) >= needed:
                for i in range(len(player['cards']) - needed + 1):
                    subset = player['cards'][i:i+needed]
                    if self.can_play(subset, self.last_play):
                        for c in subset:
                            player['cards'].remove(c)
                        self.last_play = subset
                        print(f"{player['name']}: {' '.join([card_str(c) for c in subset])}")
                        return subset
        
        print(f"{player['name']}: PASS")
        return None
    
    def play(self):
        passes = 0
        
        while True:
            player = self.players[self.current_player]
            
            if player['name'] == 'You':
                self.show_hand()
                print(">>> Auto-playing...")
            
            result = self.auto_play(self.current_player)
            
            if result:
                passes = 0
                if not player['cards']:
                    return player
            else:
                passes += 1
                if passes >= len(self.players) - 1:
                    self.last_play = None
                    passes = 0
            
            self.current_player = (self.current_player + 1) % len(self.players)

def main():
    print("\n" + "="*50)
    print("         🃏 BIG TWO (大老二) 🃏")
    print("="*50)
    print("\n规则:")
    print("- 4人游戏，每人13张牌")
    print("- 3♦先出")
    print("- 牌序: 3<4<...<A<2")
    print("- 花色: ♦<♣<♥<♠")
    print("- 先出完牌者获胜\n")
    
    game = BigTwo()
    game.deal(4)
    
    winner = game.play()
    
    print("\n" + "="*50)
    print(f"🏆 {winner['name']} WINS!")
    print("="*50)

if __name__ == '__main__':
    main()
