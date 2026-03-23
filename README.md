# 🃏 Poker & Card Games Skills for Claude Code

Play classic poker and Chinese card games directly in Claude Code!

## Games

| Game | Type | Players | Description |
|------|------|---------|-------------|
| **Blackjack** | 🌍 西方 | 1 vs Dealer | 经典21点 |
| **Texas Hold'em** | 🌍 西方 | 4+ | 德州扑克 |
| **Five Card Draw** | 🌍 西方 | 3+ | 五张抽牌 |
| **斗地主** | 🇨🇳 中国 | 3 (1v2) | 经典斗地主 |
| **掼蛋** | 🇨🇳 中国 | 4 (2v2) | 江苏掼蛋 |

## Quick Start

```bash
# Clone
cd ~/.claude/skills
git clone git@github.com:tsonglew/poker-skills.git

# Run games
cd poker-skills
python games/blackjack.py    # 21点
python games/holdem.py       # 德州扑克
python games/draw.py         # 五张抽牌
python games/doudizhu.py     # 斗地主
python games/guandan.py      # 掼蛋
```

---

## 🇨🇳 中国棋牌

### 斗地主

3人对战（1地主 vs 2农民），54张牌

**玩法：**
```
python games/doudizhu.py

> bid 3          # 叫地主（叫3分）
> play 0,1,2     # 出牌（索引）
> pass           # 不出
> cards          # 查看手牌索引
```

**牌型：** 单张、对子、三张、三带一/二、顺子、连对、飞机、炸弹、王炸

---

### 掼蛋

4人2队对抗，108张牌（两副牌）

**玩法：**
```
python games/guandan.py

> play 0,1,2     # 出牌
> pass           # 不出
> cards          # 查看手牌
> deal           # 新一局
```

**特色：**
- 从2打到A通关
- 同花顺 > 炸弹
- 双下升3级
- 王炸（四大天王）最大

---

## 🌍 西方扑克

### Blackjack

```
> deal 10        # 发牌，赌$10
> hit            # 要牌
> stand          # 停牌
> double         # 双倍下注
```

### Texas Hold'em

```
> deal           # 发牌
> call           # 跟注
> raise 20       # 加注$20
> fold           # 弃牌
```

### Five Card Draw

```
> deal           # 发牌
> call           # 跟注
> draw 0,2,4     # 换掉索引0,2,4的牌
> stand-pat      # 不换牌
```

---

## Hand Rankings

### 西方扑克

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

### 斗地主

王炸 > 炸弹 > 其他（同类型比点数，2最大，王>2）

### 掼蛋

王炸 > 6张+炸弹 > 同花顺 > 炸弹 > 其他

---

## Files

```
poker-skills/
├── SKILL.md           # Claude Code Skill
├── README.md          # This file
├── lib/
│   ├── __init__.py
│   ├── cards.py       # Card utilities
│   └── hands.py       # Hand evaluation
└── games/
    ├── __init__.py
    ├── blackjack.py   # 21
    ├── holdem.py      # Texas Hold'em
    ├── draw.py        # Five Card Draw
    ├── doudizhu.py    # 斗地主
    └── guandan.py     # 掼蛋
```

## Features

- ✅ Full game state management
- ✅ AI opponents with basic strategy
- ✅ Chip tracking & level progression
- ✅ All major card combinations
- ✅ Chinese & Western games

## Requirements

- Python 3.8+
- No external dependencies

## License

MIT

---

*Created by TsongLew <tsonglew@gmail.com>*

**Repository:** https://github.com/tsonglew/poker-skills
