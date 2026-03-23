---
name: poker-skills
description: Play poker games in Claude Code. Triggers when user asks to play poker, blackjack, Texas Hold'em, Doudizhu (斗地主), Guandan (掼蛋), or card games.
version: 1.1.0
author: TsongLew <tsonglew@gmail.com>
---

# 🃏 Poker & Card Games Skills

Play classic poker and Chinese card games directly in Claude Code!

## Games

| Game | Type | Players | Run |
|------|------|---------|-----|
| **Blackjack** | 西方 | 1 vs Dealer | `python games/blackjack.py` |
| **Texas Hold'em** | 西方 | 4+ | `python games/holdem.py` |
| **Five Card Draw** | 西方 | 3+ | `python games/draw.py` |
| **斗地主** | 中国 | 3 (1v2) | `python games/doudizhu.py` |
| **掼蛋** | 中国 | 4 (2v2) | `python games/guandan.py` |

---

## 🇨🇳 中国棋牌

### 斗地主

经典3人对战扑克游戏（1地主 vs 2农民）

```
python games/doudizhu.py
```

**规则：**
- 54张牌（含大小王）
- 每人17张，3张底牌归地主
- 叫地主（1-3分）
- 地主先出，目标先出完牌

**牌型：**
| 牌型 | 说明 |
|------|------|
| 单张 | 任意一张 |
| 对子 | 两张相同 |
| 三张 | 三张相同 |
| 三带一/二 | 三张+单/对 |
| 顺子 | 5+连续（不含2和王）|
| 连对 | 3+连续对子 |
| 飞机 | 2+连续三张 |
| 炸弹 | 四张相同 |
| 王炸 | 大小王 |

**命令：**
```
bid 0-3      # 叫地主（0=不叫）
play 0,1,2   # 出牌（索引）
pass         # 不出
cards        # 查看手牌索引
```

---

### 掼蛋

江苏省传统4人扑克游戏（2对2对抗）

```
python games/guandan.py
```

**规则：**
- 108张牌（两副牌+4王）
- 每人27张
- 2队对抗，打完升级
- 从2打到A通关

**特色：**
- 同花顺 > 炸弹
- 6张+炸弹 > 同花顺
- 王炸（四大天王）最大
- 双下升3级

**牌型：**
| 牌型 | 说明 |
|------|------|
| 单张/对子/三张 | 基础牌型 |
| 三带二 | 三张+一对 |
| 顺子 | 5+连续（A最大）|
| 连对 | 3+连续对子 |
| 钢板 | 2+连续三张 |
| 炸弹 | 4-8张相同 |
| 同花顺 | 5+同花顺子 |
| 四带二 | 四张+两单 |
| 王炸 | 4张王 |

**命令：**
```
play 0,1,2   # 出牌
pass         # 不出
cards        # 查看手牌
deal         # 新一局
```

---

## 🌍 西方扑克

### Blackjack (21点)

```
python games/blackjack.py
```

**命令：** `deal [bet]`, `hit`, `stand`, `double`

### Texas Hold'em

```
python games/holdem.py
```

**命令：** `deal`, `fold`, `check`, `call`, `raise [amount]`

### Five Card Draw

```
python games/draw.py
```

**命令：** `deal`, `fold`, `call`, `draw 0,2,4`, `stand-pat`

---

## 牌型大小（通用）

**西方扑克：**
1. 🏆 皇家同花顺
2. 🔥 同花顺
3. 💪 四条
4. 🏠 葫芦
5. 💎 同花
6. 📈 顺子
7. 🎯 三条
8. ✌️ 两对
9. 👆 一对
10. 🃏 高牌

**斗地主：** 王炸 > 炸弹 > 其他（同类型比点数，2最大）

**掼蛋：** 王炸 > 6张+炸弹 > 同花顺 > 炸弹 > 其他

---

## 使用示例

```
你: 玩斗地主

Claude: 
═════════════════════════════════════════════════════════
                    🃏 斗 地 主 🃏
═════════════════════════════════════════════════════════
  【叫地主阶段】 当前叫分: 无
───────────────────────────────────────────────────────────
→ 你(👨‍🌾农民): 3♠ 4♥ 5♣ 6♦ 7♠ 9♥ J♣ Q♦ K♠ A♥ 2♣
  张三(👨‍🌾农民): [13张]
  李四(👨‍🌾农民): [13张]
───────────────────────────────────────────────────────────
  命令: bid 0 (不叫) | bid 1-3 (叫分)
═════════════════════════════════════════════════════════
```

---

## 文件结构

```
poker-skills/
├── SKILL.md
├── README.md
├── lib/
│   ├── cards.py
│   └── hands.py
└── games/
    ├── blackjack.py
    ├── holdem.py
    ├── draw.py
    ├── doudizhu.py    # 斗地主
    └── guandan.py     # 掼蛋
```

---

*Created by TsongLew <tsonglew@gmail.com>*
