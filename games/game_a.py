"""
遊戲 A - 傳統貪食蛇
經典的貪食蛇遊戲，吃樹莓增長身體
"""
import pygame as pg
import random
from config import *
from utils import draw_text, create_screen
from games.game_base import GameBase


class SnakePlayer(pg.sprite.Sprite):
    """貪食蛇玩家"""
    
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)
        self.assets = assets
        player_img = assets.get_image('player')
        self.image_ori = pg.transform.scale(player_img, (20, 20))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        
        self.rect.x = 100
        self.rect.y = 100
        self.direction = 'right'
        self.snake_position = [100, 100]
        self.snake_segments = [[100, 100], [80, 100], [60, 100]]
        
        self.degree = 270  # 初始朝右
    
    def rotate(self):
        """旋轉蛇頭圖片"""
        self.image = pg.transform.rotate(self.image_ori, self.degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def update(self, change_direction):
        """更新蛇的狀態"""
        # 更新方向
        self.direction = change_direction
        
        # 根據方向移動蛇頭
        if self.direction == 'right':
            self.snake_position[0] += 20
            self.degree = 270
            self.rotate()
            self.rect.x += 20
        elif self.direction == 'left':
            self.snake_position[0] -= 20
            self.degree = 90
            self.rotate()
            self.rect.x -= 20
        elif self.direction == 'up':
            self.snake_position[1] -= 20
            self.degree = 0
            self.rotate()
            self.rect.y -= 20
        elif self.direction == 'down':
            self.snake_position[1] += 20
            self.degree = 180
            self.rotate()
            self.rect.y += 20
        
        # 增加蛇的長度
        self.snake_segments.insert(0, list(self.snake_position))


class SnakeRaspberry(pg.sprite.Sprite):
    """貪食蛇的食物（樹莓）"""
    
    def __init__(self, assets, max_width=WIDTH):
        pg.sprite.Sprite.__init__(self)
        raspberry_imgs = assets.get_image('raspberry_imgs')
        self.image = pg.transform.scale(random.choice(raspberry_imgs[:3]), (20, 20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
        self.radius = int(self.rect.width * 0.8 / 2)
        self.position = [300, 300]
        self.spawned = 1
        self.max_width = max_width
        self.assets = assets
    
    def respawn(self):
        """重新生成樹莓位置"""
        raspberry_imgs = self.assets.get_image('raspberry_imgs')
        self.image = pg.transform.scale(random.choice(raspberry_imgs[:3]), (20, 20))
        self.image.set_colorkey(WHITE)
        
        x = random.randrange(1, int(self.max_width / 20) - 1)
        y = random.randrange(2, int(HEIGHT / 20) - 1)
        self.position = [int(x * 20), int(y * 20)]
        self.spawned = 1


class GameA(GameBase):
    """遊戲A主類"""
    
    def __init__(self, screen, assets, score_max=100, background='background'):
        super().__init__(screen, assets)
        self.score_max = score_max
        self.background_name = background
        self.score = 0
        self.change_direction = 'right'
        self.is_big_screen = False
        self.original_screen = screen
    
    def setup(self):
        """初始化遊戲"""
        self.all_sprites = pg.sprite.Group()
        
        self.player = SnakePlayer(self.assets)
        self.all_sprites.add(self.player)
        
        self.raspberry = SnakeRaspberry(self.assets)
        self.all_sprites.add(self.raspberry)
        
        self.score = 0
        self.change_direction = 'right'
        self.fps_clock = pg.time.Clock()
        self.is_big_screen = False
    
    def handle_events(self):
        """處理事件"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.result['quit'] = True
                return False
            elif event.type == pg.KEYDOWN:
                # 判斷鍵盤事件（不能往反方向）
                if (event.key == pg.K_RIGHT or event.key == ord('d')) and \
                   self.player.direction != 'left':
                    self.change_direction = 'right'
                elif (event.key == pg.K_LEFT or event.key == ord('a')) and \
                     self.player.direction != 'right':
                    self.change_direction = 'left'
                elif (event.key == pg.K_UP or event.key == ord('w')) and \
                     self.player.direction != 'down':
                    self.change_direction = 'up'
                elif (event.key == pg.K_DOWN or event.key == ord('s')) and \
                     self.player.direction != 'up':
                    self.change_direction = 'down'
                elif event.key == pg.K_ESCAPE:
                    self.result['quit'] = True
                    return False
        return True
    
    def update(self):
        """更新遊戲邏輯"""
        self.player.update(self.change_direction)
        
        # 判斷是否吃到樹莓
        if (self.player.snake_position[0] == self.raspberry.position[0] and
            self.player.snake_position[1] == self.raspberry.position[1]):
            self.raspberry.spawned = 0
        else:
            self.player.snake_segments.pop()
        
        # 如果吃掉樹莓，則重新生成樹莓
        if self.raspberry.spawned == 0:
            self.score += 20
            
            # 分數過半，擴大螢幕
            if self.score >= self.score_max / 2 and not self.is_big_screen:
                self.screen = create_screen(WIDTH * 2, HEIGHT)
                self.is_big_screen = True
                self.raspberry.max_width = WIDTH * 2
            
            self.raspberry.respawn()
        
        # 判斷是否死亡（撞牆或撞自己）
        max_width = WIDTH * 2 if self.is_big_screen else WIDTH
        
        if (self.player.snake_position[0] > max_width - 10 or
            self.player.snake_position[0] < 0 or
            self.player.snake_position[1] > HEIGHT - 10 or
            self.player.snake_position[1] < 0):
            self.result['is_big_screen'] = self.is_big_screen
            return False
        
        # 檢查是否撞到自己
        for snake_body in self.player.snake_segments[1:]:
            if (self.player.snake_position[0] == snake_body[0] and
                self.player.snake_position[1] == snake_body[1]):
                self.result['is_big_screen'] = self.is_big_screen
                return False
        
        # 檢查勝利條件
        if self.score >= self.score_max:
            self.result['win'] = True
            self.result['score'] = self.score
            self.result['is_big_screen'] = self.is_big_screen
            return False
        
        return True
    
    def draw(self):
        """繪製畫面"""
        background = self.assets.get_image(self.background_name)
        
        if self.is_big_screen:
            background_big = pg.transform.scale(background, (WIDTH * 2, HEIGHT))
            self.screen.blit(background_big, (0, 0))
        else:
            self.screen.blit(background, (0, 0))
        
        # 繪製樹莓
        self.screen.blit(
            self.raspberry.image,
            pg.Rect(self.raspberry.position[0], self.raspberry.position[1], 20, 20)
        )
        
        # 繪製蛇身
        for position in self.player.snake_segments:
            self.screen.blit(
                self.player.image,
                pg.Rect(position[0], position[1], 20, 20)
            )
        
        # 繪製分數
        draw_text(self.screen, str(self.score), 18, WIDTH / 2, 10)
    
    def run(self):
        """執行遊戲主迴圈（覆寫以調整FPS）"""
        self.setup()
        self.running = True
        
        while self.running:
            # 根據分數調整FPS
            fps = 30 if self.score >= self.score_max / 2 else 7
            self.fps_clock.tick(fps)
            
            if not self.handle_events():
                self.running = False
                continue
            
            if not self.update():
                self.running = False
                continue
            
            self.draw()
            pg.display.flip()
        
        return self.result


def run_game_a(screen, assets, score_max=100, background='background'):
    """
    執行遊戲A
    
    Args:
        screen: pygame 顯示視窗
        assets: 資源管理器
        score_max: 目標分數
        background: 背景圖片名稱
    
    Returns:
        dict: 遊戲結果，包含 is_big_screen 標記
    """
    game = GameA(screen, assets, score_max, background)
    return game.run()