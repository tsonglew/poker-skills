#!/usr/bin/env python3
"""跑得快 (Pao De Kuai) - Get rid of all cards first."""

import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
RANK_VALUES = {r: i for i, r in enumerate(RANKS)}

def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def card_str(card):
    return f"{card[0]}{card[1]}"

def rank_value(card):
    return RANK_VALUES[card[0]]

class PaoDeKuai:
    def __init__(self):
        self.deck = []
        self.players = []
        self.current_player = 0
        self.last_play = None
        self.passes = 0
        
    def deal(self, num_players=3):
        self.deck = create_deck()
        self.players = []
        
        for i in range(num_players):
            cards = [self.deck.pop() for _ in range(17)]
            cards.sort(key=rank_value)
            player = {
                'name': f'Player {i+1}',
                'cards': cards,
                'passed': False
            }
            self.players.append(player)
        
        self.players[0]['name'] = 'You'
        
        # Find who has 3♠
        for i, player in enumerate(self.players):
            if ('3', '♠') in player['cards']:
                self.current_player = i
                break
    
    def show_hand(self):
        print(f"\nYour cards ({len(self.players[0]['cards'])} left):")
        for i, card in enumerate(self.players[0]['cards']):
            print(f"  [{i}] {card_str(card)}")
    
    def can_play(self, cards, last_play):
        """Check if cards can beat last play."""
        if last_play is None:
            return True
        
        # Same number of cards
        if len(cards) != len(last_play):
            return False
        
        # Higher rank
        max_card = max(cards, key=rank_value)
        max_last = max(last_play, key=rank_value)
        
        return rank_value(max_card) > rank_value(max_last)
    
    def auto_play(self, player_idx):
        """Simple AI: play lowest valid cards."""
        player = self.players[player_idx]
        
        if self.last_play is None:
            # Lead with lowest card
            if player['cards']:
                card = player['cards'].pop(0)
                self.last_play = [card]
                print(f"{player['name']} plays: {card_str(card)}")
                return [card]
        else:
            # Try to beat last play
            needed = len(self.last_play)
            if len(player['cards']) >= needed:
                # Find cards that can beat
                for i in range(len(player['cards']) - needed + 1):
                    subset = player['cards'][i:i+needed]
                    if self.can_play(subset, self.last_play):
                        for c in subset:
                            player['cards'].remove(c)
                        self.last_play = subset
                        cards_str = ' '.join([card_str(c) for c in subset])
                        print(f"{player['name']} plays: {cards_str}")
                        return subset
        
        # Pass
        print(f"{player['name']} passes")
        player['passed'] = True
        return None
    
    def play_round(self):
        """Play one round until someone wins or all pass."""
        self.passes = 0
        
        while True:
            player = self.players[self.current_player]
            
            if player['name'] == 'You':
                self.show_hand()
                if self.last_play:
                    print(f"Last play: {' '.join([card_str(c) for c in self.last_play])}")
                
                # Auto-play for demo
                print("\n>>> Auto-playing...")
                result = self.auto_play(0)
            else:
                result = self.auto_play(self.current_player)
            
            if result:
                self.passes = 0
                # Reset passes for others
                for p in self.players:
                    if p != player:
                        p['passed'] = False
                
                # Check win
                if not player['cards']:
                    return player
            else:
                self.passes += 1
                if self.passes >= len(self.players) - 1:
                    # All others passed, clear last play
                    self.last_play = None
                    self.passes = 0
            
            # Next player
            self.current_player = (self.current_player + 1) % len(self.players)

def main():
    print("\n" + "="*50)
    print("        🃏 跑得快 (PAO DE KUAI) 🃏")
    print("="*50)
    print("\n规则:")
    print("- 3人游戏，每人17张牌")
    print("- 3♠先出")
    print("- 先出完牌者获胜")
    print("- 必须跟牌（同数量，更大）\n")
    
    game = PaoDeKuai()
    game.deal(3)
    
    print("Starting player has 3♠")
    
    winner = game.play_round()
    
    print("\n" + "="*50)
    print(f"🏆 {winner['name']} WINS!")
    print("="*50)

if __name__ == '__main__':
    main()
