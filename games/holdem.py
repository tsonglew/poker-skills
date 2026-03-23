"""
Texas Hold'em poker game engine.

Usage:
    python -m games.holdem play
"""

import random
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.cards import Deck, Card, Rank, Suit, format_cards
from lib.hands import evaluate_hand, HandRank, EvaluatedHand


class Street(Enum):
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"


class PlayerAction(Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    RAISE = "raise"
    ALL_IN = "all-in"


@dataclass
class Player:
    name: str
    chips: int = 1000
    hole_cards: List[Card] = field(default_factory=list)
    current_bet: int = 0
    total_bet: int = 0
    is_folded: bool = False
    is_all_in: bool = False
    is_human: bool = False
    
    def reset_hand(self):
        self.hole_cards = []
        self.current_bet = 0
        self.total_bet = 0
        self.is_folded = False
        self.is_all_in = False
    
    @property
    def is_active(self) -> bool:
        return not self.is_folded and not self.is_all_in


@dataclass
class HoldemGame:
    """Texas Hold'em game state."""
    deck: Deck = field(default_factory=Deck)
    players: List[Player] = field(default_factory=list)
    community_cards: List[Card] = field(default_factory=list)
    pot: int = 0
    current_bet: int = 0
    min_raise: int = 0
    street: Street = Street.PREFLOP
    current_player_index: int = 0
    dealer_index: int = 0
    small_blind: int = 5
    big_blind: int = 10
    is_hand_over: bool = False
    message: str = ""
    last_action: str = ""
    
    def add_player(self, name: str, chips: int = 1000, is_human: bool = False):
        """Add a player to the game."""
        self.players.append(Player(name=name, chips=chips, is_human=is_human))
    
    def start_hand(self) -> str:
        """Start a new hand."""
        if len(self.players) < 2:
            return "Need at least 2 players to start."
        
        # Reset state
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.is_hand_over = False
        self.message = ""
        self.street = Street.PREFLOP
        
        # Reset players
        active_players = [p for p in self.players if p.chips > 0]
        if len(active_players) < 2:
            return "Not enough players with chips."
        
        for player in self.players:
            player.reset_hand()
        
        # Move dealer button
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        while self.players[self.dealer_index].chips <= 0:
            self.dealer_index = (self.dealer_index + 1) % len(self.players)
        
        # Post blinds
        sb_index = self._next_active_player(self.dealer_index)
        bb_index = self._next_active_player(sb_index)
        
        self._post_blind(sb_index, self.small_blind)
        self._post_blind(bb_index, self.big_blind)
        
        self.current_bet = self.big_blind
        self.min_raise = self.big_blind
        
        # Deal hole cards
        for _ in range(2):
            for player in self.players:
                if player.chips > 0 or player.total_bet > 0:
                    player.hole_cards.append(self.deck.deal_one())
        
        # Set first to act (after big blind)
        self.current_player_index = self._next_active_player(bb_index)
        
        return self._render()
    
    def _post_blind(self, player_index: int, amount: int):
        """Post a blind."""
        player = self.players[player_index]
        actual = min(amount, player.chips)
        player.chips -= actual
        player.current_bet = actual
        player.total_bet = actual
        self.pot += actual
    
    def _next_active_player(self, from_index: int) -> int:
        """Find next player who can still act."""
        index = (from_index + 1) % len(self.players)
        count = 0
        while count < len(self.players):
            player = self.players[index]
            if not player.is_folded and not player.is_all_in and player.chips > 0:
                return index
            index = (index + 1) % len(self.players)
            count += 1
        return from_index
    
    def fold(self) -> str:
        """Current player folds."""
        player = self.players[self.current_player_index]
        player.is_folded = True
        self.last_action = f"{player.name} folds"
        
        self._advance()
        return self._render()
    
    def check(self) -> str:
        """Current player checks."""
        player = self.players[self.current_player_index]
        
        if player.current_bet < self.current_bet:
            return f"Can't check - need to call {self.current_bet - player.current_bet} or fold."
        
        self.last_action = f"{player.name} checks"
        self._advance()
        return self._render()
    
    def call(self) -> str:
        """Current player calls."""
        player = self.players[self.current_player_index]
        to_call = self.current_bet - player.current_bet
        
        if to_call <= 0:
            return "Nothing to call - use check instead."
        
        if to_call >= player.chips:
            # All-in
            self.pot += player.chips
            player.total_bet += player.chips
            player.current_bet += player.chips
            player.chips = 0
            player.is_all_in = True
            self.last_action = f"{player.name} is ALL-IN for {player.total_bet}!"
        else:
            player.chips -= to_call
            player.current_bet = self.current_bet
            player.total_bet += to_call
            self.pot += to_call
            self.last_action = f"{player.name} calls {to_call}"
        
        self._advance()
        return self._render()
    
    def raise_bet(self, amount: int) -> str:
        """Current player raises."""
        player = self.players[self.current_player_index]
        
        to_call = self.current_bet - player.current_bet
        total_needed = to_call + amount
        
        if amount < self.min_raise and player.chips > total_needed:
            return f"Minimum raise is {self.min_raise}."
        
        if total_needed >= player.chips:
            # All-in
            all_in_amount = player.chips
            self.pot += all_in_amount
            player.total_bet += all_in_amount
            player.current_bet += all_in_amount
            player.chips = 0
            player.is_all_in = True
            self.last_action = f"{player.name} is ALL-IN!"
            self.current_bet = player.current_bet
        else:
            player.chips -= total_needed
            player.current_bet = self.current_bet + amount
            player.total_bet += total_needed
            self.pot += total_needed
            self.current_bet = player.current_bet
            self.min_raise = amount
            self.last_action = f"{player.name} raises to {self.current_bet}"
        
        self._advance()
        return self._render()
    
    def _advance(self):
        """Advance to next player or street."""
        # Check if only one player left
        active_players = [p for p in self.players if not p.is_folded]
        if len(active_players) == 1:
            self._award_pot(active_players[0])
            return
        
        # Check if betting round is complete
        active_betting = [p for p in self.players if p.is_active]
        all_matched = all(p.current_bet == self.current_bet for p in active_betting)
        
        if all_matched and len(active_betting) <= 1:
            self._next_street()
            return
        
        # Move to next player
        next_index = self._next_active_player(self.current_player_index)
        
        # Check if we've gone around
        if next_index == self.current_player_index:
            # Only one player can still act
            self._next_street()
        else:
            self.current_player_index = next_index
    
    def _next_street(self):
        """Advance to next street."""
        # Reset current bets
        for player in self.players:
            player.current_bet = 0
        self.current_bet = 0
        
        if self.street == Street.PREFLOP:
            self.street = Street.FLOP
            self.community_cards = self.deck.deal(3)
        elif self.street == Street.FLOP:
            self.street = Street.TURN
            self.community_cards.append(self.deck.deal_one())
        elif self.street == Street.TURN:
            self.street = Street.RIVER
            self.community_cards.append(self.deck.deal_one())
        elif self.street == Street.RIVER:
            self._showdown()
            return
        
        # First to act is after dealer
        self.current_player_index = self._next_active_player(self.dealer_index)
        self.message = f"\n*** {self.street.value.upper()} ***"
    
    def _showdown(self):
        """Determine winner at showdown."""
        self.street = Street.SHOWDOWN
        self.is_hand_over = True
        
        active_players = [p for p in self.players if not p.is_folded]
        
        # Evaluate hands
        results = []
        for player in active_players:
            all_cards = player.hole_cards + self.community_cards
            hand = evaluate_hand(all_cards)
            results.append((player, hand))
        
        # Sort by hand strength
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Find winner(s)
        winner = results[0]
        winners = [r for r in results if r[1] == winner[1]]
        
        # Split pot if tie
        share = self.pot // len(winners)
        for w_player, w_hand in winners:
            w_player.chips += share
        
        # Build message
        winner_names = ", ".join(w[0].name for w in winners)
        self.message = f"\n🏆 {winner_names} wins {self.pot} with {winner[1].name}!"
        
        # Show all hands
        self.message += "\n\nShowdown:"
        for player, hand in results:
            self.message += f"\n  {player.name}: {format_cards(player.hole_cards)} → {hand.name}"
    
    def _award_pot(self, player: Player):
        """Award pot to single winner."""
        player.chips += self.pot
        self.is_hand_over = True
        self.message = f"\n🏆 {player.name} wins {self.pot} chips!"
    
    def _render(self) -> str:
        """Render game state."""
        lines = [
            "",
            "═══════════════════════════════════════════════════",
            "              ♠ TEXAS HOLD'EM ♠",
            "═══════════════════════════════════════════════════",
            f"  Pot: {self.pot}  |  Street: {self.street.value.upper()}  |  Bet: {self.current_bet}",
            "───────────────────────────────────────────────────",
        ]
        
        # Community cards
        if self.community_cards:
            community = format_cards(self.community_cards)
            lines.append(f"  Board: {community}")
            lines.append("───────────────────────────────────────────────────")
        
        # Players
        for i, player in enumerate(self.players):
            marker = "→ " if i == self.current_player_index and not self.is_hand_over else "  "
            status = ""
            if player.is_folded:
                status = " [FOLDED]"
            elif player.is_all_in:
                status = " [ALL-IN]"
            
            cards = format_cards(player.hole_cards) if player.hole_cards else "??"
            if player.is_folded:
                cards = "--"
            
            lines.append(f"{marker}{player.name}: {cards} | {player.chips} chips{status}")
        
        lines.append("───────────────────────────────────────────────────")
        
        if self.last_action:
            lines.append(f"  Last: {self.last_action}")
        
        if self.message:
            lines.append(self.message)
        
        # Current player options
        if not self.is_hand_over:
            player = self.players[self.current_player_index]
            if player.is_human:
                to_call = self.current_bet - player.current_bet
                options = ["fold"]
                if to_call == 0:
                    options.append("check")
                else:
                    options.append(f"call ({to_call})")
                options.append("raise [amount]")
                lines.append(f"  Options: {', '.join(options)}")
        
        if self.is_hand_over:
            lines.append("  Type 'deal' for next hand")
        
        lines.append("═══════════════════════════════════════════════════")
        
        return "\n".join(lines)


def play_interactive():
    """Interactive Texas Hold'em game."""
    game = HoldemGame()
    
    print("\n♠♥♦♣ Welcome to Texas Hold'em! ♣♦♥♠\n")
    
    # Setup players
    game.add_player("You", 1000, is_human=True)
    game.add_player("Alice", 1000)
    game.add_player("Bob", 1000)
    game.add_player("Charlie", 1000)
    
    print("Players: You, Alice, Bob, Charlie")
    print(f"Blinds: {game.small_blind}/{game.big_blind}\n")
    
    print(game.start_hand())
    
    while True:
        try:
            current = game.players[game.current_player_index]
            
            # AI players act automatically
            if not current.is_human and not game.is_hand_over:
                import time
                time.sleep(0.5)
                
                to_call = game.current_bet - current.current_bet
                
                # Simple AI
                if to_call == 0:
                    if random.random() < 0.3:
                        game.raise_bet(game.big_blind * 2)
                    else:
                        game.check()
                elif to_call <= game.big_blind:
                    if random.random() < 0.7:
                        game.call()
                    else:
                        game.fold()
                else:
                    if random.random() < 0.5:
                        game.call()
                    else:
                        game.fold()
                
                print(game._render())
                continue
            
            cmd = input("\n> ").strip().lower().split()
            if not cmd:
                continue
            
            action = cmd[0]
            
            if action in ["q", "quit", "exit"]:
                print("\nFinal chip counts:")
                for p in game.players:
                    print(f"  {p.name}: {p.chips}")
                break
            elif action == "deal":
                print(game.start_hand())
            elif action == "fold":
                print(game.fold())
            elif action == "check":
                print(game.check())
            elif action == "call":
                print(game.call())
            elif action == "raise":
                amount = int(cmd[1]) if len(cmd) > 1 else game.big_blind * 2
                print(game.raise_bet(amount))
            elif action == "chips":
                print("\nChip counts:")
                for p in game.players:
                    print(f"  {p.name}: {p.chips}")
            elif action == "help":
                print("\nCommands: deal, fold, check, call, raise [amount], chips, quit")
            else:
                print(f"Unknown command: {action}")
        
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n\nGame ended.")
            break


if __name__ == "__main__":
    play_interactive()
