"""
遊戲 G - 接樹莓遊戲
玩家控制角色接住掉落的樹莓，避開毒樹莓
"""
import pygame as pg
import random
from config import *
from utils import draw_text, draw_health, draw_lives
from games.game_base import GameBase


class Player(pg.sprite.Sprite):
    """玩家角色"""
    
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(assets.get_image('player'), (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        
        self.rect.x = 200
        self.rect.y = 500
        
        self.health = 100
        self.lives = 2
        
        self.hidden = False
        self.hide_time = 0
    
    def update(self):
        """更新玩家狀態"""
        # 復活邏輯
        if self.hidden and pg.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.x = WIDTH / 2
            self.rect.y = 500
        
        # 鍵盤控制
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_RIGHT]:
            self.rect.x += 10
        if key_pressed[pg.K_LEFT]:
            self.rect.x -= 10
        if key_pressed[pg.K_UP]:
            self.rect.y -= 10
        if key_pressed[pg.K_DOWN]:
            self.rect.y += 10
        
        # 邊界檢查
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT and self.rect.top < HEIGHT + 500:
            self.rect.bottom = HEIGHT
    
    def hide(self):
        """隱藏玩家（死亡時）"""
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 1000)


class Raspberry(pg.sprite.Sprite):
    """掉落的樹莓"""
    
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)
        raspberry_imgs = assets.get_image('raspberry_imgs')
        self.image_ori = random.choice(raspberry_imgs)
        self.image_ori.set_colorkey(WHITE)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        
        self.radius = int(self.rect.width * 0.8 / 2)
        
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
    
    def rotate(self):
        """旋轉動畫"""
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pg.transform.rotate(self.image_ori, self.total_degree)
        
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def update(self):
        """更新位置"""
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx


class Explosion(pg.sprite.Sprite):
    """爆炸動畫"""
    
    def __init__(self, center, size, assets):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        expl_anim = assets.get_animation('expl')
        self.frames = expl_anim[self.size]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50
    
    def update(self):
        """更新動畫幀"""
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class GameG(GameBase):
    """遊戲G主類"""
    
    def __init__(self, screen, assets, score_max=100, background='background'):
        super().__init__(screen, assets)
        self.score_max = score_max
        self.background_name = background
        self.score = 0
    
    def setup(self):
        """初始化遊戲"""
        self.all_sprites = pg.sprite.Group()
        self.raspberries = pg.sprite.Group()
        
        self.player = Player(self.assets)
        self.all_sprites.add(self.player)
        
        # 生成初始樹莓
        for _ in range(13):
            self._new_raspberry()
        
        self.score = 0
        self.death_expl = None
    
    def _new_raspberry(self):
        """生成新樹莓"""
        raspberry = Raspberry(self.assets)
        self.all_sprites.add(raspberry)
        self.raspberries.add(raspberry)
    
    def handle_events(self):
        """處理事件"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.result['quit'] = True
                return False
        return True
    
    def update(self):
        """更新遊戲邏輯"""
        self.all_sprites.update()
        
        # 檢測碰撞
        raspberry_imgs = self.assets.get_image('raspberry_imgs')
        hit_player = pg.sprite.spritecollide(
            self.player, self.raspberries, True, pg.sprite.collide_circle
        )
        
        for hit in hit_player:
            # 檢查是否為毒樹莓（第4個圖片）
            if hit.image_ori == raspberry_imgs[3]:
                self.death_expl = Explosion(
                    self.player.rect.center, 'player', self.assets
                )
                self.all_sprites.add(self.death_expl)
                self.assets.get_sound('die').play()
                self.player.health -= hit.radius
            else:
                self.score += hit.radius
                eat_sound = random.choice(self.assets.get_sound('eat_raspberry'))
                eat_sound.play()
            
            self._new_raspberry()
        
        # 檢查玩家生命
        if self.player.health <= 0:
            self.player.lives -= 1
            self.player.health = 100
            self.player.hide()
        
        # 檢查遊戲結束條件
        if self.player.lives == 0 and (
            self.death_expl is None or not self.death_expl.alive()
        ):
            self.result['score'] = 0
            return False
        
        # 檢查勝利條件
        if self.score > self.score_max:
            self.result['win'] = True
            self.result['score'] = self.score
            return False
        
        # 移除超出螢幕的樹莓
        for raspberry in self.raspberries:
            if (raspberry.rect.top > HEIGHT or 
                raspberry.rect.left > WIDTH or 
                raspberry.rect.right < 0):
                raspberry.kill()
                self._new_raspberry()
        
        return True
    
    def draw(self):
        """繪製畫面"""
        background = self.assets.get_image(self.background_name)
        self.screen.blit(background, (0, 0))
        self.all_sprites.draw(self.screen)
        
        draw_text(self.screen, str(self.score), 18, WIDTH / 2, 10)
        draw_health(self.screen, self.player.health, 5, 10)
        draw_lives(
            self.screen, 
            self.player.lives, 
            self.assets.get_image('player_mini'), 
            WIDTH - 100, 
            15
        )


def run_game_g(screen, assets, score_max=100, background='background'):
    """
    執行遊戲G
    
    Args:
        screen: pygame 顯示視窗
        assets: 資源管理器
        score_max: 目標分數
        background: 背景圖片名稱
    
    Returns:
        dict: 遊戲結果
    """
    game = GameG(screen, assets, score_max, background)
    return game.run()