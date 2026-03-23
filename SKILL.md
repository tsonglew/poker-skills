---
name: poker-games
description: Play famous poker games in Claude Code. Triggers when user asks to play poker, blackjack, Texas Hold'em, or card games.
version: 1.0.0
author: TsongLew <tsonglew@gmail.com>
---

# Poker Games

Play classic poker games directly in Claude Code! This skill includes:

- **Texas Hold'em** - The most popular poker variant
- **Blackjack** - Classic 21 card game
- **Five Card Draw** - Traditional draw poker

## Quick Start

Just say:
- "Let's play poker"
- "I want to play blackjack"
- "Deal me in for Texas Hold'em"

## Games

### Texas Hold'em

```
/play-holdem [buy-in]
```

Standard Texas Hold'em rules:
- 2 hole cards per player
- 5 community cards (flop, turn, river)
- Best 5-card hand wins

### Blackjack

```
/play-blackjack [bet]
```

Classic 21 rules:
- Get as close to 21 as possible without going over
- Face cards = 10, Ace = 1 or 11
- Dealer hits on 16, stands on 17

### Five Card Draw

```
/play-draw [bet]
```

Traditional poker:
- 5 cards dealt face down
- One draw round to replace cards
- Best hand wins

## Hand Rankings (Texas Hold'em & Draw)

1. Royal Flush - A K Q J 10 (same suit)
2. Straight Flush - 5 consecutive cards (same suit)
3. Four of a Kind
4. Full House - 3 of a kind + pair
5. Flush - 5 cards same suit
6. Straight - 5 consecutive cards
7. Three of a Kind
8. Two Pair
9. One Pair
10. High Card

## Files

- `games/holdem.py` - Texas Hold'em engine
- `games/blackjack.py` - Blackjack engine
- `games/draw.py` - Five Card Draw engine
- `lib/cards.py` - Card deck utilities
- `lib/hands.py` - Hand evaluation

## Commands

| Command | Description |
|---------|-------------|
| `deal` | Start a new hand |
| `hit` | Take another card (blackjack) |
| `stand` | Keep current hand |
| `fold` | Give up your hand |
| `call` | Match the current bet |
| `raise [amount]` | Increase the bet |
| `check` | Pass without betting |
| `all-in` | Bet all your chips |

## Tips

- Claude manages the game state and remembers your chips
- Games are saved between sessions
- Use `chip count` to check your balance
- Use `game stats` to see your win/loss record

---

*Created by TsongLew <tsonglew@gmail.com>*
