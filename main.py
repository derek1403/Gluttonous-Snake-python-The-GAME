"""
主程式入口
貪食蛇遊戲合集
"""
import pygame as pg
from config import *
from assets import Assets
from utils import create_screen
from selection_menu import SelectionMenu
from games import run_game_g, run_game_a, run_game_m, run_game_e


def main():
    """主程式"""
    # 初始化 pygame
    pg.init()
    pg.mixer.init()
    
    # 創建視窗
    screen = create_screen(WIDTH, HEIGHT)
    pg.display.set_caption(GAME_TITLE)
    
    # 載入資源
    assets = Assets()
    
    # 設定圖示
    pg.display.set_icon(assets.get_image('player_mini'))
    
    # 播放背景音樂
    assets.play_music(-1)
    
    # 主迴圈
    running = True
    while running:
        # 顯示選單
        menu = SelectionMenu(screen, assets)
        game_choice, settings = menu.run()
        
        # 檢查是否退出
        if game_choice is None:
            running = False
            continue
        
        # 執行對應遊戲
        if game_choice == GAME_G:
            result = run_game_g(
                screen, 
                assets, 
                settings.get('score_max', 100),
                settings.get('background', 'background')
            )
            
            # 播放死亡音效（如果失敗）
            if not result.get('win', False):
                assets.get_sound('die').play()
            
            # 重置螢幕大小
            screen = create_screen(WIDTH, HEIGHT)
        
        elif game_choice == GAME_A:
            result = run_game_a(
                screen,
                assets,
                settings.get('score_max', 100),
                settings.get('background', 'background')
            )
            
            # 播放死亡音效（如果失敗）
            if not result.get('win', False):
                assets.get_sound('die').play()
            
            # 如果是大螢幕模式，重置螢幕
            if result.get('is_big_screen', False):
                screen = create_screen(WIDTH, HEIGHT)
        
        elif game_choice == GAME_M:
            result = run_game_m(
                screen,
                assets,
                settings.get('background', 'background')
            )
            
            # 播放死亡音效（如果失敗）
            if not result.get('win', False):
                assets.get_sound('die').play()
            
            # 重置螢幕大小
            screen = create_screen(WIDTH, HEIGHT)
        
        elif game_choice == GAME_E:
            result = run_game_e(
                screen,
                assets,
                settings.get('background', 'background')
            )
            
            # 恢復背景音樂
            assets.play_music(-1)
        
        # 檢查是否退出
        if result.get('quit', False):
            running = False
    
    # 清理並退出
    pg.quit()


if __name__ == '__main__':
    main()