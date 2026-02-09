"""
選單系統
處理遊戲選擇、背景設定、分數設定等
"""
import pygame as pg
import random
from config import *
from utils import draw_text


class SelectionMenu:
    """選單管理器"""
    
    def __init__(self, screen, assets):
        """
        初始化選單
        
        Args:
            screen: pygame 顯示視窗
            assets: 資源管理器
        """
        self.screen = screen
        self.assets = assets
        self.clock = pg.time.Clock()
        self.background = 'background'
        
        # 動畫蛇
        self.snake_sprites = []
    
    def _create_animated_snakes(self):
        """創建動畫蛇"""
        snake_imgs = self.assets.get_image('snake_imgs')
        
        class AnimatedSnake(pg.sprite.Sprite):
            def __init__(self, img, x_speed, y_speed):
                pg.sprite.Sprite.__init__(self)
                self.image = pg.transform.scale(img, (50, 38))
                self.image.set_colorkey(WHITE)
                self.rect = self.image.get_rect()
                self.rect.x = WIDTH / 2
                self.rect.y = HEIGHT / 2
                self.x_speed = x_speed
                self.y_speed = y_speed
            
            def update(self):
                self.rect.x += self.x_speed
                if self.rect.left > WIDTH:
                    self.rect.right = 0
                self.rect.y += self.y_speed
                if self.rect.top < 0:
                    self.rect.top = HEIGHT
        
        # 創建3對蛇
        self.snake_sprites = []
        for _ in range(3):
            x_speed = random.randrange(27, 40)
            y_speed = random.randrange(-15, -3)
            
            snake0_group = pg.sprite.Group()
            snake0 = AnimatedSnake(snake_imgs[0], x_speed, y_speed)
            snake0_group.add(snake0)
            
            snake1_group = pg.sprite.Group()
            snake1 = AnimatedSnake(snake_imgs[1], x_speed, y_speed)
            snake1_group.add(snake1)
            
            self.snake_sprites.append((snake0_group, snake1_group))
    
    def show_main_menu(self):
        """
        顯示主選單
        
        Returns:
            str: 'settings' 或 'play' 或 'quit'
        """
        self._create_animated_snakes()
        
        background = self.assets.get_image(self.background)
        frame = 0
        
        while True:
            self.clock.tick(FPS)
            frame += 1
            
            # 繪製背景
            self.screen.blit(background, (0, 0))
            
            # 繪製標題
            draw_text(
                self.screen, 
                'Gluttonous snake', 
                64, 
                WIDTH / 2, 
                HEIGHT / 8
            )
            draw_text(
                self.screen, 
                'Press " P " to select the game', 
                40, 
                WIDTH / 2, 
                HEIGHT * 5 / 8
            )
            draw_text(
                self.screen, 
                'Press " S " to set the game', 
                40, 
                WIDTH / 2, 
                HEIGHT * 6 / 8
            )
            
            # 繪製動畫蛇（交替顯示兩幀）
            for snake0_group, snake1_group in self.snake_sprites:
                if frame % 2 == 0:
                    snake0_group.update()
                    snake0_group.draw(self.screen)
                else:
                    snake1_group.update()
                    snake1_group.draw(self.screen)
            
            pg.display.update()
            
            # 處理事件
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'quit'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        return 'settings'
                    if event.key == pg.K_p:
                        return 'play'
    
    def show_settings(self):
        """
        顯示設定畫面
        
        Returns:
            str: 選擇的背景名稱 或 'quit'
        """
        bg_img = self.assets.get_image('background')
        bg_new_img = self.assets.get_image('background_new')
        
        bg_small = pg.transform.scale(bg_img, (WIDTH / 2, HEIGHT * 0.8))
        bg_new_small = pg.transform.scale(bg_new_img, (WIDTH / 2, HEIGHT * 0.8))
        
        while True:
            self.clock.tick(FPS)
            
            # 繪製背景
            self.screen.fill(BLACK)
            self.screen.blit(bg_small, (0, HEIGHT * 0.1))
            self.screen.blit(bg_new_small, (WIDTH / 2, HEIGHT * 0.1))
            
            draw_text(
                self.screen, 
                'select background', 
                40, 
                WIDTH / 2, 
                HEIGHT * 0.01
            )
            draw_text(
                self.screen, 
                '← or →', 
                40, 
                WIDTH / 2, 
                HEIGHT * 0.92
            )
            
            pg.display.update()
            
            # 處理事件
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'quit'
            
            key_pressed = pg.key.get_pressed()
            if key_pressed[pg.K_RIGHT]:
                return 'background_new'
            if key_pressed[pg.K_LEFT]:
                return 'background'
    
    def show_game_selection(self):
        """
        顯示遊戲選擇畫面
        
        Returns:
            str: 遊戲代碼 ('G', 'A', 'M', 'E') 或 'back' 或 'quit'
        """
        background = self.assets.get_image(self.background)
        
        while True:
            self.clock.tick(FPS)
            
            self.screen.blit(background, (0, 0))
            
            draw_text(
                self.screen, 
                'Choose a game to play', 
                60, 
                WIDTH / 2, 
                HEIGHT * 1 / 8
            )
            draw_text(
                self.screen, 
                'Press " B " to back', 
                30, 
                WIDTH * 1.5 / 2, 
                HEIGHT * 7 / 8
            )
            draw_text(
                self.screen, 
                'Press " G " to start the game1', 
                40, 
                WIDTH / 2, 
                HEIGHT * 3 / 8
            )
            draw_text(
                self.screen, 
                'Press " A " to start the game2', 
                40, 
                WIDTH / 2, 
                HEIGHT * 4 / 8
            )
            draw_text(
                self.screen, 
                'Press " M " to start the game3', 
                40, 
                WIDTH / 2, 
                HEIGHT * 5 / 8
            )
            draw_text(
                self.screen, 
                'Press " E " to start the game4', 
                40, 
                WIDTH / 2, 
                HEIGHT * 6 / 8
            )
            
            pg.display.update()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 'quit'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_g:
                        return 'G'
                    if event.key == pg.K_a:
                        return 'A'
                    if event.key == pg.K_m:
                        return 'M'
                    if event.key == pg.K_e:
                        return 'E'
                    if event.key == pg.K_b:
                        return 'back'
    
    def show_score_setting(self):
        """
        顯示分數設定畫面（用於遊戲G和A）
        
        Returns:
            int: 目標分數 或 None（表示取消）
        """
        background = self.assets.get_image(self.background)
        score_str = ''
        
        while True:
            self.clock.tick(FPS)
            
            self.screen.blit(background, (0, 0))
            
            draw_text(
                self.screen, 
                'How to play ?', 
                40, 
                WIDTH / 2, 
                HEIGHT * 1 / 8
            )
            draw_text(
                self.screen, 
                'Set target score to play game', 
                40, 
                WIDTH / 2, 
                HEIGHT * 2 / 8
            )
            draw_text(
                self.screen, 
                f'you set score : {score_str if score_str else "0"}', 
                40, 
                WIDTH / 2, 
                HEIGHT * 3.5 / 8
            )
            draw_text(
                self.screen, 
                'Use ↑↓←→ to move', 
                40, 
                WIDTH / 2, 
                HEIGHT * 5 / 8
            )
            draw_text(
                self.screen, 
                'When you ready , Press " G " to start', 
                40, 
                WIDTH / 2, 
                HEIGHT * 6 / 8
            )
            
            pg.display.update()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                
                if event.type == pg.KEYDOWN:
                    # 數字鍵輸入
                    if event.key >= pg.K_0 and event.key <= pg.K_9:
                        score_str += chr(event.key)
                    
                    # 開始遊戲
                    if event.key == pg.K_g and score_str:
                        return int(score_str)
    
    def show_game_m_instructions(self):
        """
        顯示遊戲M的說明畫面
        
        Returns:
            bool: True 表示開始遊戲，False 表示取消
        """
        background = self.assets.get_image(self.background)
        
        while True:
            self.clock.tick(FPS)
            
            self.screen.blit(background, (0, 0))
            
            draw_text(
                self.screen, 
                'How to play ?', 
                40, 
                WIDTH / 2, 
                HEIGHT * 1 / 8
            )
            draw_text(
                self.screen, 
                'Target : 生きる', 
                40, 
                WIDTH / 2, 
                HEIGHT * 2 / 8
            )
            draw_text(
                self.screen, 
                'Use A~F ,1~9 to set plant', 
                40, 
                WIDTH / 2, 
                HEIGHT * 4 / 8
            )
            draw_text(
                self.screen, 
                'ex: enter"A2B3"', 
                40, 
                WIDTH / 2, 
                HEIGHT * 5 / 8
            )
            draw_text(
                self.screen, 
                'When you ready , Press " G " to start', 
                40, 
                WIDTH / 2, 
                HEIGHT * 6 / 8
            )
            
            pg.display.update()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_g:
                        return True
    
    def run(self):
        """
        執行選單流程
        
        Returns:
            tuple: (game_choice, settings) 或 (None, None) 表示退出
                game_choice: 'G', 'A', 'M', 'E'
                settings: dict，包含 score_max, background 等
        """
        while True:
            # 顯示主選單
            choice = self.show_main_menu()
            
            if choice == 'quit':
                return None, None
            
            elif choice == 'settings':
                # 設定背景
                bg_choice = self.show_settings()
                if bg_choice == 'quit':
                    return None, None
                self.background = bg_choice
            
            elif choice == 'play':
                # 選擇遊戲
                game_choice = self.show_game_selection()
                
                if game_choice == 'quit':
                    return None, None
                elif game_choice == 'back':
                    continue
                elif game_choice in ['G', 'A']:
                    # 需要設定分數
                    score_max = self.show_score_setting()
                    if score_max is None:
                        return None, None
                    
                    return game_choice, {
                        'score_max': score_max,
                        'background': self.background
                    }
                elif game_choice == 'M':
                    # 顯示說明
                    if self.show_game_m_instructions():
                        return game_choice, {
                            'background': self.background
                        }
                    else:
                        return None, None
                elif game_choice == 'E':
                    return game_choice, {
                        'background': self.background
                    }