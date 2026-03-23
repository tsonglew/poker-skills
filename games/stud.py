"""
7-Card Stud poker game.

Classic stud poker with 3 down cards and 4 up cards.
No community cards - each player has their own board.

Usage:
    python games/stud.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from dataclasses import dataclass, field
from lib.cards import Deck, Card, Rank
from lib.hands import evaluate_hand


@dataclass
class Player:
    """Stud player state."""
    id: int
    name: str
    chips: int = 1000
    cards: List[Card] = field(default_factory=list)
    bet: int = 0
    folded: bool = False
    is_all_in: bool = False
    
    @property
    def up_cards(self) -> List[Card]:
        """Face-up cards (4th card onwards)."""
        return self.cards[3:] if len(self.cards) > 3 else []
    
    @property
    def door_card(self) -> Optional[Card]:
        """First up card (determines bring-in)."""
        return self.cards[3] if len(self.cards) > 3 else None


@dataclass
class StudGame:
    """7-Card Stud game state."""
    deck: Deck = field(default_factory=Deck)
    players: List[Player] = field(default_factory=list)
    pot: int = 0
    current_bet: int = 0
    current_player_idx: int = 0
    phase: str = "waiting"  # waiting, third, fourth, fifth, sixth, seventh, showdown
    ante: int = 1
    bring_in: int = 3
    small_bet: int = 5
    big_bet: int = 10
    
    def __post_init__(self):
        if not self.players:
            self.add_player("You")
            self.add_player("Alice")
            self.add_player("Bob")
            self.add_player("Charlie")
    
    def add_player(self, name: str) -> Player:
        """Add a player to the game."""
        player = Player(id=len(self.players), name=name)
        self.players.append(player)
        return player
    
    def start_hand(self) -> str:
        """Start a new hand."""
        if self.deck.cards_remaining() < 20:
            self.deck.reset()
        
        # Reset state
        self.pot = 0
        self.current_bet = 0
        self.phase = "third"
        
        # Reset players and collect ante
        active = [p for p in self.players if p.chips > self.ante]
        if len(active) < 2:
            return "Not enough players with chips!"
        
        for p in self.players:
            p.cards = []
            p.bet = 0
            p.folded = False
            p.is_all_in = False
            if p.chips > 0:
                ante = min(self.ante, p.chips)
                p.chips -= ante
                self.pot += ante
        
        # Deal 3 cards each (2 down, 1 up)
        for _ in range(2):
            for p in self.players:
                if not p.folded:
                    p.cards.append(self.deck.deal_one())
        
        # Third card (door card) face up
        for p in self.players:
            if not p.folded:
                p.cards.append(self.deck.deal_one())
        
        # Lowest door card brings it in
        self.current_player_idx = self._find_lowest_door()
        self._post_bring_in()
        
        return self._render()
    
    def _find_lowest_door(self) -> int:
        """Find player with lowest door card."""
        min_rank = 15
        min_idx = 0
        
        for i, p in enumerate(self.players):
            if not p.folded and p.door_card:
                if p.door_card.rank.value < min_rank:
                    min_rank = p.door_card.rank.value
                    min_idx = i
        
        return min_idx
    
    def _post_bring_in(self):
        """Post bring-in bet."""
        player = self.players[self.current_player_idx]
        amount = min(self.bring_in, player.chips)
        player.chips -= amount
        player.bet = amount
        self.pot += amount
        self.current_bet = amount
    
    def call(self) -> str:
        """Call the current bet."""
        player = self.players[self.current_player_idx]
        to_call = self.current_bet - player.bet
        
        if to_call <= 0:
            return self.check()
        
        actual = min(to_call, player.chips)
        player.chips -= actual
        player.bet += actual
        self.pot += actual
        
        if player.chips == 0:
            player.is_all_in = True
        
        return self._next_action()
    
    def check(self) -> str:
        """Check."""
        return self._next_action()
    
    def raise_bet(self, amount: int = None) -> str:
        """Raise the bet."""
        player = self.players[self.current_player_idx]
        
        # Determine bet size based on phase
        bet_size = self.small_bet if self.phase in ["third", "fourth"] else self.big_bet
        
        if amount is None:
            amount = bet_size
        
        to_call = self.current_bet - player.bet
        total = to_call + amount
        
        if total > player.chips:
            total = player.chips
        
        player.chips -= total
        player.bet += total
        self.pot += total
        self.current_bet = player.bet
        
        if player.chips == 0:
            player.is_all_in = True
        
        return self._next_action()
    
    def fold(self) -> str:
        """Fold the hand."""
        player = self.players[self.current_player_idx]
        player.folded = True
        
        active = [p for p in self.players if not p.folded]
        if len(active) == 1:
            active[0].chips += self.pot
            self.pot = 0
            self.phase = "waiting"
            return self._render() + f"\n\n{active[0].name} wins the pot!"
        
        return self._next_action()
    
    def _next_action(self) -> str:
        """Move to next action."""
        active_players = [p for p in self.players if not p.folded and not p.is_all_in]
        all_matched = all(p.bet == self.current_bet for p in active_players)
        
        if all_matched and active_players:
            return self._next_phase()
        
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self._skip_folded()
        
        return self._render()
    
    def _skip_folded(self):
        """Skip folded/all-in players."""
        start = self.current_player_idx
        while self.players[self.current_player_idx].folded or self.players[self.current_player_idx].is_all_in:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            if self.current_player_idx == start:
                break
    
    def _next_phase(self) -> str:
        """Move to next street."""
        for p in self.players:
            p.bet = 0
        self.current_bet = 0
        
        phases = ["third", "fourth", "fifth", "sixth", "seventh", "showdown"]
        current_idx = phases.index(self.phase)
        
        if current_idx < len(phases) - 2:
            self.phase = phases[current_idx + 1]
            
            # Deal next card face up (except 7th street is down)
            for p in self.players:
                if not p.folded:
                    card = self.deck.deal_one()
                    p.cards.append(card)
            
            # High hand showing acts first
            self.current_player_idx = self._find_highest_up()
            self._skip_folded()
            
            return self._render()
        else:
            return self._showdown()
    
    def _find_highest_up(self) -> int:
        """Find player with highest up cards."""
        best_idx = 0
        best_value = 0
        
        for i, p in enumerate(self.players):
            if not p.folded and p.up_cards:
                # Simple: highest single card showing
                max_card = max(c.rank.value for c in p.up_cards)
                if max_card > best_value:
                    best_value = max_card
                    best_idx = i
        
        return best_idx
    
    def _showdown(self) -> str:
        """Determine winner."""
        self.phase = "showdown"
        
        active = [p for p in self.players if not p.folded]
        results = []
        
        for p in active:
            if len(p.cards) >= 5:
                hand = evaluate_hand(p.cards)
                results.append((p, hand))
        
        results.sort(key=lambda x: x[1], reverse=True)
        winner = results[0][0]
        winner.chips += self.pot
        pot = self.pot
        self.pot = 0
        
        output = self._render()
        output += f"\n\n🏆 {winner.name} wins ${pot} with {results[0][1]}!"
        
        for p, hand in results[1:]:
            output += f"\n   {p.name}: {hand}"
        
        self.phase = "waiting"
        return output
    
    def _render(self) -> str:
        """Render game state."""
        lines = [
            "╔════════════════════════════════════════════════════╗",
            "│               🃏 7-CARD STUD 🃏                    │",
            "╠════════════════════════════════════════════════════╣",
            f"│ Street: {self.phase.upper():<10}  Pot: ${self.pot:<5}                   │",
            "╠════════════════════════════════════════════════════╣",
        ]
        
        for i, p in enumerate(self.players):
            marker = "→ " if i == self.current_player_idx and self.phase not in ["waiting", "showdown"] else "  "
            status = " [FOLDED]" if p.folded else (" [ALL-IN]" if p.is_all_in else "")
            
            if p.id == 0:
                # Show all cards for player
                down = " ".join(str(c) for c in p.cards[:3]) if len(p.cards) >= 3 else ""
                up = " ".join(str(c) for c in p.up_cards)
                cards_str = f"{down} | {up}" if up else down
            else:
                # Show only up cards for others
                up = " ".join(str(c) for c in p.up_cards)
                down = "***" * min(3, len(p.cards))
                cards_str = f"{down} | {up}" if up else down
            
            lines.append(f"│ {marker}{p.name:<8} ${p.chips:<5} {cards_str:<28}{status} │")
        
        lines.append("╠════════════════════════════════════════════════════╣")
        
        if self.phase == "waiting":
            lines.append("│ Commands: deal | quit                              │")
        else:
            player = self.players[self.current_player_idx]
            to_call = self.current_bet - player.bet
            lines.append(f"│ Bet: ${self.current_bet:<3}  To call: ${to_call:<3}                       │")
            lines.append("│ Commands: call | check | raise | fold | quit       │")
        
        lines.append("╚════════════════════════════════════════════════════╝")
        
        return "\n".join(lines)


def play_interactive():
    """Interactive 7-Card Stud game."""
    game = StudGame()
    
    print("\n🃏 Welcome to 7-Card Stud! 🃏")
    print("3 down cards, 4 up cards. Best 5-card hand wins.\n")
    print(game._render())
    
    while True:
        try:
            cmd = input("\n> ").strip().lower().split()
            if not cmd:
                continue
            
            action = cmd[0]
            
            if action in ["q", "quit", "exit"]:
                print("\nThanks for playing!")
                break
            elif action == "deal":
                print("\n" + game.start_hand())
            elif action == "call":
                print("\n" + game.call())
            elif action == "check":
                print("\n" + game.check())
            elif action == "raise":
                print("\n" + game.raise_bet())
            elif action == "fold":
                print("\n" + game.fold())
            elif action == "help":
                print("\nCommands: deal, call, check, raise, fold, quit")
            else:
                print(f"Unknown command: {action}")
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    play_interactive()
