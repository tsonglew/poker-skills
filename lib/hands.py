"""
Poker hand evaluation utilities.
"""

from typing import List, Tuple, Optional
from enum import IntEnum
from dataclasses import dataclass
from lib.cards import Card, Rank, Suit


class HandRank(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


@dataclass
class EvaluatedHand:
    """Result of hand evaluation."""
    rank: HandRank
    name: str
    cards: List[Card]
    kickers: List[int]
    
    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.kickers < other.kickers
    
    def __eq__(self, other):
        return self.rank == other.rank and self.kickers == other.kickers
    
    def __str__(self):
        return self.name


def evaluate_hand(cards: List[Card]) -> EvaluatedHand:
    """
    Evaluate the best 5-card poker hand from given cards.
    
    Args:
        cards: List of 5-7 cards
        
    Returns:
        EvaluatedHand with rank, name, and kickers
    """
    if len(cards) < 5:
        raise ValueError("Need at least 5 cards to evaluate")
    
    # Find best 5-card combination
    best_hand = None
    from itertools import combinations
    
    for combo in combinations(cards, 5):
        hand = _evaluate_five(list(combo))
        if best_hand is None or hand > best_hand:
            best_hand = hand
    
    return best_hand


def _evaluate_five(cards: List[Card]) -> EvaluatedHand:
    """Evaluate exactly 5 cards."""
    ranks = sorted([c.rank.value for c in cards], reverse=True)
    suits = [c.suit for c in cards]
    
    # Count rank occurrences
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1
    
    # Check for flush
    is_flush = len(set(suits)) == 1
    
    # Check for straight
    is_straight, straight_high = _check_straight(ranks)
    
    # Get sorted counts
    counts = sorted(rank_counts.values(), reverse=True)
    sorted_ranks = sorted(rank_counts.keys(), key=lambda r: (rank_counts[r], r), reverse=True)
    
    # Determine hand rank
    if is_straight and is_flush:
        if straight_high == 14:  # Ace-high straight flush
            return EvaluatedHand(HandRank.ROYAL_FLUSH, "Royal Flush", cards, [10])
        else:
            return EvaluatedHand(HandRank.STRAIGHT_FLUSH, "Straight Flush", cards, [straight_high])
    
    if counts == [4, 1]:
        return EvaluatedHand(HandRank.FOUR_OF_A_KIND, "Four of a Kind", cards, sorted_ranks)
    
    if counts == [3, 2]:
        return EvaluatedHand(HandRank.FULL_HOUSE, "Full House", cards, sorted_ranks)
    
    if is_flush:
        return EvaluatedHand(HandRank.FLUSH, "Flush", cards, ranks)
    
    if is_straight:
        return EvaluatedHand(HandRank.STRAIGHT, "Straight", cards, [straight_high])
    
    if counts == [3, 1, 1]:
        return EvaluatedHand(HandRank.THREE_OF_A_KIND, "Three of a Kind", cards, sorted_ranks)
    
    if counts == [2, 2, 1]:
        return EvaluatedHand(HandRank.TWO_PAIR, "Two Pair", cards, sorted_ranks)
    
    if counts == [2, 1, 1, 1]:
        return EvaluatedHand(HandRank.ONE_PAIR, "One Pair", cards, sorted_ranks)
    
    return EvaluatedHand(HandRank.HIGH_CARD, "High Card", cards, ranks)


def _check_straight(ranks: List[int]) -> Tuple[bool, int]:
    """Check if ranks form a straight. Returns (is_straight, high_card)."""
    unique = sorted(set(ranks), reverse=True)
    
    if len(unique) != 5:
        return False, 0
    
    # Normal straight
    if unique[0] - unique[4] == 4:
        return True, unique[0]
    
    # Wheel (A-2-3-4-5)
    if unique == [14, 5, 4, 3, 2]:
        return True, 5  # 5-high straight
    
    return False, 0


def compare_hands(hand1: EvaluatedHand, hand2: EvaluatedHand) -> int:
    """
    Compare two evaluated hands.
    
    Returns:
        1 if hand1 wins, -1 if hand2 wins, 0 if tie
    """
    if hand1 > hand2:
        return 1
    elif hand1 < hand2:
        return -1
    return 0


def hand_description(cards: List[Card]) -> str:
    """Get human-readable description of the best hand."""
    hand = evaluate_hand(cards)
    return f"{hand.name}"


# Quick test
if __name__ == "__main__":
    from lib.cards import Deck
    
    deck = Deck()
    hand = deck.deal(5)
    print(f"Cards: {hand}")
    print(f"Hand: {evaluate_hand(hand)}")
