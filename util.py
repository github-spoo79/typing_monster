import pygame
import json
from config import Config as cfg

class Util:
    @staticmethod
    def render_sheet(sheet_name, width, height, count, spacing):
        sprite_sheet = pygame.image.load(cfg.GAME_IMG_DIR + sheet_name)
        frame_width = width
        frame_height = height
        frame_count = count
        frame_spacing = spacing
        images = []
        for i in range(frame_count):
            x = i * (frame_width + frame_spacing)
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), (x, 0, frame_width, frame_height))
            images.append(frame)
        return images
    
    @staticmethod
    def rotates(image, sprites, angle_inc):
        angle = 0
        for _ in range(360):
            sprites.append(pygame.transform.rotozoom(image, angle, 1))
            angle += angle_inc
            
    @staticmethod
    def transfer_color(image, color):
        new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                pixel_color = image.get_at((x, y))
                if pixel_color.a >= 200:
                    new_image.set_at((x, y), color)                    
                else:
                    new_image.set_at((x, y), (0, 0, 0, 0))                    
        return new_image
    
    @staticmethod
    def transparent_color(image, transparent):
        new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                pixel_color = image.get_at((x, y))
                pixel_color.a = transparent
                new_image.set_at((x, y), pixel_color)          
        return new_image
    
    
    @staticmethod
    def mask_text(text):
        return "?" * len(text)
        # if len(text) <= 2:
        #     return text        
        # num_mask = max(1, len(text) // 3)  # 최소 1개는 마스킹
        # start = (len(text) - num_mask) // 2
        # masked_text = text[:start] + "?" * num_mask + text[start + num_mask:]
        # return masked_text
        
    @staticmethod    
    def load_words_by_length():
        word_dict = {}
        with open(cfg.GAME_DATA_DIR + "word.dat", 'r', encoding='utf-8') as file:
            words = file.readlines()
        
        for word in words:
            word = word.strip()
            word_length = len(word)
            
            if word_length not in word_dict:
                word_dict[word_length] = []
            
            word_dict[word_length].append(word)
    
        return word_dict
    
    @staticmethod
    def load_json(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            stages = json.load(f)
        return stages
    
    @staticmethod
    def save_json(data, json_file_path):
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)