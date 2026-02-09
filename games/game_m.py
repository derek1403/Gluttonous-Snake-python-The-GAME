"""
遊戲 M - 植物大戰貪食蛇
塔防類型遊戲，放置植物抵禦蛇的進攻
"""
import pygame as pg
import random
from config import *
from utils import draw_text, create_screen
from games.game_base import GameBase


# ==================== 精靈類別 ====================

class GoalLine(pg.sprite.Sprite):
    """目標線（蛇不能越過）"""
    
    def __init__(self, line_img, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(line_img, (3, height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = -width * 0.05
        self.rect.y = 0
    
    def update(self):
        pass


class Plant(pg.sprite.Sprite):
    """植物"""
    
    def __init__(self, plant_img, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(
            plant_img, (width * 1.5 / 20, height * 1 / 7)
        )
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        pass


class Bullet(pg.sprite.Sprite):
    """子彈"""
    
    def __init__(self, x, y, raspberry_imgs, width):
        pg.sprite.Sprite.__init__(self)
        self.image = random.choice(raspberry_imgs)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 10
        self.width = width
    
    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > self.width:
            self.kill()


class Car(pg.sprite.Sprite):
    """推車（清除該行的蛇）"""
    
    def __init__(self, car_img, line, y, width, height, need_go):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(
            car_img, (width * 1.5 / 20, height * 1 / 7)
        )
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.line = line
        self.rect.y = y
        self.x_speed = 50
        self.need_go = need_go
        self.width = width
        self.is_moving = need_go  # 新增：標記車是否正在移動
    
    def update(self):
        if self.need_go:
            self.rect.x += self.x_speed
            if self.rect.left > self.width:
                self.kill()


class Snake(pg.sprite.Sprite):
    """敵人蛇"""
    
    def __init__(self, snake_img, x_speed, y, health, width):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(
            snake_img, (width * 1.5 / 20, HEIGHT * 1 / 7)
        )
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.rect.y = y
        self.health = health
        self.x_speed = x_speed
        self.width = width
    
    def update(self):
        self.rect.x -= self.x_speed


# ==================== 遊戲主類 ====================

class GameM(GameBase):
    """遊戲M主類"""
    
    def __init__(self, screen, assets, background='background'):
        super().__init__(screen, assets)
        self.background_name = background
        self.width = WIDTH * 2  # 遊戲M使用雙倍寬度
        self.game_time = 0
        
        # 行座標映射
        self.line_y_map = {
            'B': HEIGHT * 0.2 + HEIGHT * 0 / 6.5,
            'C': HEIGHT * 0.2 + HEIGHT * 1 / 6.5,
            'D': HEIGHT * 0.2 + HEIGHT * 2 / 6.5,
            'E': HEIGHT * 0.2 + HEIGHT * 3 / 6.5,
            'F': HEIGHT * 0.2 + HEIGHT * 4 / 6.5
        }
        
        # 列座標映射
        self.col_x_map = {
            '1': self.width * 1 / 20 + self.width * 0 / 10,
            '2': self.width * 1 / 20 + self.width * 1 / 10,
            '3': self.width * 1 / 20 + self.width * 2 / 10,
            '4': self.width * 1 / 20 + self.width * 3 / 10,
            '5': self.width * 1 / 20 + self.width * 4 / 10,
            '6': self.width * 1 / 20 + self.width * 5 / 10,
            '7': self.width * 1 / 20 + self.width * 6 / 10,
            '8': self.width * 1 / 20 + self.width * 7 / 10,
            '9': self.width * 1 / 20 + self.width * 8 / 10
        }
    
    def setup(self):
        """初始化遊戲"""
        # 創建雙倍寬度螢幕
        self.screen = create_screen(self.width, HEIGHT)
        
        # 初始化精靈組
        self.goalline_sprites = pg.sprite.Group()
        self.plant_groups = []
        self.plant_x_coords = []
        self.plant_y_coords = []
        self.bullet_groups = []
        self.car_groups = []
        self.snake_groups = []
        self.snake_groups_under = []
        
        # 創建目標線
        line_img = self.assets.get_image('plant1')  # 使用植物圖片製作線
        line = GoalLine(line_img, self.width, HEIGHT)
        self.goalline_sprites.add(line)
        
        # 創建每行的車
        car_img = self.assets.get_image('car')
        for line_key in ['B', 'C', 'D', 'E', 'F']:
            car = Car(
                car_img, line_key, self.line_y_map[line_key],
                self.width, HEIGHT, False
            )
            car_group = pg.sprite.Group()
            car_group.add(car)
            self.car_groups.append(car_group)
        
        # 創建初始蛇
        self._spawn_snake('C', 'A', 20)
        
        # 用戶輸入緩衝
        self.user_input = ''
        
        # 關卡標記
        self.wave_50 = True
        self.wave_200 = True
        self.wave_350 = True
        self.wave_500 = True
        
        self.game_time = 0
    
    def _spawn_snake(self, line, snake_type, x_speed):
        """生成蛇"""
        badsnake_imgs = self.assets.get_image('badsnake_imgs')
        
        # 根據類型選擇圖片和屬性
        type_config = {
            'A': (badsnake_imgs[0], badsnake_imgs[1], 100, x_speed),
            'B': (badsnake_imgs[2], badsnake_imgs[3], 200, x_speed - random.randrange(2, 5)),
            'C': (badsnake_imgs[4], badsnake_imgs[5], 250, x_speed),
            'D': (badsnake_imgs[6], badsnake_imgs[7], 300, x_speed - random.randrange(5, 10))
        }
        
        img0, img1, health, speed = type_config[snake_type]
        y = self.line_y_map[line]
        
        snake0 = Snake(img0, speed, y, health, self.width)
        snake1 = Snake(img1, speed, y, health, self.width)
        
        group0 = pg.sprite.Group()
        group0.add(snake0)
        group1 = pg.sprite.Group()
        group1.add(snake1)
        
        self.snake_groups.append(group0)
        self.snake_groups_under.append(group1)
    
    def _create_plant(self, plant_type, line, col):
        """創建植物"""
        plant_imgs = [
            self.assets.get_image('plant1'),
            self.assets.get_image('plant2')
        ]
        plant_img = plant_imgs[int(plant_type) - 1]
        
        x = self.col_x_map[col]
        y = self.line_y_map[line]
        
        plant = Plant(plant_img, x, y, self.width, HEIGHT)
        plant_group = pg.sprite.Group()
        plant_group.add(plant)
        
        self.plant_groups.append(plant_group)
        self.plant_x_coords.append(col)
        self.plant_y_coords.append(line)
    
    def _create_bullet(self, line, col):
        """創建子彈"""
        x = self.col_x_map[col]
        y = self.line_y_map[line] + HEIGHT * 0.05
        
        raspberry_imgs = self.assets.get_image('raspberry_imgs')[:3]
        bullet = Bullet(x, y, raspberry_imgs, self.width)
        
        bullet_group = pg.sprite.Group()
        bullet_group.add(bullet)
        self.bullet_groups.append(bullet_group)
    
    def handle_events(self):
        """處理事件"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.result['quit'] = True
                return False
            
            if event.type == pg.KEYDOWN:
                # 處理植物放置輸入 (格式: A[1-2][B-F][1-9])
                if event.key == pg.K_a:
                    self.user_input = 'A'
                elif event.key in [pg.K_1, pg.K_2]:
                    self.user_input += chr(event.key)
                elif event.key in [pg.K_b, pg.K_c, pg.K_d, pg.K_e, pg.K_f]:
                    self.user_input += chr(event.key).upper()
                elif event.key in [pg.K_3, pg.K_4, pg.K_5, pg.K_6, 
                                   pg.K_7, pg.K_8, pg.K_9]:
                    self.user_input += chr(event.key)
        
        # 檢查是否完成輸入
        if len(self.user_input) == 4:
            if (self.user_input[0] == 'A' and 
                self.user_input[1] in ['1', '2'] and
                self.user_input[2] in ['B', 'C', 'D', 'E', 'F'] and
                self.user_input[3] in ['1', '2', '3', '4', '5', 
                                       '6', '7', '8', '9']):
                self._create_plant(
                    self.user_input[1],  # 植物類型
                    self.user_input[2],  # 行
                    self.user_input[3]   # 列
                )
            self.user_input = ''
        
        return True
    
    def update(self):
        """更新遊戲邏輯"""
        self.game_time += 1
        
        # 關卡波次
        if self.wave_50 and self.game_time > 50:
            for _ in range(2):
                line = random.choice(['B', 'C', 'D', 'E', 'F'])
                snake_type = random.choice(['A', 'B', 'C', 'D'])
                speed = random.randrange(13, 15)
                self._spawn_snake(line, snake_type, speed)
            self.wave_50 = False
        
        if self.wave_200 and self.game_time > 200:
            for _ in range(3):
                line = random.choice(['B', 'C', 'D', 'E', 'F'])
                snake_type = random.choice(['A', 'B', 'C', 'D'])
                speed = random.randrange(13, 16)
                self._spawn_snake(line, snake_type, speed)
            self.wave_200 = False
        
        if self.wave_350 and self.game_time > 350:
            for _ in range(5):
                line = random.choice(['B', 'C', 'D', 'E', 'F'])
                snake_type = random.choice(['A', 'B', 'C', 'D'])
                speed = random.randrange(14, 18)
                self._spawn_snake(line, snake_type, speed)
            self.wave_350 = False
        
        if self.wave_500 and self.game_time > 500 and self.game_time % 24 == 0:
            for _ in range(3):
                line = random.choice(['B', 'C', 'D', 'E', 'F'])
                snake_type = random.choice(['A', 'B', 'C', 'D'])
                speed = random.randrange(17, 22)
                self._spawn_snake(line, snake_type, speed)
        
        if self.game_time > 1650:
            self.wave_500 = False
        
        # 勝利條件
        if self.game_time > 1800:
            self.result['win'] = True
            return False
        
        # 檢查蛇是否到達目標線（失敗）
        for snake_group in self.snake_groups:
            hits = pg.sprite.groupcollide(
                self.goalline_sprites, snake_group, False, False
            )
            if hits:
                self.result['win'] = False
                return False
        
        # 更新所有精靈
        for plant_group in self.plant_groups:
            plant_group.update()
        
        for i, snake_group in enumerate(self.snake_groups):
            # 交替顯示蛇的兩個動畫幀
            if self.game_time % 2 == 0:
                snake_group.update()
            else:
                self.snake_groups_under[i].update()
        
        for car_group in self.car_groups:
            car_group.update()
        
        # 植物發射子彈
        if self.game_time % 10 == 0:
            for i, plant_group in enumerate(self.plant_groups):
                if plant_group.sprites():
                    self._create_bullet(
                        self.plant_y_coords[i],
                        self.plant_x_coords[i]
                    )
        
        for bullet_group in self.bullet_groups:
            bullet_group.update()
        
        # 碰撞檢測：車與蛇
        for car_idx, car_group in enumerate(self.car_groups):
            for snake_idx, snake_group in enumerate(self.snake_groups):
                hits = pg.sprite.groupcollide(car_group, snake_group, False, True)
                
                if hits:
                    for hit_car in hits.keys():
                        # 如果車是靜止的，啟動它
                        if not hit_car.is_moving:
                            hit_car.need_go = True
                            hit_car.is_moving = True
                        # 如果車已經在移動，什麼都不做（繼續前進）
                    
                    # 清除被撞到的蛇
                    snake_group.empty()
                    if snake_idx < len(self.snake_groups_under):
                        self.snake_groups_under[snake_idx].empty()
        
        # 碰撞檢測：子彈與蛇
        for snake_idx, snake_group in enumerate(self.snake_groups):
            for bullet_group in self.bullet_groups:
                hits = pg.sprite.groupcollide(snake_group, bullet_group, False, True)
                for hit_snake in hits:
                    hit_snake.health -= 48
                    if hit_snake.health < 0:
                        snake_group.empty()
                        self.snake_groups_under[snake_idx].empty()
        
        # 碰撞檢測：蛇與植物
        for snake_idx, snake_group in enumerate(self.snake_groups):
            for plant_group in self.plant_groups:
                hits = pg.sprite.groupcollide(snake_group, plant_group, False, True)
                for hit_snake in hits:
                    hit_snake.health -= 50
                    if hit_snake.health < 0:
                        snake_group.empty()
                        self.snake_groups_under[snake_idx].empty()
        
        return True
    
    def draw(self):
        """繪製畫面"""
        # 繪製背景
        background = self.assets.get_image(self.background_name)
        background_scaled = pg.transform.scale(background, (self.width, HEIGHT))
        self.screen.blit(background_scaled, (0, 0))
        
        # 繪製遊戲背景
        pvg_bg = self.assets.get_image('pvg_bg')
        pvg_bg_scaled = pg.transform.scale(pvg_bg, (self.width, HEIGHT * 0.9))
        self.screen.blit(pvg_bg_scaled, (0, HEIGHT * 0.1))
        
        # 繪製植物面板
        plant_board = self.assets.get_image('plant_board')
        plant_board_scaled = pg.transform.scale(
            plant_board, (self.width * 2 / 10, HEIGHT * 1 / 10)
        )
        self.screen.blit(plant_board_scaled, (self.width * 1 / 20, 0))
        
        # 繪製目標線
        self.goalline_sprites.draw(self.screen)
        
        # 繪製植物
        for plant_group in self.plant_groups:
            plant_group.draw(self.screen)
        
        # 繪製蛇（交替顯示）
        for i, snake_group in enumerate(self.snake_groups):
            if self.game_time % 5 == 0:
                snake_group.draw(self.screen)
            else:
                self.snake_groups_under[i].draw(self.screen)
        
        # 繪製車
        for car_group in self.car_groups:
            car_group.draw(self.screen)
        
        # 繪製子彈
        for bullet_group in self.bullet_groups:
            bullet_group.draw(self.screen)
        
        # 繪製時間
        draw_text(self.screen, f'time = {self.game_time}', 20, 0.9 * self.width, 0)


def run_game_m(screen, assets, background='background'):
    """
    執行遊戲M
    
    Args:
        screen: pygame 顯示視窗
        assets: 資源管理器
        background: 背景圖片名稱
    
    Returns:
        dict: 遊戲結果
    """
    game = GameM(screen, assets, background)
    return game.run()