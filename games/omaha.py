"""
Omaha Hold'em poker game.

Similar to Texas Hold'em but players get 4 hole cards
and must use exactly 2 from hand + 3 from board.

Usage:
    python games/omaha.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from itertools import combinations
from lib.cards import Deck, Card
from lib.hands import evaluate_hand, HandRank


@dataclass
class Player:
    """Omaha player state."""
    id: int
    name: str
    chips: int = 1000
    hole_cards: List[Card] = field(default_factory=list)
    bet: int = 0
    folded: bool = False
    is_all_in: bool = False


@dataclass
class OmahaGame:
    """Omaha Hold'em game state."""
    deck: Deck = field(default_factory=Deck)
    players: List[Player] = field(default_factory=list)
    community_cards: List[Card] = field(default_factory=list)
    pot: int = 0
    current_bet: int = 0
    current_player_idx: int = 0
    dealer_idx: int = 0
    phase: str = "waiting"  # waiting, preflop, flop, turn, river, showdown
    small_blind: int = 5
    big_blind: int = 10
    
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
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.phase = "preflop"
        
        # Reset players
        active = [p for p in self.players if p.chips > 0]
        if len(active) < 2:
            return "Not enough players with chips!"
        
        for p in self.players:
            p.hole_cards = []
            p.bet = 0
            p.folded = False
            p.is_all_in = False
        
        # Move dealer
        self.dealer_idx = (self.dealer_idx + 1) % len(self.players)
        
        # Post blinds
        sb_idx = (self.dealer_idx + 1) % len(self.players)
        bb_idx = (self.dealer_idx + 2) % len(self.players)
        
        self._post_blind(sb_idx, self.small_blind)
        self._post_blind(bb_idx, self.big_blind)
        self.current_bet = self.big_blind
        
        # Deal 4 hole cards to each player
        for _ in range(4):
            for p in self.players:
                if p.chips > 0 or p.bet > 0:
                    p.hole_cards.append(self.deck.deal_one())
        
        # First to act is after BB
        self.current_player_idx = (bb_idx + 1) % len(self.players)
        self._skip_folded_players()
        
        return self._render()
    
    def _post_blind(self, player_idx: int, amount: int):
        """Post a blind."""
        player = self.players[player_idx]
        actual = min(amount, player.chips)
        player.chips -= actual
        player.bet = actual
        self.pot += actual
    
    def _skip_folded_players(self):
        """Skip folded/all-in players."""
        start = self.current_player_idx
        while self.players[self.current_player_idx].folded or self.players[self.current_player_idx].is_all_in:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            if self.current_player_idx == start:
                break
    
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
        """Check (pass action)."""
        return self._next_action()
    
    def raise_bet(self, amount: int) -> str:
        """Raise the bet."""
        player = self.players[self.current_player_idx]
        to_call = self.current_bet - player.bet
        total = to_call + amount
        
        if total > player.chips:
            total = player.chips
            amount = total - to_call
        
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
        
        # Check if only one player left
        active = [p for p in self.players if not p.folded]
        if len(active) == 1:
            self.pot = 0
            for p in self.players:
                p.bet = 0
            self.phase = "waiting"
            return self._render() + f"\n\n{active[0].name} wins the pot!"
        
        return self._next_action()
    
    def _next_action(self) -> str:
        """Move to next action."""
        # Check if betting round complete
        active_players = [p for p in self.players if not p.folded and not p.is_all_in]
        all_matched = all(p.bet == self.current_bet for p in active_players)
        
        if all_matched and active_players:
            # Move to next phase
            return self._next_phase()
        
        # Next player
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self._skip_folded_players()
        
        return self._render()
    
    def _next_phase(self) -> str:
        """Move to next betting phase."""
        # Reset bets for new round
        for p in self.players:
            p.bet = 0
        self.current_bet = 0
        
        if self.phase == "preflop":
            # Deal flop
            self.phase = "flop"
            self.community_cards.extend(self.deck.deal(3))
        elif self.phase == "flop":
            # Deal turn
            self.phase = "turn"
            self.community_cards.append(self.deck.deal_one())
        elif self.phase == "turn":
            # Deal river
            self.phase = "river"
            self.community_cards.append(self.deck.deal_one())
        elif self.phase == "river":
            # Showdown
            return self._showdown()
        
        # First to act after dealer
        self.current_player_idx = (self.dealer_idx + 1) % len(self.players)
        self._skip_folded_players()
        
        return self._render()
    
    def _showdown(self) -> str:
        """Determine winner at showdown."""
        self.phase = "showdown"
        
        active_players = [p for p in self.players if not p.folded]
        results = []
        
        for player in active_players:
            # In Omaha, must use exactly 2 hole cards + 3 community cards
            best_hand = None
            for hole_combo in combinations(player.hole_cards, 2):
                for comm_combo in combinations(self.community_cards, 3):
                    five_cards = list(hole_combo) + list(comm_combo)
                    hand = evaluate_hand(five_cards)
                    if best_hand is None or hand > best_hand:
                        best_hand = hand
            
            results.append((player, best_hand))
        
        # Sort by hand strength
        results.sort(key=lambda x: x[1], reverse=True)
        winner = results[0][0]
        
        # Award pot
        winner.chips += self.pot
        pot = self.pot
        self.pot = 0
        
        output = self._render()
        output += f"\n\n🏆 {winner.name} wins ${pot} with {results[0][1]}!"
        
        for player, hand in results[1:]:
            output += f"\n   {player.name}: {hand}"
        
        self.phase = "waiting"
        return output
    
    def _render(self) -> str:
        """Render game state."""
        lines = [
            "╔════════════════════════════════════════════════════╗",
            "│              🃏 OMAHA HOLD'EM 🃏                   │",
            "╠════════════════════════════════════════════════════╣",
            f"│ Phase: {self.phase.upper():<10}  Pot: ${self.pot:<5}                  │",
        ]
        
        # Community cards
        if self.community_cards:
            comm_str = " ".join(str(c) for c in self.community_cards)
            lines.append(f"│ Board: {comm_str:<37} │")
        else:
            lines.append("│ Board: [waiting...]                               │")
        
        lines.append("╠════════════════════════════════════════════════════╣")
        
        for i, p in enumerate(self.players):
            marker = "→ " if i == self.current_player_idx and self.phase not in ["waiting", "showdown"] else "  "
            status = ""
            if p.folded:
                status = " [FOLDED]"
            elif p.is_all_in:
                status = " [ALL-IN]"
            
            if p.id == 0:  # Show player's cards
                cards_str = " ".join(str(c) for c in p.hole_cards) if p.hole_cards else "No cards"
            else:
                cards_str = "****" if p.hole_cards and not p.folded else "----"
            
            lines.append(f"│ {marker}{p.name:<8} ${p.chips:<5} [{cards_str:<11}]{status:<10} │")
        
        lines.append("╠════════════════════════════════════════════════════╣")
        
        if self.phase == "waiting":
            lines.append("│ Commands: deal | quit                             │")
        elif self.phase == "showdown":
            lines.append("│ Commands: deal | quit                             │")
        else:
            player = self.players[self.current_player_idx]
            to_call = self.current_bet - player.bet
            lines.append(f"│ To call: ${to_call:<3}  Current bet: ${self.current_bet:<3}             │")
            lines.append("│ Commands: call | check | raise [amt] | fold | quit │")
        
        lines.append("╚════════════════════════════════════════════════════╝")
        
        return "\n".join(lines)


def play_interactive():
    """Interactive Omaha game."""
    game = OmahaGame()
    
    print("\n🃏 Welcome to Omaha Hold'em! 🃏")
    print("You get 4 hole cards, must use exactly 2 + 3 from board.\n")
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
                amount = int(cmd[1]) if len(cmd) > 1 else game.big_blind
                print("\n" + game.raise_bet(amount))
            elif action == "fold":
                print("\n" + game.fold())
            elif action == "help":
                print("\nCommands: deal, call, check, raise [amt], fold, quit")
            else:
                print(f"Unknown command: {action}")
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    play_interactive()
