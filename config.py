"""
遊戲全域設定檔
包含所有常數、顏色定義、視窗尺寸等
"""
import os

# 顏色定義
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)

# 視窗設定
WIDTH = 700
HEIGHT = 800
FPS = 20

# 路徑設定
IMG_DIR = 'img'
SOUND_DIR = 'sound'
FONT_PATH = os.path.join('font.ttf')

# 遊戲標題
GAME_TITLE = "Gluttonous Snake"

# 遊戲類型
GAME_G = 'G'  # 接樹莓遊戲
GAME_A = 'A'  # 傳統貪食蛇
GAME_M = 'M'  # 植物大戰貪食蛇
GAME_E = 'E'  # 音樂彩蛋