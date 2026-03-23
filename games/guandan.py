"""
掼蛋游戏引擎

江苏省淮安市传统扑克游戏，4人2对2对抗

Usage:
    python games/guandan.py
"""

import random
from typing import List, Optional, Tuple, Dict, Set
from dataclasses import dataclass, field
from enum import IntEnum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CardLevel(IntEnum):
    """掼蛋特殊：2是最大单牌，但A是顺子最大"""
    NORMAL = 0
    RED_JOKER = 1  # 大王
    BLACK_JOKER = 2  # 小王


@dataclass
class Card:
    """扑克牌"""
    rank: int  # 3-14 (3-10, J=11, Q=12, K=13, A=14), 2=15, 小王=16, 大王=17
    suit: int  # 1-4=黑红梅方, 0=王
    
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
        # 掼蛋中2最大，然后是王
        if self.rank == other.rank:
            return self.suit < other.suit
        return self.rank < other.rank
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False
    
    def __hash__(self):
        return hash((self.rank, self.suit))


class ComboType(IntEnum):
    """牌型"""
    INVALID = 0
    SINGLE = 1              # 单张
    PAIR = 2                # 对子
    TRIPLE = 3              # 三张
    TRIPLE_TWO = 4          # 三带二
    STRAIGHT = 5            # 顺子
    DOUBLE_STRAIGHT = 6     # 连对
    TRIPLE_STRAIGHT = 7     # 钢板（三顺）
    BOMB = 8                # 炸弹
    STRAIGHT_FLUSH = 9      # 同花顺
    FOUR_TWO = 10           # 四带二
    ROCKET = 11             # 王炸（四大天王）


@dataclass
class Combo:
    """牌型组合"""
    type: ComboType
    main_rank: int
    cards: List[Card]
    score: int = 0  # 牌力分数
    
    def __lt__(self, other):
        # 王炸最大
        if self.type == ComboType.ROCKET:
            return False
        if other.type == ComboType.ROCKET:
            return True
        
        # 同花顺 > 炸弹
        if self.type == ComboType.STRAIGHT_FLUSH and other.type == ComboType.BOMB:
            return False
        if other.type == ComboType.STRAIGHT_FLUSH and self.type == ComboType.BOMB:
            if len(self.cards) == 6:  # 6张炸弹比同花顺大
                return False
            return True
        
        # 炸弹比普通牌大，张数多的炸弹大
        if self.type == ComboType.BOMB and other.type not in (ComboType.BOMB, ComboType.STRAIGHT_FLUSH, ComboType.ROCKET):
            return False
        if other.type == ComboType.BOMB and self.type not in (ComboType.BOMB, ComboType.STRAIGHT_FLUSH, ComboType.ROCKET):
            return True
        
        # 同类型比较
        if self.type == other.type:
            if self.type in (ComboType.BOMB, ComboType.STRAIGHT_FLUSH):
                # 张数相同比点数
                if len(self.cards) == len(other.cards):
                    return self.main_rank < other.main_rank
                return len(self.cards) < len(other.cards)
            
            # 同张数比点数
            if len(self.cards) == len(other.cards):
                return self.main_rank < other.main_rank
        
        return True


def create_double_deck() -> List[Card]:
    """创建108张牌（两副牌）"""
    deck = []
    for _ in range(2):  # 两副
        for suit in range(1, 5):
            for rank in range(3, 16):  # 3到2
                deck.append(Card(rank, suit))
        deck.append(Card(16, 0))  # 小王
        deck.append(Card(17, 0))  # 大王
    return deck


def analyze(cards: List[Card]) -> Combo:
    """分析牌型"""
    if not cards:
        return Combo(ComboType.INVALID, 0, [])
    
    n = len(cards)
    ranks = sorted([c.rank for c in cards])
    suits = [c.suit for c in cards]
    
    # 统计
    rank_count: Dict[int, int] = {}
    suit_count: Dict[int, int] = {}
    for c in cards:
        rank_count[c.rank] = rank_count.get(c.rank, 0) + 1
        suit_count[c.suit] = suit_count.get(c.suit, 0) + 1
    
    counts = sorted(rank_count.values(), reverse=True)
    unique_ranks = sorted(rank_count.keys())
    
    # 王炸（四大天王）
    if rank_count.get(16, 0) == 2 and rank_count.get(17, 0) == 2:
        return Combo(ComboType.ROCKET, 17, cards)
    
    # 单张
    if n == 1:
        return Combo(ComboType.SINGLE, ranks[0], cards)
    
    # 对子
    if n == 2 and counts == [2]:
        return Combo(ComboType.PAIR, ranks[0], cards)
    
    # 三张
    if n == 3 and counts == [3]:
        return Combo(ComboType.TRIPLE, ranks[0], cards)
    
    # 三带二
    if n == 5 and sorted(counts) == [2, 3]:
        main = [r for r, c in rank_count.items() if c == 3][0]
        return Combo(ComboType.TRIPLE_TWO, main, cards)
    
    # 炸弹（4-8张相同）
    if 4 <= n <= 8 and counts[0] == n:
        return Combo(ComboType.BOMB, ranks[0], cards)
    
    # 四带二
    if n == 6 and counts == [4, 1, 1]:
        main = [r for r, c in rank_count.items() if c == 4][0]
        return Combo(ComboType.FOUR_TWO, main, cards)
    
    # 同花顺（5张以上同花色顺子）
    if n >= 5 and len(suit_count) == 1 and suits[0] != 0:
        if all(c == 1 for c in counts) and all(r <= 14 for r in ranks):
            if ranks[-1] - ranks[0] == n - 1:
                return Combo(ComboType.STRAIGHT_FLUSH, ranks[-1], cards)
    
    # 顺子（5张以上）
    if n >= 5 and all(c == 1 for c in counts):
        if all(r <= 14 for r in ranks):  # 不含2和王
            if ranks[-1] - ranks[0] == n - 1:
                return Combo(ComboType.STRAIGHT, ranks[-1], cards)
    
    # 连对（3对以上）
    if n >= 6 and n % 2 == 0 and all(c == 2 for c in counts):
        if all(r <= 14 for r in unique_ranks):
            if unique_ranks[-1] - unique_ranks[0] == len(unique_ranks) - 1:
                return Combo(ComboType.DOUBLE_STRAIGHT, unique_ranks[-1], cards)
    
    # 钢板（2个以上三张连续）
    if n >= 6 and n % 3 == 0 and all(c == 3 for c in counts):
        if all(r <= 14 for r in unique_ranks):
            if unique_ranks[-1] - unique_ranks[0] == len(unique_ranks) - 1:
                return Combo(ComboType.TRIPLE_STRAIGHT, unique_ranks[-1], cards)
    
    return Combo(ComboType.INVALID, 0, cards)


@dataclass
class Player:
    """玩家"""
    name: str
    team: int  # 0 or 1
    cards: List[Card] = field(default_factory=list)
    level: int = 2  # 当前级别（从2开始）
    is_human: bool = False
    
    def sort_cards(self):
        self.cards.sort()
    
    def remove_cards(self, cards: List[Card]):
        for card in cards:
            for i, c in enumerate(self.cards):
                if c == card:
                    self.cards.pop(i)
                    break


@dataclass 
class Team:
    """队伍"""
    id: int
    level: int = 2  # 级别（2-A）
    wins: int = 0   # 本局胜场
    
    LEVELS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # 2-A
    
    def promote(self):
        """升级"""
        idx = self.LEVELS.index(self.level)
        if idx < len(self.LEVELS) - 1:
            self.level = self.LEVELS[idx + 1]
    
    def level_name(self) -> str:
        if self.level == 11:
            return 'J'
        if self.level == 12:
            return 'Q'
        if self.level == 13:
            return 'K'
        if self.level == 14:
            return 'A'
        return str(self.level)


@dataclass
class GuandanGame:
    """掼蛋游戏"""
    deck: List[Card] = field(default_factory=create_double_deck)
    players: List[Player] = field(default_factory=list)
    teams: List[Team] = field(default_factory=lambda: [Team(0), Team(1)])
    current_player: int = 0
    last_player: int = -1
    last_combo: Optional[Combo] = None
    pass_count: int = 0
    round_winner: Optional[int] = None  # 本轮获胜者
    first_out: Optional[int] = None  # 第一个出完的
    phase: str = "playing"
    message: str = ""
    
    def add_player(self, name: str, team: int, is_human: bool = False):
        """添加玩家"""
        idx = len(self.players)
        self.players.append(Player(name=name, team=team, is_human=is_human))
    
    def start_game(self) -> str:
        """开始新一局"""
        # 重置牌组
        self.deck = create_double_deck()
        random.shuffle(self.deck)
        
        # 发牌（每人27张）
        for p in self.players:
            p.cards = []
        
        for i in range(27):
            for j in range(4):
                self.players[j].cards.append(self.deck.pop())
        
        for p in self.players:
            p.sort_cards()
        
        self.current_player = random.randint(0, 3)
        self.last_player = -1
        self.last_combo = None
        self.pass_count = 0
        self.round_winner = None
        self.first_out = None
        self.phase = "playing"
        self.message = ""
        
        return self._render()
    
    def play(self, indices: List[int]) -> str:
        """出牌"""
        if self.phase != "playing":
            return "现在不能出牌"
        
        player = self.players[self.current_player]
        
        if not indices:
            return self.pass_turn()
        
        try:
            cards = [player.cards[i] for i in indices]
        except IndexError:
            return "无效的牌索引"
        
        combo = analyze(cards)
        
        if combo.type == ComboType.INVALID:
            return "无效牌型"
        
        # 检查能否打过
        if self.last_combo and self.last_player != self.current_player:
            if combo < self.last_combo:
                return "打不过上家"
        
        # 出牌
        player.remove_cards(cards)
        self.last_combo = combo
        self.last_player = self.current_player
        self.pass_count = 0
        
        self.message = f"{player.name} 出: {' '.join(str(c) for c in cards)}"
        
        # 检查是否出完
        if not player.cards:
            if self.first_out is None:
                self.first_out = self.current_player
            
            # 检查是否一方都出完
            team = player.team
            teammate = [i for i, p in enumerate(self.players) if p.team == team and i != self.current_player][0]
            
            if not self.players[teammate].cards:
                # 一方都出完，结算
                return self._end_round(team)
        
        self._next_player()
        return self._render()
    
    def pass_turn(self) -> str:
        """不出"""
        if self.last_player == self.current_player or self.last_player == -1:
            return "必须出牌"
        
        self.pass_count += 1
        self.message = f"{self.players[self.current_player].name} 不出"
        
        if self.pass_count >= 3:
            self.last_combo = None
            self.pass_count = 0
        
        self._next_player()
        return self._render()
    
    def _next_player(self):
        """下一个玩家"""
        self.current_player = (self.current_player + 1) % 4
        
        # 跳过已出完的
        count = 0
        while not self.players[self.current_player].cards and count < 4:
            self.current_player = (self.current_player + 1) % 4
            count += 1
    
    def _end_round(self, winner_team: int) -> str:
        """结束本轮"""
        self.phase = "ended"
        
        winner = self.teams[winner_team]
        loser = self.teams[1 - winner_team]
        
        # 计算升级数
        upgrade = 1
        
        # 双下（对手都没出完）
        loser_cards = sum(len(self.players[i].cards) for i in [0, 2] if winner_team == 1 else [1, 3])
        if loser_cards == 0:
            upgrade = 3  # 双下升3级
        
        winner.wins += 1
        for _ in range(upgrade):
            winner.promote()
        
        self.message = f"🎉 {['红队', '蓝队'][winner_team]}获胜！升{upgrade}级！当前级别: {winner.level_name()}"
        
        # 检查是否通关
        if winner.level == 14 and winner.wins >= 1:
            self.message += f"\n🏆 {['红队', '蓝队'][winner_team]}通关获胜！游戏结束！"
        
        return self._render()
    
    def _render(self) -> str:
        """渲染"""
        lines = [
            "",
            "═════════════════════════════════════════════════════════════",
            "                      🃏 掼 蛋 🃏",
            "═════════════════════════════════════════════════════════════",
        ]
        
        # 队伍信息
        lines.append(f"  红队[级别{self.teams[0].level_name()}] vs 蓝队[级别{self.teams[1].level_name()}]")
        lines.append("───────────────────────────────────────────────────────────────")
        
        # 玩家
        team_names = ["红", "蓝"]
        for i, p in enumerate(self.players):
            marker = "→ " if i == self.current_player and self.phase == "playing" else "  "
            team = team_names[p.team]
            cards = " ".join(str(c) for c in p.cards) if p.is_human or self.phase == "ended" else f"[{len(p.cards)}张]"
            lines.append(f"{marker}{p.name}({team}队): {cards}")
        
        lines.append("───────────────────────────────────────────────────────────────")
        
        if self.last_combo:
            lines.append(f"  当前牌型: {ComboType(self.last_combo.type).name}")
        
        if self.message:
            lines.append(f"  {self.message}")
        
        if self.phase == "playing":
            current = self.players[self.current_player]
            if current.is_human:
                lines.append("  命令: play 0,1,2 (出牌) | pass (不出) | cards (查看)")
        elif self.phase == "ended":
            lines.append("  输入 'deal' 开始下一局")
        
        lines.append("═════════════════════════════════════════════════════════════")
        
        return "\n".join(lines)


def play_interactive():
    """交互式掼蛋"""
    game = GuandanGame()
    
    print("\n🃏 欢迎来到掼蛋！\n")
    
    # 4人2队
    game.add_player("你", 0, is_human=True)
    game.add_player("张三", 1)
    game.add_player("队友", 0)
    game.add_player("李四", 1)
    
    print("红队: 你, 队友")
    print("蓝队: 张三, 李四\n")
    
    print(game.start_game())
    
    while True:
        try:
            current = game.players[game.current_player]
            
            # AI
            if not current.is_human and game.phase == "playing":
                import time
                time.sleep(0.5)
                
                if game.last_combo is None or game.last_player == game.current_player:
                    # 必须出牌，出最小的
                    game.play([0])
                else:
                    # 尝试打
                    found = False
                    for i in range(len(current.cards)):
                        combo = analyze([current.cards[i]])
                        if combo.type != ComboType.INVALID and not (combo < game.last_combo):
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
            elif action == "play":
                indices = [int(x) for x in cmd[1].split(",")] if len(cmd) > 1 else []
                print(game.play(indices))
            elif action == "pass":
                print(game.pass_turn())
            elif action == "cards":
                p = game.players[0]
                print(f"\n你的牌: {' '.join(str(c) for c in p.cards)}")
                idx = "   ".join(str(i).ljust(3) for i in range(len(p.cards)))
                print(f"索引:   {idx}")
            elif action == "help":
                print("\n命令: deal, play 0,1,2, pass, cards, quit")
            else:
                print(f"未知: {action}")
        
        except (ValueError, IndexError) as e:
            print(f"错误: {e}")
        except KeyboardInterrupt:
            print("\n\n游戏结束")
            break


if __name__ == "__main__":
    play_interactive()
