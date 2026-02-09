"""
遊戲基類
提供所有遊戲的統一接口
"""
import pygame as pg
from abc import ABC, abstractmethod
from config import *


class GameBase(ABC):
    """遊戲基礎類別"""
    
    def __init__(self, screen, assets, **kwargs):
        """
        初始化遊戲
        
        Args:
            screen: pygame 顯示視窗
            assets: 資源管理器
            **kwargs: 其他遊戲設定參數
        """
        self.screen = screen
        self.assets = assets
        self.clock = pg.time.Clock()
        self.running = False
        self.result = {
            'quit': False,  # 是否退出整個程式
            'win': False,   # 是否獲勝
            'score': 0      # 分數
        }
    
    @abstractmethod
    def setup(self):
        """
        遊戲初始化設定
        在遊戲開始前呼叫
        """
        pass
    
    @abstractmethod
    def handle_events(self):
        """
        處理遊戲事件
        返回 False 表示遊戲結束
        """
        pass
    
    @abstractmethod
    def update(self):
        """
        更新遊戲邏輯
        返回 False 表示遊戲結束
        """
        pass
    
    @abstractmethod
    def draw(self):
        """繪製遊戲畫面"""
        pass
    
    def run(self):
        """
        執行遊戲主迴圈
        
        Returns:
            dict: 遊戲結果 {'quit': bool, 'win': bool, 'score': int}
        """
        self.setup()
        self.running = True
        
        while self.running:
            self.clock.tick(FPS)
            
            # 處理事件
            if not self.handle_events():
                self.running = False
                continue
            
            # 更新遊戲邏輯
            if not self.update():
                self.running = False
                continue
            
            # 繪製畫面
            self.draw()
            pg.display.update()
        
        return self.result
    
    def quit_game(self):
        """標記遊戲退出"""
        self.running = False
        self.result['quit'] = True