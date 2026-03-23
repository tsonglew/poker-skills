"""
Card deck utilities for poker games.
"""

import random
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"
    
    def __str__(self):
        return self.value


class Rank(Enum):
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")
    
    def __init__(self, value: int, symbol: str):
        self.value = value
        self.symbol = symbol
    
    def __str__(self):
        return self.symbol


@dataclass
class Card:
    rank: Rank
    suit: Suit
    
    def __str__(self):
        return f"{self.rank.symbol}{self.suit.value}"
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return self.rank.value < other.rank.value
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False
    
    def __hash__(self):
        return hash((self.rank, self.suit))


class Deck:
    """Standard 52-card deck."""
    
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self):
        """Reset and shuffle the deck."""
        self.cards = [
            Card(rank, suit)
            for suit in Suit
            for rank in Rank
        ]
        self.shuffle()
    
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def deal(self, num: int = 1) -> List[Card]:
        """Deal cards from the top of the deck."""
        dealt = []
        for _ in range(num):
            if self.cards:
                dealt.append(self.cards.pop())
        return dealt
    
    def deal_one(self) -> Optional[Card]:
        """Deal a single card."""
        return self.cards.pop() if self.cards else None
    
    def cards_remaining(self) -> int:
        """Number of cards left in deck."""
        return len(self.cards)


def card_from_string(s: str) -> Optional[Card]:
    """Parse a card from string like 'A♥' or '10♠'."""
    if len(s) < 2:
        return None
    
    suit_map = {
        "♥": Suit.HEARTS,
        "♦": Suit.DIAMONDS,
        "♣": Suit.CLUBS,
        "♠": Suit.SPADES,
        "H": Suit.HEARTS,
        "D": Suit.DIAMONDS,
        "C": Suit.CLUBS,
        "S": Suit.SPADES,
    }
    
    rank_map = {
        "2": Rank.TWO, "3": Rank.THREE, "4": Rank.FOUR, "5": Rank.FIVE,
        "6": Rank.SIX, "7": Rank.SEVEN, "8": Rank.EIGHT, "9": Rank.NINE,
        "10": Rank.TEN, "J": Rank.JACK, "Q": Rank.QUEEN, "K": Rank.KING,
        "A": Rank.ACE,
    }
    
    suit_char = s[-1]
    rank_str = s[:-1].upper()
    
    if suit_char not in suit_map or rank_str not in rank_map:
        return None
    
    return Card(rank_map[rank_str], suit_map[suit_char])


def format_cards(cards: List[Card], separator: str = " ") -> str:
    """Format a list of cards for display."""
    return separator.join(str(card) for card in cards)


def cards_to_ascii(cards: List[Card]) -> str:
    """Convert cards to ASCII art representation."""
    lines = [""] * 5
    for card in cards:
        card_lines = _single_card_ascii(card)
        for i, line in enumerate(card_lines):
            lines[i] += line + " "
    return "\n".join(lines)


def _single_card_ascii(card: Card) -> List[str]:
    """Generate ASCII art for a single card."""
    rank = card.rank.symbol
    suit = card.suit.value
    
    # Adjust for 10 (two characters)
    rank_display = rank if rank != "10" else "10"
    
    if rank == "10":
        return [
            "┌─────────┐",
            f"│{rank_display}        │",
            f"│    {suit}    │",
            f"│        {rank_display}│",
            "└─────────┘",
        ]
    else:
        return [
            "┌─────────┐",
            f"│{rank}        │",
            f"│    {suit}    │",
            f"│        {rank}│",
            "└─────────┘",
        ]
