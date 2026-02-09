"""
資源管理類別
負責載入並管理所有遊戲資源（圖片、音效等）
"""
import pygame as pg
import os
from config import *


class Assets:
    """遊戲資源管理器"""
    
    def __init__(self):
        """初始化並載入所有資源"""
        self.images = {}
        self.sounds = {}
        self.animations = {}
        
        self._load_images()
        self._load_sounds()
        self._load_animations()
    
    def _load_images(self):
        """載入所有圖片資源"""
        # 背景圖片
        self.images['background'] = pg.transform.scale(
            pg.image.load(os.path.join(IMG_DIR, 'background.png')).convert(),
            (WIDTH, HEIGHT)
        )
        self.images['background_new'] = pg.transform.scale(
            pg.image.load(os.path.join(IMG_DIR, 'background_new.png')).convert(),
            (WIDTH, HEIGHT)
        )
        
        # 玩家圖片
        self.images['player'] = pg.image.load(
            os.path.join(IMG_DIR, 'player.png')
        ).convert()
        self.images['player_mini'] = pg.transform.scale(
            self.images['player'], (25, 19)
        )
        self.images['player_mini'].set_colorkey(BLACK)
        
        # 蛇圖片
        self.images['snake_imgs'] = []
        for i in range(2):
            img = pg.image.load(os.path.join(IMG_DIR, f'snake_img{i}.png')).convert()
            self.images['snake_imgs'].append(img)
        
        # 壞蛇圖片（PVG遊戲用）
        self.images['badsnake_imgs'] = []
        for i in range(8):
            img = pg.image.load(os.path.join(IMG_DIR, f'badsnake_img{i}.png')).convert()
            self.images['badsnake_imgs'].append(img)
        
        # 樹莓圖片
        self.images['raspberry_imgs'] = []
        for i in range(4):
            img = pg.image.load(os.path.join(IMG_DIR, f'raspberry_img{i}.png')).convert()
            self.images['raspberry_imgs'].append(img)
        
        # 植物圖片
        self.images['plant1'] = pg.transform.scale(
            pg.image.load(os.path.join(IMG_DIR, 'goodplant1.png')).convert(),
            (50, 38)
        )
        self.images['plant2'] = pg.transform.scale(
            pg.image.load(os.path.join(IMG_DIR, 'goodplant2.png')).convert(),
            (50, 38)
        )
        self.images['plant_board'] = pg.image.load(
            os.path.join(IMG_DIR, 'goodplant_board.png')
        ).convert()
        
        # 車圖片
        self.images['car'] = pg.image.load(
            os.path.join(IMG_DIR, 'car_img.png')
        ).convert()
        
        # PVG背景
        self.images['pvg_bg'] = pg.image.load(
            os.path.join(IMG_DIR, 'game_m_PVGbackground.png')
        ).convert()
    
    def _load_sounds(self):
        """載入所有音效資源"""
        # 音效
        self.sounds['shoot'] = pg.mixer.Sound(
            os.path.join(SOUND_DIR, 'shoot.wav')
        )
        self.sounds['die'] = pg.mixer.Sound(
            os.path.join(SOUND_DIR, 'die.mp3')
        )
        self.sounds['expl'] = pg.mixer.Sound(
            os.path.join(SOUND_DIR, 'rumble.ogg')
        )
        self.sounds['ba'] = pg.mixer.Sound(
            os.path.join(SOUND_DIR, 'BA.mp3')
        )
        
        # 吃樹莓音效
        self.sounds['eat_raspberry'] = [
            pg.mixer.Sound(os.path.join(SOUND_DIR, 'eat_raspberry0.mp3')),
            pg.mixer.Sound(os.path.join(SOUND_DIR, 'eat_raspberry1.mp3'))
        ]
        
        # 背景音樂
        pg.mixer.music.load(os.path.join(SOUND_DIR, 'background.mp3'))
        pg.mixer.music.set_volume(0.4)
    
    def _load_animations(self):
        """載入動畫資源"""
        self.animations['expl'] = {
            'lg': [],
            'sm': [],
            'player': []
        }
        
        for i in range(9):
            # 爆炸動畫
            expl_img = pg.image.load(
                os.path.join(IMG_DIR, f'expl{i}.png')
            ).convert()
            expl_img.set_colorkey(BLACK)
            self.animations['expl']['lg'].append(
                pg.transform.scale(expl_img, (75, 75))
            )
            self.animations['expl']['sm'].append(
                pg.transform.scale(expl_img, (30, 30))
            )
            
            # 玩家爆炸動畫
            player_expl_img = pg.image.load(
                os.path.join(IMG_DIR, f'player_expl{i}.png')
            ).convert()
            player_expl_img.set_colorkey(BLACK)
            self.animations['expl']['player'].append(player_expl_img)
    
    def get_image(self, name):
        """獲取圖片"""
        return self.images.get(name)
    
    def get_sound(self, name):
        """獲取音效"""
        return self.sounds.get(name)
    
    def get_animation(self, name):
        """獲取動畫"""
        return self.animations.get(name)
    
    def play_music(self, loops=-1):
        """播放背景音樂"""
        pg.mixer.music.play(loops)
    
    def stop_music(self):
        """停止背景音樂"""
        pg.mixer.music.stop()