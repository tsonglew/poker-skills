---
name: poker-games
description: Play famous poker games in Claude Code. Triggers when user asks to play poker, blackjack, Texas Hold'em, or card games.
version: 1.0.0
author: TsongLew <tsonglew@gmail.com>
---

# 🃏 Poker Games

Play classic poker games directly in Claude Code!

## Quick Start

Just say:
- "Let's play poker"
- "I want to play blackjack"
- "Deal me in for Texas Hold'em"

## Available Games

### 🃏 Blackjack (21)

The classic casino card game!

```
python games/blackjack.py
```

**Rules:**
- Get as close to 21 as possible without going over
- Face cards (J, Q, K) = 10, Ace = 1 or 11
- Dealer hits on 16, stands on 17
- Natural blackjack (A + 10-value) pays 3:2

**Commands:**
| Command | Description |
|---------|-------------|
| `deal [bet]` | Start new hand |
| `hit` | Take another card |
| `stand` | Keep current hand |
| `double` | Double down (2x bet, 1 card) |

---

### ♠ Texas Hold'em

The world's most popular poker variant!

```
python games/holdem.py
```

**Rules:**
- 2 hole cards per player
- 5 community cards (flop, turn, river)
- Best 5-card hand wins

**Commands:**
| Command | Description |
|---------|-------------|
| `deal` | Start a new hand |
| `fold` | Give up your hand |
| `check` | Pass without betting |
| `call` | Match the current bet |
| `raise [amount]` | Increase the bet |

---

### 🎴 Five Card Draw

Traditional draw poker!

```
python games/draw.py
```

**Rules:**
- 5 cards dealt face down
- One betting round
- Discard up to 4 cards and draw new ones
- Final betting round
- Best hand wins

**Commands:**
| Command | Description |
|---------|-------------|
| `deal` | Start a new hand |
| `fold` | Give up |
| `call` | Match the bet |
| `draw 0,2,4` | Discard cards at positions 0, 2, 4 |
| `stand-pat` | Keep all cards |

---

## Hand Rankings

From highest to lowest:

| Rank | Name | Example |
|------|------|---------|
| 1 | 🏆 Royal Flush | A♠ K♠ Q♠ J♠ 10♠ |
| 2 | 🔥 Straight Flush | 9♣ 8♣ 7♣ 6♣ 5♣ |
| 3 | 💪 Four of a Kind | K♠ K♥ K♦ K♣ 3♠ |
| 4 | 🏠 Full House | Q♠ Q♥ Q♦ 7♣ 7♥ |
| 5 | 💎 Flush | A♠ J♠ 8♠ 5♠ 2♠ |
| 6 | 📈 Straight | 10♠ 9♥ 8♦ 7♣ 6♠ |
| 7 | 🎯 Three of a Kind | 7♠ 7♥ 7♦ K♣ 2♠ |
| 8 | ✌️ Two Pair | J♠ J♥ 4♦ 4♣ 9♠ |
| 9 | 👆 One Pair | A♠ A♥ K♦ 7♣ 2♠ |
| 10 | 🃏 High Card | A♠ K♥ 9♦ 7♣ 2♠ |

---

## Tips

- Games track your chips between hands
- AI opponents use basic strategy
- Use `chips` command to check balance
- Use `help` command for available actions

---

## Files Structure

```
poker-skills/
├── SKILL.md              # This file
├── README.md             # Documentation
├── lib/
│   ├── cards.py          # Card & Deck utilities
│   └── hands.py          # Hand evaluation
└── games/
    ├── blackjack.py      # 21 game
    ├── holdem.py         # Texas Hold'em
    └── draw.py           # Five Card Draw
```

---

## Example Session

```
You: Let's play blackjack

Claude: Starting blackjack game...

╔══════════════════════════════════╗
│          ♠ BLACKJACK ♠          │
╠══════════════════════════════════╣
│ Chips: 1000                      │
╠══════════════════════════════════╣
│ Dealer: [K♠ ??] = ?              │
╠══════════════════════════════════╣
│ → Hand 1: [A♥ 7♦] = 18          │
╠══════════════════════════════════╣
│ Commands: hit | stand | double   │
╚══════════════════════════════════╝

You: hit

Claude: You draw 3♣ for 21! BLACKJACK!
```

---

*Created by TsongLew <tsonglew@gmail.com>*
