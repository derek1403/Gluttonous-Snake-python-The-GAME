"""
共用工具函數
提供繪製文字、血條、生命等常用功能
"""
import pygame as pg
from config import *


def draw_text(surf, text, size, x, y, color=WHITE):
    """
    在指定位置繪製文字
    
    Args:
        surf: pygame surface
        text: 文字內容
        size: 字體大小
        x: x 座標（中心）
        y: y 座標（頂部）
        color: 文字顏色
    """
    font = pg.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)


def draw_health(surf, hp, x, y, bar_length=100, bar_height=10):
    """
    繪製血條
    
    Args:
        surf: pygame surface
        hp: 當前血量（0-100）
        x: x 座標
        y: y 座標
        bar_length: 血條長度
        bar_height: 血條高度
    """
    if hp < 0:
        hp = 0
    
    fill = (hp / 100) * bar_length
    
    outline_rect = pg.Rect(x, y, bar_length, bar_height)
    fill_rect = pg.Rect(x, y, fill, bar_height)
    
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, lives, img, x, y, spacing=30):
    """
    繪製生命圖示
    
    Args:
        surf: pygame surface
        lives: 生命數量
        img: 生命圖示
        x: x 座標
        y: y 座標
        spacing: 圖示間距
    """
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + spacing * i
        img_rect.y = y
        surf.blit(img, img_rect)


def create_screen(width=WIDTH, height=HEIGHT):
    """創建遊戲視窗"""
    return pg.display.set_mode((width, height))


def game_over_screen(surf, message="Game Over", font_size=72):
    """
    顯示遊戲結束畫面
    
    Args:
        surf: pygame surface
        message: 顯示訊息
        font_size: 字體大小
    """
    font = pg.font.Font(FONT_PATH, font_size)
    text_surface = font.render(message, True, GREY)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH // 2, 10)
    surf.blit(text_surface, text_rect)
    pg.display.flip()