import uuid
import pygame
import random
from util import Util
from config import Config as cfg
from monster import Monster
from monster import MonsterText

class Spawn():
    def __init__(self, stage_idx, stage_resource):
        self.stage_idx = stage_idx
        self.stage_resource = stage_resource
        self.stage_info = stage_resource[self.stage_idx]

        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = pygame.time.get_ticks()

        self.previous_pos = 0
        self.enemy_pos = [90, 180, 270, 360, 450, 540, 630, 720]
        
        self.next_time = random.randint(self.stage_info["spawnMinTime"], self.stage_info["spawnMaxTime"])      
        self.min_len = self.stage_info["wordMinLen"]
        self.max_len = self.stage_info["wordMaxLen"]
        self.word_dict = Util.load_words_by_length()
        self.spawning_mob = True

    def init_stage(self, stage_idx):
        self.stage_idx = stage_idx
        self.stage_info = self.stage_resource[self.stage_idx]
        self.min_len = self.stage_info["wordMinLen"]
        self.max_len = self.stage_info["wordMaxLen"]
        self.next_time = random.randint(self.stage_info["spawnMinTime"], self.stage_info["spawnMaxTime"])

    def next_stage(self):
        self.stage_idx += 1
        self.stage_resource[self.stage_idx]["openYn"] = "Y"
        self.stage_info = self.stage_resource[self.stage_idx]
        self.min_len = self.stage_info["wordMinLen"]
        self.max_len = self.stage_info["wordMaxLen"]
        self.next_time = random.randint(self.stage_info["spawnMinTime"], self.stage_info["spawnMaxTime"])
        Util.save_json(self.stage_resource, cfg.GAME_DATA_DIR + "stage.dat")
        
    def spawn_mob(self, main):
        if self.spawning_mob:
            self.elapsed_time = pygame.time.get_ticks() - self.start_time            
            if self.elapsed_time >= self.next_time:
                x = self.next_monster_pos()
                random_pos = (x, 0)
                random_length = self.monster_text_length()
                random_text = random.choice(self.word_dict[random_length])
                #50퍼센트 확률로 남자좀비 또는 여자좀비
                if random.random() < 0.5:
                    walk = main.resources.zombie_walk_images
                    die = main.resources.zombie_die_images
                    attack = main.resources.zombie_attack_images
                    scream = main.resources.male_scream
                else:
                    walk = main.resources.zombie_woman_walk_images
                    die = main.resources.zombie_woman_die_images
                    attack = main.resources.zombie_woman_attack_images    
                    scream = main.resources.female_scream

                #스테이지 정보에서 몹의 최소, 최대 속도에서 random하게 추출
                speed = round(random.uniform(self.stage_info["mobMinSpeed"], self.stage_info["mobMaxSpeed"]), 1)

                monster_uuid = uuid.uuid4()
                monster = Monster(self, monster_uuid, random_pos, walk, die, attack, scream, speed)
                monster_text = MonsterText(self, monster_uuid, monster, random_text, self.stage_info["mobSkillProba"])
                monster.monster_text = monster_text
                
                main.enemy_sprites.add(monster)
                main.enemy_text_sprites.add(monster_text)

                self.start_time = pygame.time.get_ticks()
                self.next_time = random.randint(self.stage_info["spawnMinTime"], self.stage_info["spawnMaxTime"])        

    def next_monster_pos(self):
        possible_choices = [pos for pos in self.enemy_pos if pos != self.previous_pos]
        next_pos = random.choice(possible_choices)
        self.previous_pos = next_pos
        return next_pos
    
    def monster_text_length(self):
        return random.randint(self.min_len, self.max_len)
    
    def stop_spawn_mob(self):
        self.spawning_mob = False