import os

class Config:
    
    #GAME ENVIRONMENT
    GAME_DIR = os.path.dirname(os.path.abspath(__file__))
    GAME_IMG_DIR = os.path.join(GAME_DIR, "img/")
    GAME_FONT_DIR = os.path.join(GAME_DIR, "font/")
    GAME_SOUND_DIR = os.path.join(GAME_DIR, "sound/")
    GAME_DATA_DIR = os.path.join(GAME_DIR, "data/")
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    FPS = 60    
    MAX_MIXER = 16
    
    #GAME CONSTRANTS
    EMPTY = ""
    MAX_LENGTH = 8  
    START_TEXT_POS = (SCREEN_WIDTH / 2, 690)
    START_POS = (SCREEN_WIDTH / 2, 746)
    FENCE_POSITION_Y = 600

    #GAME COLORS
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED   = (255, 0, 0)
    YELLOW= (255, 255, 0)
        
    #MONSTER STATUS
    DIE = 0
    WALK = 1
    ATTACK = 2
    DISAPPEAR = 3
    WAIT = 4
    
    #BARRIER
    BARRIER_COUNT = 10
    BARRIER_WIDTH = 90
    BARRIER_Y = 559
        
    #PLAYER STATUS
    IDLE = 0
    LEFT_ATTACK = 1
    RIGHT_ATTACK = 2
    DEATH = 3
    
    GAME_MENU = 0
    GAME_PLAYING = 1
    GAME_OVER = 2
    GAME_PAUSED = 3
    GAME_END = 4
    GAME_ENVIORMENT = 5

    CARTRIDGE_COLOR = (200, 150, 50)
    CARTRIDGE_RADIUS = 3
    GRAVITY = 0.3   

    #PROBABILITY = 0.00017
    PROBABILITY = 0.0017

    MENU_ITEM = [
        ("스테이지 {0}", 250),
        ("시작", 310),
        ("설정", 370),
        ("종료", 430)
    ]

    ENV_ITEM = [
        ("배경음 {0}", 250),
        ("효과음 {0}", 320),
        ("메인으로", 390)
    ]