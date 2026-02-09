"""
遊戲模組
包含所有遊戲的實作
"""
from games.game_g import run_game_g
from games.game_a import run_game_a
from games.game_m import run_game_m
from games.game_e import run_game_e

__all__ = [
    'run_game_g',
    'run_game_a',
    'run_game_m',
    'run_game_e'
]