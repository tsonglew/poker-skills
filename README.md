# 🃏 Poker & Card Games Skills for Claude Code

Play classic poker and card games directly in Claude Code!

## Games (24 Total)

### 🇨🇳 中国棋牌 (Chinese Games)

| Game | Players | Description |
|------|---------|-------------|
| **斗地主** | 3 (1v2) | 经典斗地主，54张牌 |
| **掼蛋** | 4 (2v2) | 江苏掼蛋，108张牌 |
| **跑得快** | 3 | 先出完牌者胜 |
| **大老二** | 4 | 香港扑克，2最大 |
| **十三张** | 4 | 中国扑克，排3手牌 |

### 🌍 西方扑克 (Western Poker)

| Game | Players | Description |
|------|---------|-------------|
| **Texas Hold'em** | 4+ | 德州扑克 |
| **Omaha** | 4+ | 奥马哈，发4张牌 |
| **7-Card Stud** | 4+ | 七张牌梭哈 |
| **Five Card Draw** | 3+ | 五张抽牌 |
| **Pineapple** | 4+ | 菠萝扑克，3弃1 |
| **Short Deck** | 4+ | 短牌德州(6+) |
| **Razz** | 4+ | 低牌扑克 |
| **Badugi** | 4+ | 韩国低牌 |

### 🎰 赌场游戏 (Casino Games)

| Game | Players | Description |
|------|---------|-------------|
| **Blackjack** | 1 | 经典21点 |
| **Baccarat** | 1 | 百家乐 |
| **Three Card Poker** | 1 | 三张扑克 |
| **Caribbean Stud** | 1 | 加勒比梭哈 |
| **Let It Ride** | 1 | 随它去 |
| **Pai Gow Poker** | 1 | 比九扑克 |
| **Casino War** | 1 | 赌场战争 |
| **Red Dog** | 1 | 红狗 |
| **Video Poker** | 1 | 视频扑克 |
| **Hi-Lo** | 1 | 高低牌 |

---

## Quick Start

```bash
# Clone
git clone git@github.com:tsonglew/poker-skills.git

# Run any game
cd poker-skills
python3 games/holdem.py       # 德州扑克
python3 games/doudizhu.py     # 斗地主
python3 games/baccarat.py     # 百家乐
python3 games/blackjack.py    # 21点
# ... 更多游戏
```

---

## 🎮 游戏详解

### 🇨🇳 斗地主 (Doudizhu)

3人对战（1地主 vs 2农民），54张牌

```bash
python3 games/doudizhu.py

> bid 3          # 叫地主（叫3分）
> play 0,1,2     # 出牌（索引）
> pass           # 不出
> cards          # 查看手牌索引
```

**牌型**: 单张、对子、三张、三带一/二、顺子、连对、飞机、炸弹、王炸

---

### 🇨🇳 掼蛋 (Guandan)

4人2队对抗，108张牌（两副牌）

```bash
python3 games/guandan.py

> play 0,1,2     # 出牌
> pass           # 不出
> cards          # 查看手牌
> deal           # 新一局
```

**特色**: 从2打到A通关，同花顺 > 炸弹，王炸最大

---

### 🇨🇳 跑得快 (Pao De Kuai)

3人游戏，每人17张牌

```bash
python3 games/paodekuai.py
```

**规则**: 3♠先出，先出完牌者胜

---

### 🇨🇳 大老二 (Big Two)

4人游戏，每人13张牌

```bash
python3 games/bigtwo.py
```

**规则**: 3♦先出，2最大，♠最大花色

---

### 🌍 Texas Hold'em

```bash
python3 games/holdem.py

> deal           # 发牌
> call           # 跟注
> raise 20       # 加注$20
> fold           # 弃牌
```

---

### 🌍 Omaha

类似德州，但发4张底牌，必须用2张

```bash
python3 games/omaha.py
```

---

### 🌍 7-Card Stud

经典梭哈，7张牌，3张暗4张明

```bash
python3 games/stud.py
```

---

### 🌍 Pineapple

类似德州，发3张底牌，必须弃1张

```bash
python3 games/pineapple.py
```

---

### 🌍 Short Deck (6+)

36张牌(去掉2-5)，Flush > Full House

```bash
python3 games/shortdeck.py
```

---

### 🌍 Razz

低牌扑克，牌越小越好

```bash
python3 games/razz.py
```

---

### 🌍 Badugi

韩国低牌，4张不同花色不同点数

```bash
python3 games/badugi.py
```

---

### 🎰 Blackjack (21点)

```bash
python3 games/blackjack.py

> deal 10        # 发牌，赌$10
> hit            # 要牌
> stand          # 停牌
> double         # 双倍下注
```

---

### 🎰 Baccarat (百家乐)

```bash
python3 games/baccarat.py

> player         # 买闲
> banker         # 买庄
> tie            # 买和
```

---

### 🎰 Three Card Poker

```bash
python3 games/threecard.py

> play           # 继续（跟注）
> fold           # 弃牌
```

---

### 🎰 Caribbean Stud

```bash
python3 games/caribbean.py

> raise          # 加注
> fold           # 弃牌
```

---

### 🎰 Let It Ride

```bash
python3 games/letitride.py

> let-it-ride    # 保持下注
> pull           # 撤回下注
```

---

### 🎰 Pai Gow Poker

```bash
python3 games/paigow.py

# 自动分成5张高牌 + 2张低牌
```

---

### 🎰 Casino War

```bash
python3 games/war.py

> war            # 开战（加倍）
> surrender      # 投降（输一半）
```

---

### 🎰 Red Dog

```bash
python3 games/redog.py

> raise          # 加注
> stand          # 保持
```

---

### 🎰 Video Poker

```bash
python3 games/videopoker.py

> keep 0,1,2     # 保留指定牌
> draw           # 换牌
```

---

### 🎰 Hi-Lo

```bash
python3 games/hilo.py

> higher         # 猜更高
> lower          # 猜更低
> collect        # 收钱
```

---

## 牌型排名 (Hand Rankings)

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

---

## 项目结构

```
poker-skills/
├── SKILL.md           # Claude Code Skill
├── README.md          # 本文件
├── lib/
│   ├── __init__.py
│   ├── cards.py       # 卡牌工具
│   └── hands.py       # 牌型评估
└── games/
    ├── __init__.py
    ├── blackjack.py   # 21点
    ├── holdem.py      # 德州扑克
    ├── omaha.py       # 奥马哈
    ├── stud.py        # 七张牌梭哈
    ├── draw.py        # 五张抽牌
    ├── pineapple.py   # 菠萝扑克
    ├── shortdeck.py   # 短牌德州
    ├── razz.py        # 低牌
    ├── badugi.py      # 韩国低牌
    ├── baccarat.py    # 百家乐
    ├── threecard.py   # 三张扑克
    ├── caribbean.py   # 加勒比梭哈
    ├── letitride.py   # 随它去
    ├── paigow.py      # 比九扑克
    ├── war.py         # 赌场战争
    ├── redog.py       # 红狗
    ├── videopoker.py  # 视频扑克
    ├── hilo.py        # 高低牌
    ├── chinesepoker.py # 十三张
    ├── doudizhu.py    # 斗地主
    ├── guandan.py     # 掼蛋
    ├── paodekuai.py   # 跑得快
    └── bigtwo.py      # 大老二
```

---

## Features

- ✅ 24种游戏
- ✅ 完整游戏状态管理
- ✅ AI对手
- ✅ 筹码追踪
- ✅ 所有主流牌型
- ✅ 中西方游戏

## Requirements

- Python 3.8+
- 无外部依赖

## License

MIT

---

*Created by TsongLew <tsonglew@gmail.com>*

**Repository:** https://github.com/tsonglew/poker-skills
