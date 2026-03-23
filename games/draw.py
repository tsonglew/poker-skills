"""
Five Card Draw poker game engine.

Usage:
    python -m games.draw play
"""

import random
from typing import List, Optional, Set
from dataclasses import dataclass, field
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.cards import Deck, Card, format_cards
from lib.hands import evaluate_hand


@dataclass
class Player:
    name: str
    chips: int = 1000
    hand: List[Card] = field(default_factory=list)
    current_bet: int = 0
    is_folded: bool = False
    is_human: bool = False
    discards: int = 0
    
    def reset_hand(self):
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.discards = 0


@dataclass
class DrawGame:
    """Five Card Draw poker game state."""
    deck: Deck = field(default_factory=Deck)
    players: List[Player] = field(default_factory=list)
    pot: int = 0
    current_bet: int = 0
    ante: int = 5
    phase: str = "betting"  # betting, draw, showdown
    current_player_index: int = 0
    dealer_index: int = 0
    is_hand_over: bool = False
    message: str = ""
    last_action: str = ""
    betting_round: int = 1  # 1 = before draw, 2 = after draw
    
    def add_player(self, name: str, chips: int = 1000, is_human: bool = False):
        """Add a player."""
        self.players.append(Player(name=name, chips=chips, is_human=is_human))
    
    def start_hand(self) -> str:
        """Start a new hand."""
        if len(self.players) < 2:
            return "Need at least 2 players."
        
        # Reset
        self.deck.reset()
        self.pot = 0
        self.current_bet = 0
        self.is_hand_over = False
        self.message = ""
        self.phase = "betting"
        self.betting_round = 1
        
        for player in self.players:
            player.reset_hand()
        
        # Move dealer
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        
        # Post antes
        for player in self.players:
            ante = min(self.ante, player.chips)
            player.chips -= ante
            self.pot += ante
        
        # Deal 5 cards
        for _ in range(5):
            for player in self.players:
                player.hand.append(self.deck.deal_one())
        
        # First to act is left of dealer
        self.current_player_index = (self.dealer_index + 1) % len(self.players)
        
        return self._render()
    
    def fold(self) -> str:
        """Fold current hand."""
        player = self.players[self.current_player_index]
        player.is_folded = True
        self.last_action = f"{player.name} folds"
        
        self._check_winner()
        if not self.is_hand_over:
            self._next_player()
        
        return self._render()
    
    def bet(self, amount: int = 0) -> str:
        """Bet or call."""
        player = self.players[self.current_player_index]
        
        if amount == 0:
            # Call/check
            to_call = self.current_bet - player.current_bet
            if to_call == 0:
                self.last_action = f"{player.name} checks"
            elif to_call >= player.chips:
                # All-in
                self.pot += player.chips
                player.current_bet += player.chips
                self.last_action = f"{player.name} calls all-in ({player.chips})"
                player.chips = 0
            else:
                player.chips -= to_call
                player.current_bet = self.current_bet
                self.pot += to_call
                self.last_action = f"{player.name} calls {to_call}"
        else:
            # Raise
            to_call = self.current_bet - player.current_bet
            total = to_call + amount
            
            if total >= player.chips:
                total = player.chips
                amount = total - to_call
            
            player.chips -= total
            player.current_bet += total
            self.pot += total
            self.current_bet = player.current_bet
            self.last_action = f"{player.name} bets {total}"
        
        self._next_player()
        return self._render()
    
    def draw(self, indices: List[int]) -> str:
        """
        Discard and draw new cards.
        
        Args:
            indices: Card indices to discard (0-4)
        """
        if self.phase != "draw":
            return "Not in draw phase."
        
        player = self.players[self.current_player_index]
        
        if player.is_folded:
            self._next_player()
            return self._render()
        
        # Validate indices
        indices = sorted(set(indices), reverse=True)
        
        if len(indices) > 4:
            return "Can only discard up to 4 cards."
        
        # Discard
        discarded = []
        for i in indices:
            if 0 <= i < len(player.hand):
                discarded.append(player.hand[i])
                player.hand.pop(i)
        
        # Draw new cards
        new_cards = self.deck.deal(len(discarded))
        player.hand.extend(new_cards)
        player.discards = len(discarded)
        
        self.last_action = f"{player.name} draws {len(discarded)} card(s)"
        
        self._next_player()
        return self._render()
    
    def stand_pat(self) -> str:
        """Keep current cards (draw 0)."""
        return self.draw([])
    
    def _next_player(self):
        """Move to next player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Check if betting round is complete
        active = [p for p in self.players if not p.is_folded]
        all_acted = all(p.current_bet == self.current_bet for p in active)
        
        if all_acted:
            if self.phase == "betting" and self.betting_round == 1:
                # Move to draw phase
                self.phase = "draw"
                self.current_player_index = (self.dealer_index + 1) % len(self.players)
                self.message = "\n*** DRAW PHASE ***"
            elif self.phase == "draw":
                # Move to final betting
                self.phase = "betting"
                self.betting_round = 2
                self.current_bet = 0
                for p in self.players:
                    p.current_bet = 0
                self.current_player_index = (self.dealer_index + 1) % len(self.players)
                self.message = "\n*** FINAL BETTING ***"
            elif self.phase == "betting" and self.betting_round == 2:
                self._showdown()
    
    def _check_winner(self):
        """Check if only one player remains."""
        active = [p for p in self.players if not p.is_folded]
        
        if len(active) == 1:
            winner = active[0]
            winner.chips += self.pot
            self.is_hand_over = True
            self.message = f"\n🏆 {winner.name} wins {self.pot} chips!"
    
    def _showdown(self):
        """Determine winner."""
        self.is_hand_over = True
        self.phase = "showdown"
        
        active = [p for p in self.players if not p.is_folded]
        
        # Evaluate hands
        results = []
        for player in active:
            hand = evaluate_hand(player.hand)
            results.append((player, hand))
        
        # Sort by strength
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Winner(s)
        winner = results[0]
        winners = [r for r in results if r[1] == winner[1]]
        
        share = self.pot // len(winners)
        for w_player, _ in winners:
            w_player.chips += share
        
        winner_names = ", ".join(w[0].name for w in winners)
        self.message = f"\n🏆 {winner_names} wins {self.pot} with {winner[1].name}!"
        
        # Show hands
        self.message += "\n\nShowdown:"
        for player, hand in results:
            cards = format_cards(player.hand)
            self.message += f"\n  {player.name}: {cards} → {hand.name}"
    
    def _render(self) -> str:
        """Render game state."""
        lines = [
            "",
            "═══════════════════════════════════════════════════",
            "            ♠ FIVE CARD DRAW ♠",
            "═══════════════════════════════════════════════════",
            f"  Pot: {self.pot}  |  Phase: {self.phase.upper()}  |  Bet: {self.current_bet}",
            "───────────────────────────────────────────────────",
        ]
        
        # Players
        for i, player in enumerate(self.players):
            marker = "→ " if i == self.current_player_index and not self.is_hand_over else "  "
            status = " [FOLDED]" if player.is_folded else ""
            
            if player.is_human or self.is_hand_over:
                cards = format_cards(player.hand) if player.hand else "--"
            else:
                cards = "?? ?? ?? ?? ??"
            
            lines.append(f"{marker}{player.name}: {cards} | {player.chips} chips{status}")
        
        lines.append("───────────────────────────────────────────────────")
        
        if self.last_action:
            lines.append(f"  Last: {self.last_action}")
        
        if self.message:
            lines.append(self.message)
        
        # Commands
        if not self.is_hand_over:
            player = self.players[self.current_player_index]
            if player.is_human:
                if self.phase == "betting":
                    lines.append("  Commands: fold, bet [amount], call/check")
                elif self.phase == "draw":
                    lines.append("  Commands: draw 0,1,2 | stand-pat")
        else:
            lines.append("  Type 'deal' for next hand")
        
        lines.append("═══════════════════════════════════════════════════")
        
        return "\n".join(lines)


def play_interactive():
    """Interactive Five Card Draw game."""
    game = DrawGame()
    
    print("\n♠♥♦♣ Welcome to Five Card Draw! ♣♦♥♠\n")
    
    # Setup
    game.add_player("You", 1000, is_human=True)
    game.add_player("Alice", 1000)
    game.add_player("Bob", 1000)
    
    print("Players: You, Alice, Bob")
    print(f"Ante: {game.ante}\n")
    
    print(game.start_hand())
    
    while True:
        try:
            current = game.players[game.current_player_index]
            
            # AI auto-plays
            if not current.is_human and not game.is_hand_over:
                import time
                time.sleep(0.5)
                
                if game.phase == "betting":
                    to_call = game.current_bet - current.current_bet
                    if to_call == 0:
                        if random.random() < 0.3:
                            game.bet(game.ante * 2)
                        else:
                            game.bet(0)  # check
                    elif to_call <= game.ante * 2:
                        game.bet(0)  # call
                    elif random.random() < 0.5:
                        game.bet(0)  # call
                    else:
                        game.fold()
                elif game.phase == "draw":
                    # Simple discard strategy
                    hand = evaluate_hand(current.hand)
                    if hand.rank.value >= 3:  # Pair or better
                        game.stand_pat()
                    else:
                        # Discard lowest cards
                        indices = [i for i in range(5)]
                        keep = 5 - min(3, 5 - hand.rank.value)
                        discard = random.sample(indices, min(3, 5 - keep))
                        game.draw(discard)
                
                print(game._render())
                continue
            
            cmd = input("\n> ").strip().lower().split()
            if not cmd:
                continue
            
            action = cmd[0]
            
            if action in ["q", "quit", "exit"]:
                print("\nFinal chips:")
                for p in game.players:
                    print(f"  {p.name}: {p.chips}")
                break
            elif action == "deal":
                print(game.start_hand())
            elif action == "fold":
                print(game.fold())
            elif action in ["bet", "raise"]:
                amount = int(cmd[1]) if len(cmd) > 1 else game.ante * 2
                print(game.bet(amount))
            elif action in ["call", "check"]:
                print(game.bet(0))
            elif action == "draw":
                if len(cmd) > 1:
                    indices = [int(x) for x in cmd[1].split(",")]
                else:
                    indices = []
                print(game.draw(indices))
            elif action == "stand-pat":
                print(game.stand_pat())
            elif action == "chips":
                for p in game.players:
                    print(f"  {p.name}: {p.chips}")
            elif action == "hand":
                player = game.players[0]  # You
                hand = evaluate_hand(player.hand)
                print(f"\nYour hand: {format_cards(player.hand)}")
                print(f"Best: {hand.name}")
            elif action == "help":
                print("\nCommands: deal, fold, bet [amount], call, draw 0,2,4, stand-pat, chips, hand, quit")
            else:
                print(f"Unknown: {action}")
        
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\n\nGame ended.")
            break


if __name__ == "__main__":
    play_interactive()
