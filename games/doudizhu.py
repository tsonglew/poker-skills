"""
斗地主游戏引擎

经典中国扑克游戏，3人对战（1地主 vs 2农民）

Usage:
    python games/doudizhu.py
"""

import random
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass, field
from enum import IntEnum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CardType(IntEnum):
    """牌型"""
    INVALID = 0
    SINGLE = 1           # 单张
    PAIR = 2             # 对子
    TRIPLE = 3           # 三张
    TRIPLE_ONE = 4       # 三带一
    TRIPLE_PAIR = 5      # 三带一对
    STRAIGHT = 6         # 顺子
    STRAIGHT_PAIR = 7    # 连对
    PLANE = 8            # 飞机不带
    PLANE_SINGLE = 9     # 飞机带单
    PLANE_PAIR = 10      # 飞机带对
    FOUR_TWO = 11        # 四带二单
    FOUR_PAIR = 12       # 四带二对
    BOMB = 13            # 炸弹
    ROCKET = 14          # 王炸


@dataclass
class Card:
    """扑克牌"""
    rank: int  # 3-15 (3-10, J=11, Q=12, K=13, A=14, 2=15), 小王=16, 大王=17
    suit: int = 0  # 0=无, 1-4=黑红梅方
    
    # 牌面显示
    RANK_NAMES = {
        3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
        11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2', 16: '小王', 17: '大王'
    }
    
    SUIT_NAMES = {0: '', 1: '♠', 2: '♥', 3: '♣', 4: '♦'}
    
    def __str__(self):
        if self.rank >= 16:
            return self.RANK_NAMES[self.rank]
        return f"{self.RANK_NAMES[self.rank]}{self.SUIT_NAMES.get(self.suit, '')}"
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        return self.rank < other.rank
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank
        return False
    
    def __hash__(self):
        return hash(self.rank)


def create_deck() -> List[Card]:
    """创建54张牌的斗地主牌组"""
    deck = []
    
    # 3-2 四种花色
    for suit in range(1, 5):
        for rank in range(3, 16):  # 3到2
            deck.append(Card(rank, suit))
    
    # 大小王
    deck.append(Card(16, 0))  # 小王
    deck.append(Card(17, 0))  # 大王
    
    return deck


@dataclass
class CardCombo:
    """牌型组合"""
    type: CardType
    main_rank: int  # 主牌点数
    cards: List[Card]
    
    def __lt__(self, other):
        # 王炸最大
        if self.type == CardType.ROCKET:
            return False
        if other.type == CardType.ROCKET:
            return True
        
        # 炸弹比普通牌大
        if self.type == CardType.BOMB and other.type != CardType.BOMB:
            return False
        if other.type == CardType.BOMB and self.type != CardType.BOMB:
            return True
        
        # 同类型比点数
        if self.type == other.type and len(self.cards) == len(other.cards):
            return self.main_rank < other.main_rank
        
        return True  # 不同类型不能比较，默认小


def analyze_cards(cards: List[Card]) -> CardCombo:
    """分析牌型"""
    if not cards:
        return CardCombo(CardType.INVALID, 0, [])
    
    ranks = sorted([c.rank for c in cards])
    n = len(cards)
    
    # 统计各点数出现次数
    count_map: Dict[int, int] = {}
    for r in ranks:
        count_map[r] = count_map.get(r, 0) + 1
    
    counts = sorted(count_map.values(), reverse=True)
    unique_ranks = sorted(count_map.keys())
    
    # 王炸
    if ranks == [16, 17]:
        return CardCombo(CardType.ROCKET, 17, cards)
    
    # 单张
    if n == 1:
        return CardCombo(CardType.SINGLE, ranks[0], cards)
    
    # 对子
    if n == 2 and counts == [2]:
        return CardCombo(CardType.PAIR, ranks[0], cards)
    
    # 三张
    if n == 3 and counts == [3]:
        return CardCombo(CardType.TRIPLE, ranks[0], cards)
    
    # 炸弹
    if n == 4 and counts == [4]:
        return CardCombo(CardType.BOMB, ranks[0], cards)
    
    # 三带一
    if n == 4 and counts == [3, 1]:
        main_rank = [r for r, c in count_map.items() if c == 3][0]
        return CardCombo(CardType.TRIPLE_ONE, main_rank, cards)
    
    # 三带一对
    if n == 5 and counts == [3, 2]:
        main_rank = [r for r, c in count_map.items() if c == 3][0]
        return CardCombo(CardType.TRIPLE_PAIR, main_rank, cards)
    
    # 四带二单
    if n == 6 and counts == [4, 1, 1]:
        main_rank = [r for r, c in count_map.items() if c == 4][0]
        return CardCombo(CardType.FOUR_TWO, main_rank, cards)
    
    # 四带二对
    if n == 8 and counts == [4, 2, 2]:
        main_rank = [r for r, c in count_map.items() if c == 4][0]
        return CardCombo(CardType.FOUR_PAIR, main_rank, cards)
    
    # 顺子 (5-12张，不含2和王)
    if n >= 5 and n <= 12 and all(c == 1 for c in counts):
        if all(r <= 14 for r in ranks):  # 不含2和王
            if ranks[-1] - ranks[0] == n - 1:  # 连续
                return CardCombo(CardType.STRAIGHT, ranks[-1], cards)
    
    # 连对 (6+张，成对连续)
    if n >= 6 and n % 2 == 0 and all(c == 2 for c in counts):
        if all(r <= 14 for r in unique_ranks):  # 不含2和王
            if unique_ranks[-1] - unique_ranks[0] == len(unique_ranks) - 1:
                return CardCombo(CardType.STRAIGHT_PAIR, unique_ranks[-1], cards)
    
    # 飞机不带 (6+张，3张连续)
    if n >= 6 and n % 3 == 0 and all(c == 3 for c in counts):
        if all(r <= 14 for r in unique_ranks):
            if unique_ranks[-1] - unique_ranks[0] == len(unique_ranks) - 1:
                return CardCombo(CardType.PLANE, unique_ranks[-1], cards)
    
    # 飞机带单翅膀
    plane_count = sum(1 for c in counts if c == 3)
    if plane_count >= 2:
        triples = sorted([r for r, c in count_map.items() if c == 3])
        if triples[-1] - triples[0] == len(triples) - 1 and all(r <= 14 for r in triples):
            wings = n - plane_count * 3
            if wings == plane_count:  # 带单
                return CardCombo(CardType.PLANE_SINGLE, triples[-1], cards)
            if wings == plane_count * 2:  # 带对
                return CardCombo(CardType.PLANE_PAIR, triples[-1], cards)
    
    return CardCombo(CardType.INVALID, 0, cards)


def can_beat(play: CardCombo, last: Optional[CardCombo]) -> bool:
    """判断能否打过上家"""
    if last is None:
        return play.type != CardType.INVALID
    
    if play.type == CardType.ROCKET:
        return True
    
    if play.type == CardType.BOMB:
        if last.type == CardType.ROCKET:
            return False
        if last.type == CardType.BOMB:
            return play.main_rank > last.main_rank
        return True
    
    # 同类型同数量才能比较
    if play.type == last.type and len(play.cards) == len(last.cards):
        return play.main_rank > last.main_rank
    
    return False


@dataclass
class Player:
    """玩家"""
    name: str
    cards: List[Card] = field(default_factory=list)
    is_landlord: bool = False
    is_human: bool = False
    last_play: Optional[CardCombo] = None
    
    def sort_cards(self):
        """排序手牌"""
        self.cards.sort(key=lambda c: (c.rank, c.suit))
    
    def remove_cards(self, cards: List[Card]):
        """移除打出的牌"""
        for card in cards:
            for i, c in enumerate(self.cards):
                if c.rank == card.rank and c.suit == card.suit:
                    self.cards.pop(i)
                    break


@dataclass
class DoudizhuGame:
    """斗地主游戏"""
    deck: List[Card] = field(default_factory=create_deck)
    players: List[Player] = field(default_factory=list)
    bottom_cards: List[Card] = field(default_factory=list)  # 底牌
    current_player: int = 0
    last_player: int = -1  # 上一个出牌的人
    last_combo: Optional[CardCombo] = None
    pass_count: int = 0
    phase: str = "bidding"  # bidding, playing, ended
    landlord_candidate: int = 0
    bid_value: int = 0  # 叫分 1-3
    message: str = ""
    
    def add_player(self, name: str, is_human: bool = False):
        """添加玩家"""
        self.players.append(Player(name=name, is_human=is_human))
    
    def start_game(self) -> str:
        """开始游戏"""
        if len(self.players) != 3:
            return "斗地主需要3名玩家"
        
        # 洗牌发牌
        random.shuffle(self.deck)
        
        for p in self.players:
            p.cards = []
            p.is_landlord = False
            p.last_play = None
        
        # 每人17张
        for i in range(17):
            for j in range(3):
                self.players[j].cards.append(self.deck.pop())
        
        # 3张底牌
        self.bottom_cards = self.deck[:3]
        
        # 排序
        for p in self.players:
            p.sort_cards()
        
        self.phase = "bidding"
        self.current_player = random.randint(0, 2)
        self.landlord_candidate = self.current_player
        self.bid_value = 0
        self.message = ""
        
        return self._render()
    
    def bid(self, value: int) -> str:
        """叫地主 (0=不叫, 1-3=叫分)"""
        if self.phase != "bidding":
            return "现在不是叫地主阶段"
        
        player = self.players[self.current_player]
        
        if value > 0:
            if value <= self.bid_value:
                return f"必须叫比{self.bid_value}更高的分"
            self.bid_value = value
            self.landlord_candidate = self.current_player
            self.message = f"{player.name} 叫 {value} 分"
            
            if value == 3:
                # 叫3分直接成为地主
                return self._become_landlord()
        else:
            self.message = f"{player.name} 不叫"
        
        self.current_player = (self.current_player + 1) % 3
        
        # 一轮结束
        if self.current_player == (self.landlord_candidate + 1) % 3:
            if self.bid_value == 0:
                # 没人叫，重新发牌
                self.message = "没人叫地主，重新发牌"
                return self.start_game()
            else:
                return self._become_landlord()
        
        return self._render()
    
    def _become_landlord(self) -> str:
        """成为地主"""
        landlord = self.players[self.landlord_candidate]
        landlord.is_landlord = True
        
        # 地主获得底牌
        landlord.cards.extend(self.bottom_cards)
        landlord.sort_cards()
        
        self.phase = "playing"
        self.current_player = self.landlord_candidate
        self.last_player = -1
        self.last_combo = None
        self.pass_count = 0
        
        self.message = f"地主是 {landlord.name}，底牌: {' '.join(str(c) for c in self.bottom_cards)}"
        
        return self._render()
    
    def play(self, card_indices: List[int]) -> str:
        """出牌"""
        if self.phase != "playing":
            return "现在不是出牌阶段"
        
        player = self.players[self.current_player]
        
        if not card_indices:
            return self.pass_turn()
        
        # 获取要打的牌
        try:
            cards_to_play = [player.cards[i] for i in card_indices]
        except IndexError:
            return "无效的牌索引"
        
        # 分析牌型
        combo = analyze_cards(cards_to_play)
        
        if combo.type == CardType.INVALID:
            return "无效的牌型"
        
        # 检查能否打过上家
        if self.last_combo and self.last_player != self.current_player:
            if not can_beat(combo, self.last_combo):
                return "打不过上家"
        
        # 出牌
        player.remove_cards(cards_to_play)
        player.last_play = combo
        self.last_combo = combo
        self.last_player = self.current_player
        self.pass_count = 0
        
        self.message = f"{player.name} 出牌: {' '.join(str(c) for c in cards_to_play)}"
        
        # 检查是否获胜
        if not player.cards:
            self.phase = "ended"
            if player.is_landlord:
                self.message = f"🎉 地主 {player.name} 获胜！"
            else:
                farmers = [p.name for p in self.players if not p.is_landlord]
                self.message = f"🎉 农民 {' & '.join(farmers)} 获胜！"
            return self._render()
        
        self.current_player = (self.current_player + 1) % 3
        return self._render()
    
    def pass_turn(self) -> str:
        """不出"""
        if self.phase != "playing":
            return "现在不是出牌阶段"
        
        if self.last_player == self.current_player or self.last_player == -1:
            return "你必须出牌"
        
        player = self.players[self.current_player]
        player.last_play = None
        self.pass_count += 1
        self.message = f"{player.name} 不出"
        
        # 两人都不出，清空上家
        if self.pass_count >= 2:
            self.last_combo = None
            self.pass_count = 0
        
        self.current_player = (self.current_player + 1) % 3
        return self._render()
    
    def get_valid_plays(self) -> List[List[int]]:
        """获取所有可打的牌组合"""
        player = self.players[self.current_player]
        cards = player.cards
        
        # 简化：返回所有可能的牌型组合索引
        # 实际应该更智能
        valid = []
        
        # 单张
        for i in range(len(cards)):
            valid.append([i])
        
        # 对子、三张等需要更多逻辑
        # 这里简化处理
        
        return valid
    
    def _render(self) -> str:
        """渲染游戏状态"""
        lines = [
            "",
            "═════════════════════════════════════════════════════════",
            "                    🃏 斗 地 主 🃏",
            "═════════════════════════════════════════════════════════",
        ]
        
        if self.phase == "bidding":
            lines.append(f"  【叫地主阶段】 当前叫分: {self.bid_value if self.bid_value > 0 else '无'}")
        elif self.phase == "playing":
            lines.append(f"  【出牌阶段】")
        else:
            lines.append(f"  【游戏结束】")
        
        lines.append("───────────────────────────────────────────────────────────")
        
        # 显示玩家
        for i, player in enumerate(self.players):
            marker = "→ " if i == self.current_player else "  "
            role = "👑地主" if player.is_landlord else "👨‍🌾农民"
            cards_str = " ".join(str(c) for c in player.cards)
            
            if player.is_human or self.phase == "ended":
                lines.append(f"{marker}{player.name}({role}): {cards_str}")
            else:
                lines.append(f"{marker}{player.name}({role}): [{len(player.cards)}张]")
        
        lines.append("───────────────────────────────────────────────────────────")
        
        if self.bottom_cards and self.phase != "bidding":
            bottom = " ".join(str(c) for c in self.bottom_cards)
            lines.append(f"  底牌: {bottom}")
        
        if self.last_combo and self.phase == "playing":
            lines.append(f"  当前牌: {CardType(self.last_combo.type).name}")
        
        if self.message:
            lines.append(f"  {self.message}")
        
        # 命令提示
        if self.phase == "bidding":
            current = self.players[self.current_player]
            if current.is_human:
                lines.append("  命令: bid 0 (不叫) | bid 1-3 (叫分)")
        elif self.phase == "playing":
            current = self.players[self.current_player]
            if current.is_human:
                lines.append("  命令: play 0,1,2 (出牌索引) | pass (不出)")
        elif self.phase == "ended":
            lines.append("  输入 'deal' 开始新一局")
        
        lines.append("═════════════════════════════════════════════════════════")
        
        return "\n".join(lines)


def play_interactive():
    """交互式游戏"""
    game = DoudizhuGame()
    
    print("\n🃏 欢迎来到斗地主！\n")
    
    game.add_player("你", is_human=True)
    game.add_player("张三")
    game.add_player("李四")
    
    print(game.start_game())
    
    while True:
        try:
            current = game.players[game.current_player]
            
            # AI 自动操作
            if not current.is_human and game.phase != "ended":
                import time
                time.sleep(0.8)
                
                if game.phase == "bidding":
                    # 简单AI：随机叫或不叫
                    if game.bid_value < 2 and random.random() < 0.5:
                        game.bid(game.bid_value + 1)
                    else:
                        game.bid(0)
                elif game.phase == "playing":
                    # 简单AI：能出就出最小的单张
                    if game.last_combo is None or game.last_player == game.current_player:
                        game.play([0])  # 出最小的一张
                    else:
                        # 尝试找能打的牌
                        found = False
                        for i in range(len(current.cards)):
                            combo = analyze_cards([current.cards[i]])
                            if can_beat(combo, game.last_combo):
                                game.play([i])
                                found = True
                                break
                        if not found:
                            game.pass_turn()
                
                print(game._render())
                continue
            
            cmd = input("\n> ").strip().lower().split()
            if not cmd:
                continue
            
            action = cmd[0]
            
            if action in ["q", "quit", "exit"]:
                print("\n游戏结束")
                break
            elif action == "deal":
                print(game.start_game())
            elif action == "bid":
                value = int(cmd[1]) if len(cmd) > 1 else 0
                result = game.bid(value)
                print(result)
            elif action == "play":
                indices = [int(x) for x in cmd[1].split(",")] if len(cmd) > 1 else []
                result = game.play(indices)
                print(result)
            elif action == "pass":
                result = game.pass_turn()
                print(result)
            elif action == "cards":
                player = game.players[0]
                print(f"\n你的牌: {' '.join(str(c) for c in player.cards)}")
                print(f"索引:   {'   '.join(str(i) for i in range(len(player.cards)))}")
            elif action == "help":
                print("\n命令:")
                print("  deal          - 开始新游戏")
                print("  bid 0-3       - 叫地主(0=不叫)")
                print("  play 0,1,2    - 出牌(牌的索引)")
                print("  pass          - 不出")
                print("  cards         - 查看手牌和索引")
                print("  quit          - 退出")
            else:
                print(f"未知命令: {action}")
        
        except (ValueError, IndexError) as e:
            print(f"错误: {e}")
        except KeyboardInterrupt:
            print("\n\n游戏结束")
            break


if __name__ == "__main__":
    play_interactive()
