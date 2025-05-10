from config import Config as cfg

class SAP():
    def __init__(self):
        self.sap_check_list = []
        
    def add_sprites(self, sprites):
        for sprite in sprites.sprites():
            self.sap_check_list.append(sprite)        
            
    def check_collision(self):
        self.sap_check_list.sort(key=lambda sprite: sprite.rect.y)
        for i in range(len(self.sap_check_list)):
            sprite_a = self.sap_check_list[i]
            for j in range(i + 1, len(self.sap_check_list)):
                sprite_b = self.sap_check_list[j]                
                    
                if sprite_a.collider.rect.y + sprite_a.collider.rect.height < 0 or \
                    sprite_a.collider.rect.y > cfg.SCREEN_HEIGHT:
                    break

                if sprite_a.collider.rect.y + sprite_a.collider.rect.height < sprite_b.collider.rect.y:
                    break
                
                if self.check_aabb(sprite_a.collider.rect, sprite_b.collider.rect):
                    if sprite_a.id == "monster" and sprite_b.id == "barrier":
                        if sprite_a.monster_status != cfg.ATTACK:
                            sprite_a.set_status("ATTACK")
                            sprite_a.attack_target = sprite_b                            
                    
                    if sprite_a.id == "barrier" and sprite_b.id == "monster":
                        if sprite_b.monster_status != cfg.ATTACK:
                            sprite_b.set_status("ATTACK")
                            sprite_b.attack_target = sprite_a
                        
                    if sprite_a.id == "monster" and sprite_b.id == "monster":
                        if sprite_a.monster_status not in (cfg.ATTACK, cfg.DIE, cfg.DISAPPEAR) and \
                            sprite_b.monster_status not in (cfg.ATTACK, cfg.DIE, cfg.DISAPPEAR):
                            if sprite_a.rect.y <= sprite_b.rect.y:
                                sprite_a.set_status("WAIT")
                                sprite_b.set_status("WALK")
                            # else:
                            #     sprite_a.set_status("WAIT")
                            #     sprite_b.set_status("WALK")
                else:
                    if sprite_a.id == "monster" and sprite_a.monster_status == cfg.WAIT:
                        sprite_a.set_status("WALK")
                        
                    if sprite_b.id == "monster" and sprite_b.monster_status == cfg.WAIT:
                        sprite_b.set_status("WALK")
                        
                    
        self.sap_check_list.clear()
                
    
    def check_aabb(self, rect_a, rect_b):
        return (rect_a.left < rect_b.right and
                rect_a.right > rect_b.left and
                rect_a.top < rect_b.bottom and
                rect_a.bottom > rect_b.top)