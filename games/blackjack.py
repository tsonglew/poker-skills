"""
Blackjack (21) game engine.

Usage:
    python -m games.blackjack play [bet]
    python -m games.blackjack strategy
"""

import random
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.cards import Deck, Card, Rank


class Action(Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"
    SPLIT = "split"


@dataclass
class Hand:
    cards: List[Card] = field(default_factory=list)
    bet: int = 0
    is_doubled: bool = False
    is_split: bool = False
    is_standing: bool = False
    is_busted: bool = False
    
    def add_card(self, card: Card):
        self.cards.append(card)
        if self.value > 21:
            self.is_busted = True
    
    @property
    def value(self) -> int:
        """Calculate hand value."""
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == Rank.ACE:
                aces += 1
                total += 11
            elif card.rank.value >= 10:  # J, Q, K
                total += 10
            else:
                total += card.rank.value
        
        # Adjust for aces
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total
    
    @property
    def is_blackjack(self) -> bool:
        """Check for natural blackjack."""
        return len(self.cards) == 2 and self.value == 21
    
    @property
    def can_split(self) -> bool:
        """Check if hand can be split."""
        return (
            len(self.cards) == 2 and 
            self.cards[0].rank.value == self.cards[1].rank.value and
            not self.is_split
        )
    
    @property
    def can_double(self) -> bool:
        """Check if can double down."""
        return len(self.cards) == 2 and not self.is_doubled
    
    def __str__(self) -> str:
        cards_str = " ".join(str(c) for c in self.cards)
        status = ""
        if self.is_blackjack:
            status = " BLACKJACK!"
        elif self.is_busted:
            status = " BUST!"
        return f"[{cards_str}] = {self.value}{status}"


@dataclass
class BlackjackGame:
    """Blackjack game state."""
    deck: Deck = field(default_factory=Deck)
    player_hands: List[Hand] = field(default_factory=list)
    dealer_hand: Hand = field(default_factory=Hand)
    chips: int = 1000
    current_hand_index: int = 0
    game_over: bool = False
    message: str = ""
    
    def deal(self, bet: int) -> str:
        """Start a new round."""
        if bet > self.chips:
            return f"Not enough chips! You have {self.chips}."
        
        if self.deck.cards_remaining() < 15:
            self.deck.reset()
        
        # Reset hands
        self.player_hands = [Hand(bet=bet)]
        self.dealer_hand = Hand()
        self.current_hand_index = 0
        self.game_over = False
        self.message = ""
        
        # Deal initial cards
        self.player_hands[0].add_card(self.deck.deal_one())
        self.dealer_hand.add_card(self.deck.deal_one())
        self.player_hands[0].add_card(self.deck.deal_one())
        self.dealer_hand.add_card(self.deck.deal_one())
        
        # Check for blackjacks
        if self.player_hands[0].is_blackjack:
            if self.dealer_hand.is_blackjack:
                self.game_over = True
                self.message = "Both have blackjack! Push."
            else:
                self.game_over = True
                self.chips += int(bet * 1.5)
                self.message = f"BLACKJACK! You win {int(bet * 1.5)} chips!"
        elif self.dealer_hand.is_blackjack:
            self.game_over = True
            self.chips -= bet
            self.message = f"Dealer blackjack! You lose {bet} chips."
        
        return self._render()
    
    def hit(self) -> str:
        """Take another card."""
        if self.game_over:
            return "Game is over. Start a new hand with 'deal'."
        
        hand = self.player_hands[self.current_hand_index]
        hand.add_card(self.deck.deal_one())
        
        if hand.is_busted:
            self.chips -= hand.bet
            self.message = f"Bust! You lose {hand.bet} chips."
            self._next_hand()
        
        return self._render()
    
    def stand(self) -> str:
        """Stand with current hand."""
        if self.game_over:
            return "Game is over. Start a new hand with 'deal'."
        
        self.player_hands[self.current_hand_index].is_standing = True
        self._next_hand()
        return self._render()
    
    def double(self) -> str:
        """Double down."""
        if self.game_over:
            return "Game is over. Start a new hand with 'deal'."
        
        hand = self.player_hands[self.current_hand_index]
        
        if not hand.can_double:
            return "Can only double down on initial two cards."
        
        if hand.bet > self.chips:
            return f"Not enough chips to double! You have {self.chips}."
        
        hand.bet *= 2
        hand.is_doubled = True
        hand.add_card(self.deck.deal_one())
        
        if hand.is_busted:
            self.chips -= hand.bet
            self.message = f"Bust! You lose {hand.bet} chips."
            self._next_hand()
        else:
            self._next_hand()
        
        return self._render()
    
    def _next_hand(self):
        """Move to next hand or dealer turn."""
        self.current_hand_index += 1
        
        if self.current_hand_index >= len(self.player_hands):
            self._dealer_turn()
    
    def _dealer_turn(self):
        """Dealer plays their hand."""
        # Reveal dealer's hole card and play
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal_one())
        
        self._resolve()
    
    def _resolve(self):
        """Resolve all hands."""
        dealer_value = self.dealer_hand.value
        dealer_bust = self.dealer_hand.is_busted
        
        results = []
        total_win = 0
        total_loss = 0
        
        for hand in self.player_hands:
            if hand.is_busted:
                continue  # Already counted as loss
            
            player_value = hand.value
            
            if dealer_bust:
                win = hand.bet
                total_win += win
                results.append(f"Dealer busts! Win {win} chips.")
            elif player_value > dealer_value:
                win = hand.bet
                total_win += win
                results.append(f"{player_value} beats {dealer_value}! Win {win} chips.")
            elif player_value < dealer_value:
                total_loss += hand.bet
                results.append(f"Dealer's {dealer_value} beats {player_value}. Lose {hand.bet} chips.")
            else:
                results.append(f"Push at {player_value}.")
        
        self.chips += total_win - total_loss
        self.message = " | ".join(results)
        self.game_over = True
    
    def _render(self) -> str:
        """Render game state."""
        lines = [
            "╔══════════════════════════════════╗",
            "│          ♠ BLACKJACK ♠          │",
            "╠══════════════════════════════════╣",
            f"│ Chips: {self.chips:>6}                   │",
            "╠══════════════════════════════════╣",
        ]
        
        # Dealer's hand
        if self.game_over or self.current_hand_index >= len(self.player_hands):
            dealer_display = str(self.dealer_hand)
        else:
            # Hide hole card
            visible = f"[{self.dealer_hand.cards[0]} ??]"
            dealer_display = f"{visible} = ?"
        
        lines.append(f"│ Dealer: {dealer_display:<25} │")
        lines.append("╠══════════════════════════════════╣")
        
        # Player's hands
        for i, hand in enumerate(self.player_hands):
            prefix = "→ " if i == self.current_hand_index and not self.game_over else "  "
            lines.append(f"│ {prefix}Hand {i+1}: {str(hand):<22} │")
        
        lines.append("╠══════════════════════════════════╣")
        
        if self.message:
            lines.append(f"│ {self.message:<32} │")
            lines.append("╠══════════════════════════════════╣")
        
        if self.game_over:
            lines.append("│ Commands: deal [bet]             │")
        else:
            lines.append("│ Commands: hit | stand | double   │")
        
        lines.append("╚══════════════════════════════════╝")
        
        return "\n".join(lines)


def basic_strategy(player_total: int, dealer_up: int, soft: bool = False, can_double: bool = True) -> str:
    """Return basic strategy recommendation."""
    # Hard totals
    if not soft:
        if player_total >= 17:
            return "STAND"
        if player_total <= 8:
            return "HIT"
        if player_total == 9:
            return "DOUBLE" if dealer_up in [3, 4, 5, 6] and can_double else "HIT"
        if player_total == 10:
            return "DOUBLE" if dealer_up <= 9 and can_double else "HIT"
        if player_total == 11:
            return "DOUBLE" if can_double else "HIT"
        if player_total == 12:
            return "STAND" if dealer_up in [4, 5, 6] else "HIT"
        if 13 <= player_total <= 16:
            return "STAND" if dealer_up <= 6 else "HIT"
    else:
        # Soft totals
        if player_total >= 19:
            return "STAND"
        if player_total == 18:
            return "DOUBLE" if dealer_up in [2, 3, 4, 5, 6] and can_double else "STAND"
        if player_total == 17:
            return "DOUBLE" if dealer_up in [3, 4, 5, 6] and can_double else "HIT"
        if 15 <= player_total <= 16:
            return "DOUBLE" if dealer_up in [4, 5, 6] and can_double else "HIT"
        if 13 <= player_total <= 14:
            return "DOUBLE" if dealer_up in [5, 6] and can_double else "HIT"
    
    return "HIT"


def play_interactive(starting_chips: int = 1000):
    """Interactive blackjack game."""
    game = BlackjackGame(chips=starting_chips)
    
    print("\n♠♥♦♣ Welcome to Blackjack! ♣♦♥♠\n")
    print(f"Starting with {starting_chips} chips.\n")
    print(game._render())
    
    while True:
        try:
            cmd = input("\n> ").strip().lower().split()
            if not cmd:
                continue
            
            action = cmd[0]
            
            if action in ["q", "quit", "exit"]:
                print(f"\nThanks for playing! Final chips: {game.chips}")
                break
            elif action == "deal":
                bet = int(cmd[1]) if len(cmd) > 1 else 10
                print("\n" + game.deal(bet))
            elif action == "hit":
                print("\n" + game.hit())
            elif action == "stand":
                print("\n" + game.stand())
            elif action == "double":
                print("\n" + game.double())
            elif action == "chips":
                print(f"\nChips: {game.chips}")
            elif action == "help":
                print("\nCommands: deal [bet], hit, stand, double, chips, quit")
            else:
                print(f"Unknown command: {action}")
        
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print(f"\n\nThanks for playing! Final chips: {game.chips}")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "strategy":
            print("\nBasic Blackjack Strategy:")
            print("=" * 50)
            print("\nHard Totals:")
            for total in range(5, 21):
                print(f"  {total}: ", end="")
                recs = []
                for dealer in range(2, 12):
                    recs.append(basic_strategy(total, dealer if dealer <= 10 else 11)[:1])
                print(" ".join(recs) + f"  (dealer: 2-9,T,A)")
            print("\n  H=Hit, S=Stand, D=Double")
        else:
            play_interactive()
    else:
        play_interactive()
