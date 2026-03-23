"""
Baccarat game.

Classic casino game - bet on Player, Banker, or Tie.
Banker has slight edge, 5% commission on wins.

Usage:
    python games/baccarat.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
from dataclasses import dataclass, field
from lib.cards import Deck, Card, Rank


@dataclass
class BaccaratGame:
    """Baccarat game state."""
    deck: Deck = field(default_factory=Deck)
    player_hand: List[Card] = field(default_factory=list)
    banker_hand: List[Card] = field(default_factory=list)
    chips: int = 1000
    player_bet: int = 0  # Bet on Player
    banker_bet: int = 0  # Bet on Banker
    tie_bet: int = 0     # Bet on Tie
    message: str = ""
    game_over: bool = True
    
    def deal(self, player_bet: int = 0, banker_bet: int = 0, tie_bet: int = 0) -> str:
        """Deal a new hand with bets."""
        total_bet = player_bet + banker_bet + tie_bet
        
        if total_bet > self.chips:
            return f"Not enough chips! You have {self.chips}."
        
        if total_bet == 0:
            return "Place a bet on Player, Banker, or Tie!"
        
        if self.deck.cards_remaining() < 15:
            self.deck.reset()
        
        # Store bets
        self.player_bet = player_bet
        self.banker_bet = banker_bet
        self.tie_bet = tie_bet
        self.chips -= total_bet
        
        # Reset hands
        self.player_hand = []
        self.banker_hand = []
        self.game_over = False
        self.message = ""
        
        # Deal initial 2 cards each
        self.player_hand.append(self.deck.deal_one())
        self.banker_hand.append(self.deck.deal_one())
        self.player_hand.append(self.deck.deal_one())
        self.banker_hand.append(self.deck.deal_one())
        
        # Check for naturals (8 or 9)
        player_total = self._hand_value(self.player_hand)
        banker_total = self._hand_value(self.banker_hand)
        
        if player_total >= 8 or banker_total >= 8:
            # Natural - no more cards
            self._resolve()
        else:
            # Player's rule
            if player_total <= 5:
                self.player_hand.append(self.deck.deal_one())
                player_third = self._card_value(self.player_hand[2])
            else:
                player_third = -1
            
            # Banker's rule
            banker_draw = self._banker_draws(banker_total, player_third)
            if banker_draw:
                self.banker_hand.append(self.deck.deal_one())
            
            self._resolve()
        
        return self._render()
    
    def _card_value(self, card: Card) -> int:
        """Get baccarat value of a card."""
        if card.rank.value >= 10:  # 10, J, Q, K
            return 0
        return card.rank.value
    
    def _hand_value(self, hand: List[Card]) -> int:
        """Calculate hand value (mod 10)."""
        total = sum(self._card_value(c) for c in hand)
        return total % 10
    
    def _banker_draws(self, banker_total: int, player_third: int) -> bool:
        """Determine if banker draws a third card."""
        if banker_total >= 7:
            return False
        if banker_total <= 2:
            return True
        if banker_total == 3:
            return player_third != 8  # Draw unless player drew 8
        if banker_total == 4:
            return player_third in [0, 1, 8, 9] or player_third in range(2, 8)
        if banker_total == 5:
            return player_third in [0, 1, 2, 3] or player_third in range(4, 8)
        if banker_total == 6:
            return player_third in [6, 7]
        return False
    
    def _resolve(self):
        """Resolve the hand."""
        player_total = self._hand_value(self.player_hand)
        banker_total = self._hand_value(self.banker_hand)
        
        self.game_over = True
        
        if player_total > banker_total:
            # Player wins
            win = self.player_bet * 2
            self.chips += win
            self.message = f"Player wins {player_total}-{banker_total}!"
            if self.player_bet > 0:
                self.message += f" Won ${self.player_bet}!"
            if self.banker_bet > 0:
                self.message += f" Lost ${self.banker_bet} on Banker."
            if self.tie_bet > 0:
                self.message += f" Lost ${self.tie_bet} on Tie."
        
        elif banker_total > player_total:
            # Banker wins (5% commission)
            commission = int(self.banker_bet * 0.05)
            win = self.banker_bet * 2 - commission
            self.chips += win
            self.message = f"Banker wins {banker_total}-{player_total}!"
            if self.banker_bet > 0:
                self.message += f" Won ${self.banker_bet - commission} (after 5% commission)!"
            if self.player_bet > 0:
                self.message += f" Lost ${self.player_bet} on Player."
            if self.tie_bet > 0:
                self.message += f" Lost ${self.tie_bet} on Tie."
        
        else:
            # Tie
            win = self.tie_bet * 9  # 8:1 payout + original bet
            self.chips += win
            self.message = f"Tie at {player_total}!"
            if self.tie_bet > 0:
                self.message += f" Won ${self.tie_bet * 8} on Tie!"
            # Player and Banker bets push (returned)
            self.chips += self.player_bet + self.banker_bet
            if self.player_bet > 0 or self.banker_bet > 0:
                self.message += " Other bets push."
        
        # Reset bets
        self.player_bet = 0
        self.banker_bet = 0
        self.tie_bet = 0
    
    def _render(self) -> str:
        """Render game state."""
        lines = [
            "╔════════════════════════════════════════════════════╗",
            "│                  🎰 BACCARAT 🎰                   │",
            "╠════════════════════════════════════════════════════╣",
            f"│ Chips: ${self.chips:<6}                                    │",
            "╠════════════════════════════════════════════════════╣",
        ]
        
        # Banker's hand
        banker_cards = " ".join(str(c) for c in self.banker_hand)
        banker_val = self._hand_value(self.banker_hand) if self.banker_hand else 0
        lines.append(f"│ BANKER: {banker_cards:<20} = {banker_val}           │")
        
        lines.append("│                                                      │")
        
        # Player's hand
        player_cards = " ".join(str(c) for c in self.player_hand)
        player_val = self._hand_value(self.player_hand) if self.player_hand else 0
        lines.append(f"│ PLAYER: {player_cards:<20} = {player_val}           │")
        
        lines.append("╠════════════════════════════════════════════════════╣")
        
        if self.message:
            lines.append(f"│ {self.message:<52} │")
            lines.append("╠════════════════════════════════════════════════════╣")
        
        if self.game_over:
            lines.append("│ Commands: player [amt] | banker [amt] | tie [amt]  │")
            lines.append("│          | deal p [b [t]] | quit                   │")
        else:
            lines.append("│ Game in progress...                                 │")
        
        lines.append("╚════════════════════════════════════════════════════╝")
        
        return "\n".join(lines)


def play_interactive():
    """Interactive baccarat game."""
    game = BaccaratGame()
    
    print("\n🎰 Welcome to Baccarat! 🎰")
    print("Bet on Player (1:1), Banker (1:1 - 5%), or Tie (8:1)\n")
    print(game._render())
    
    while True:
        try:
            cmd = input("\n> ").strip().lower().split()
            if not cmd:
                continue
            
            action = cmd[0]
            
            if action in ["q", "quit", "exit"]:
                print(f"\nThanks for playing! Final chips: ${game.chips}")
                break
            elif action == "player":
                bet = int(cmd[1]) if len(cmd) > 1 else 10
                print("\n" + game.deal(player_bet=bet))
            elif action == "banker":
                bet = int(cmd[1]) if len(cmd) > 1 else 10
                print("\n" + game.deal(banker_bet=bet))
            elif action == "tie":
                bet = int(cmd[1]) if len(cmd) > 1 else 10
                print("\n" + game.deal(tie_bet=bet))
            elif action == "deal":
                # Quick bet: deal p b t
                p = int(cmd[1]) if len(cmd) > 1 else 0
                b = int(cmd[2]) if len(cmd) > 2 else 0
                t = int(cmd[3]) if len(cmd) > 3 else 0
                if p == 0 and b == 0 and t == 0:
                    p = 10
                print("\n" + game.deal(player_bet=p, banker_bet=b, tie_bet=t))
            elif action == "chips":
                print(f"\nChips: ${game.chips}")
            elif action == "help":
                print("\nCommands: player [amt], banker [amt], tie [amt], chips, quit")
            else:
                print(f"Unknown command: {action}")
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    play_interactive()
