"""
遊戲 E - 音樂彩蛋
播放音樂並顯示特殊訊息的彩蛋遊戲
"""
import pygame as pg
from config import *
from utils import draw_text
from games.game_base import GameBase


class GameE(GameBase):
    """遊戲E主類"""
    
    def __init__(self, screen, assets, background='background'):
        super().__init__(screen, assets)
        self.background_name = background
        self.game_time = 0
        self.first_quit_attempt = True
        self.ba_sound_played = False
        
        # 音樂時長（秒）* FPS
        self.music_duration = (3 * 60 + 39) * FPS
    
    def setup(self):
        """初始化遊戲"""
        self.game_time = 0
        self.first_quit_attempt = True
        self.ba_sound_played = False
        
        # 停止背景音樂
        pg.mixer.music.set_volume(0)
        
        # 播放 BA 音效
        if not self.ba_sound_played:
            ba_sound = self.assets.get_sound('ba')
            ba_sound.play()
            self.ba_sound_played = True
    
    def handle_events(self):
        """處理事件"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # 每次嘗試退出都顯示警告，但不真正退出
                self.first_quit_attempt = False
                # 不返回 False，繼續遊戲
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    # 按 B 不會退出，只是顯示訊息
                    pass
        
        return True
    
    def update(self):
        """更新遊戲邏輯"""
        self.game_time += 1
        
        # 音樂播放完畢後退出
        if self.game_time > self.music_duration:
            return False
        
        return True
    
    def draw(self):
        """繪製畫面"""
        background = self.assets.get_image(self.background_name)
        self.screen.blit(background, (0, 0))
        
        if self.first_quit_attempt:
            # 正常顯示
            draw_text(
                self.screen, 
                'there is no gameE yet', 
                40, 
                WIDTH / 2, 
                HEIGHT * 1 / 8
            )
            draw_text(
                self.screen, 
                'listen to the song', 
                40, 
                WIDTH / 2, 
                HEIGHT * 2 / 8
            )
            draw_text(
                self.screen, 
                'for Back press " B " ', 
                40, 
                WIDTH / 2, 
                HEIGHT * 4 / 8
            )
        else:
            # 嘗試退出後顯示警告
            draw_text(
                self.screen, 
                'I     SAY', 
                80, 
                WIDTH / 2, 
                HEIGHT * 2 / 8
            )
            draw_text(
                self.screen, 
                'WAIT!!!!', 
                80, 
                WIDTH / 2, 
                HEIGHT * 4 / 8
            )
            draw_text(
                self.screen, 
                'you can not leave ', 
                80, 
                WIDTH / 2, 
                HEIGHT * 6 / 8
            )


def run_game_e(screen, assets, background='background'):
    """
    執行遊戲E
    
    Args:
        screen: pygame 顯示視窗
        assets: 資源管理器
        background: 背景圖片名稱
    
    Returns:
        dict: 遊戲結果
    """
    game = GameE(screen, assets, background)
    return game.run()