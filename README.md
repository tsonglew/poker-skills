# 🃏 Poker Skills for Claude Code

Play classic poker games directly in Claude Code!

## Games

| Game | Description | Run |
|------|-------------|-----|
| **Blackjack** | Classic 21 card game | `python games/blackjack.py` |
| **Texas Hold'em** | Most popular poker variant | `python games/holdem.py` |
| **Five Card Draw** | Traditional draw poker | `python games/draw.py` |

## Installation

```bash
# Clone into your Claude Code skills directory
cd ~/.claude/skills
git clone git@github.com:tsonglew/poker-skills.git

# Or use with Claude Code directly
cd poker-skills
python games/blackjack.py
```

## Quick Start

### Blackjack

```
python games/blackjack.py

> deal 10      # Deal a hand with $10 bet
> hit          # Take another card
> stand        # Keep current hand
> double       # Double down
```

### Texas Hold'em

```
python games/holdem.py

> deal         # Start a new hand
> call         # Match the bet
> raise 20     # Raise by $20
> fold         # Give up your hand
```

### Five Card Draw

```
python games/draw.py

> deal         # Start a new hand
> call         # Match the bet
> draw 0,2,4   # Discard cards at positions 0, 2, 4
> stand-pat    # Keep all cards
```

## Hand Rankings

1. 🏆 Royal Flush - A K Q J 10 (same suit)
2. 🔥 Straight Flush - 5 consecutive (same suit)
3. 💪 Four of a Kind
4. 🏠 Full House - 3 of a kind + pair
5. 💎 Flush - 5 cards same suit
6. 📈 Straight - 5 consecutive cards
7. 🎯 Three of a Kind
8. ✌️ Two Pair
9. 👆 One Pair
10. 🃏 High Card

## Files

```
poker-skills/
├── SKILL.md           # Skill definition
├── README.md          # This file
├── lib/
│   ├── __init__.py
│   ├── cards.py       # Card & Deck classes
│   └── hands.py       # Hand evaluation
└── games/
    ├── __init__.py
    ├── blackjack.py   # 21 game
    ├── holdem.py      # Texas Hold'em
    └── draw.py        # Five Card Draw
```

## Features

- ✅ Full game state management
- ✅ AI opponents with basic strategy
- ✅ Chip tracking across hands
- ✅ Hand evaluation for all poker hands
- ✅ ASCII card display

## Requirements

- Python 3.8+
- No external dependencies

## License

MIT

---

*Created by TsongLew <tsonglew@gmail.com>*
