# 貪食蛇遊戲合集

一個包含四種不同遊戲模式的 Python pygame 專案。

## 專案結構

```
project/
├── main.py                    # 主程式入口
├── config.py                  # 全域設定
├── utils.py                   # 共用工具函數
├── assets.py                  # 資源管理
├── selection_menu.py          # 選單系統
├── games/
│   ├── __init__.py
│   ├── game_base.py          # 遊戲基類
│   ├── game_g.py             # 遊戲G - 接樹莓
│   ├── game_a.py             # 遊戲A - 傳統貪食蛇
│   ├── game_m.py             # 遊戲M - 植物大戰貪食蛇
│   └── game_e.py             # 遊戲E - 音樂彩蛋
├── img/                       # 圖片資源
└── sound/                     # 音效資源
```

## 遊戲說明

### 遊戲 G - 接樹莓遊戲
- **目標**: 控制角色接住掉落的樹莓，避開炸彈
- **操作**: 方向鍵移動
- **規則**: 
  - 接到普通樹莓加分
  - 接到炸彈扣血
  - 達到目標分數即可獲勝

### 遊戲 A - 傳統貪食蛇
- **目標**: 吃樹莓增長身體，達到目標分數
- **操作**: 方向鍵↑、↓、←、→控制方向
- **規則**:
  - 吃到樹莓身體變長，分數增加
  - 撞牆或撞到自己失敗
  - 達到一半分數後螢幕會變大

### 遊戲 M - 植物大戰貪食蛇
- **目標**: 放置植物抵禦蛇的進攻，堅持到時間結束
- **操作**: 按鍵輸入 `A[1-2][B-F][1-9]` 放置植物
  - `A`: 啟動放置模式
  - `1-2`: 植物類型（1或2）
  - `B-F`: 行位置
  - `1-9`: 列位置
  - 例如: `A2B3` 表示在B行3列放置2號植物
- **規則**:
  - 植物會自動發射子彈攻擊蛇
  - 蛇到達左側邊界即失敗
  - 堅持1800回合即可獲勝

### 遊戲 E - 音樂彩蛋
- 一個有趣的彩蛋遊戲
- 欣賞音樂並嘗試退出 😉

## 安裝與執行

### 環境需求
- Python 3.7+
- pygame

### 安裝步驟

1. 安裝 pygame:
```bash
pip install pygame
```

2. 確保專案結構完整，包含 `img/` 和 `sound/` 資料夾及其內容

3. 執行遊戲:
```bash
python main.py
```

## 程式碼架構說明

### 核心模組

#### config.py
定義所有全域常數，包括:
- 顏色定義
- 視窗尺寸
- FPS
- 路徑設定

#### utils.py
提供共用工具函數:
- `draw_text()`: 繪製文字
- `draw_health()`: 繪製血條
- `draw_lives()`: 繪製生命圖示
- `create_screen()`: 創建視窗

#### assets.py
資源管理器，負責:
- 載入所有圖片資源
- 載入所有音效資源
- 管理動畫序列
- 提供統一的資源訪問接口

#### selection_menu.py
選單系統，包含:
- 主選單
- 遊戲選擇
- 背景設定
- 分數設定

### 遊戲模組 (games/)

#### game_base.py
遊戲基類，定義統一接口:
- `setup()`: 遊戲初始化
- `handle_events()`: 事件處理
- `update()`: 遊戲邏輯更新
- `draw()`: 畫面繪製
- `run()`: 遊戲主迴圈

所有遊戲都繼承自此基類，確保統一的結構。

#### 各遊戲模組
每個遊戲都實作為獨立模組，提供 `run_game_x()` 函數作為入口點。

## 開發指南

### 新增遊戲

要新增新遊戲，只需:

1. 在 `games/` 目錄下創建 `game_x.py`
2. 繼承 `GameBase` 類別
3. 實作必要方法
4. 在 `games/__init__.py` 中導入
5. 在 `main.py` 中添加調用邏輯

範例:
```python
from games.game_base import GameBase

class GameX(GameBase):
    def setup(self):
        # 初始化
        pass
    
    def handle_events(self):
        # 處理事件
        return True
    
    def update(self):
        # 更新邏輯
        return True
    
    def draw(self):
        # 繪製畫面
        pass

def run_game_x(screen, assets, **kwargs):
    game = GameX(screen, assets, **kwargs)
    return game.run()
```
### 製作成exe

```bash
pyi-makespec -F -w main.py
pyinstaller main.spec
```

### 新增資源

1. 圖片放在 `img/` 目錄
2. 音效放在 `sound/` 目錄
3. 在 `assets.py` 中添加載入邏輯
4. 使用 `assets.get_image()` 或 `assets.get_sound()` 訪問

## 注意事項

- 所有圖片應為 PNG 格式
- 音效建議使用 WAV 或 MP3 格式
- 程式碼使用 UTF-8 編碼，支援中文註解
- 遊戲 M 會自動創建雙倍寬度螢幕
- 遊戲 A 達到一半分數後會擴大螢幕

## 授權

此專案為教育用途，歡迎修改和擴展。

## 貢獻

歡迎提交問題報告和改進建議！