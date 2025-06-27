import pygame
import math
from core.settings import SWORD_GROWTH_PER_COIN, COINS_FOR_SWORD_LEVEL_UP 
from world.projectile import Projectile # <--- ADICIONE ESTA LINHA [cite: sword_180_degree_swing]

class Sword(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        try:
            self.original_image = pygame.image.load("assets/images/sword.png").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (45, 150)) # Tamanho base da espada
        except pygame.error:
            print("Erro: Imagem da espada (sword.png) não encontrada. Usando um retângulo como placeholder.")
            self.original_image = pygame.Surface((45, 150), pygame.SRCALPHA) # Placeholder
            self.original_image.fill((150, 150, 150)) 
            pygame.draw.rect(self.original_image, (100, 50, 0), (15, 120, 15, 30)) # Cabo do placeholder

        self.scaled_current_image = self.original_image.copy() 
        self.image = self.scaled_current_image 
        self.rect = self.image.get_rect() 

        self.base_width: int = self.original_image.get_width()
        self.base_height: int = self.original_image.get_height()
        self.current_growth_level: int = 0
        self.current_damage: int = 5 

        self.swing_active: bool = False 
        self.swing_direction: int = 0 
        self.swing_angle: float = 0 
        
        self.swing_duration_frames: int = 20 
        self.current_swing_frame: int = 0 

        self.swing_back_speed: float = 7 

        self.SWING_OVERHEAD_RIGHT_START_ANGLE = 225 
        self.SWING_OVERHEAD_RIGHT_END_ANGLE = 45   
        self.SWING_OVERHEAD_LEFT_START_ANGLE = 315 
        self.SWING_OVERHEAD_LEFT_END_ANGLE = 135   

        self.sword_pivot_offset_local = pygame.math.Vector2(self.base_width / 2, self.base_height * 0.9)


    def try_grow_by_coins(self, total_coins: int) -> None:
        new_growth_level = total_coins // COINS_FOR_SWORD_LEVEL_UP
        
        if new_growth_level > self.current_growth_level:
            self.current_growth_level = new_growth_level
            new_height = self.base_height + (self.current_growth_level * SWORD_GROWTH_PER_COIN * 10)
            
            self.scaled_current_image = pygame.transform.scale(self.original_image, (self.base_width, int(new_height)))
            self.sword_pivot_offset_local = pygame.math.Vector2(self.base_width / 2, self.scaled_current_image.get_height() * 0.9)

            print(f"Espada cresceu! Nível: {self.current_growth_level}, Altura: {new_height:.2f}px")
            self.current_damage = 5 + (self.current_growth_level * 2) 

    def start_swing(self, direction: int) -> None:
        if not self.swing_active: 
            self.swing_active = True
            self.is_attacking = True 
            self.swing_direction = direction
            self.current_swing_frame = 0 

            if self.swing_direction == 1: 
                self.swing_start_angle = self.SWING_OVERHEAD_RIGHT_START_ANGLE
                self.swing_end_angle = self.SWING_OVERHEAD_RIGHT_END_ANGLE
            else: 
                self.swing_start_angle = self.SWING_OVERHEAD_LEFT_START_ANGLE
                self.swing_end_angle = self.SWING_OVERHEAD_LEFT_END_ANGLE
            
            self.swing_angle = self.swing_start_angle 
            # print(f"Swing START: Active={self.swing_active}, Dir={self.swing_direction}, Angle={self.swing_angle:.2f}") # Debug removido
            # TODO: Tocar som de balanço da espada aqui

    def update(self, player_center: tuple[int, int], player_facing_right: bool) -> None:
        if self.swing_active:
            self.current_swing_frame += 1 
            
            progress = min(1.0, self.current_swing_frame / self.swing_duration_frames)
            self.swing_angle = self.swing_start_angle + (self.swing_end_angle - self.swing_start_angle) * progress
            
            if progress >= 1.0:
                self.swing_active = False
                self.is_attacking = False 
                self.swing_angle = self.swing_end_angle 

        else: 
            target_angle = 0 if player_facing_right else 180 
            self.swing_angle = self.swing_angle % 360
            target_angle = target_angle % 360

            angle_diff = target_angle - self.swing_angle
            if angle_diff > 180:
                angle_diff -= 360
            elif angle_diff < -180:
                angle_diff += 360

            if abs(angle_diff) > self.swing_back_speed:
                if angle_diff > 0:
                    self.swing_angle += self.swing_back_speed
                else:
                    self.swing_angle -= self.swing_back_speed
            else:
                self.swing_angle = target_angle
            
            self.is_attacking = False


        rotated_image = pygame.transform.rotate(self.scaled_current_image, self.swing_angle)
        
        player_anchor_offset_x = 0 
        player_anchor_offset_y = -40 

        player_anchor_world_x = player_center[0] + (player_anchor_offset_x if player_facing_right else -player_anchor_offset_x)
        player_anchor_world_y = player_center[1] + player_anchor_offset_y

        rotated_pivot_offset = self.sword_pivot_offset_local.rotate(-self.swing_angle) 

        new_topleft_x = player_anchor_world_x - rotated_pivot_offset.x
        new_topleft_y = player_anchor_world_y - rotated_pivot_offset.y

        self.rect = rotated_image.get_rect(topleft=(new_topleft_x, new_topleft_y))

        self.image = rotated_image

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def get_damage(self) -> int:
        return self.current_damage

    def repel_projectile(self, projectile: Projectile, player_facing_right: bool) -> None:
        """
        Repela um projétil, invertendo sua direção e talvez aumentando sua velocidade.
        Args:
            projectile (Projectile): O projétil a ser repelido.
            player_facing_right (bool): Direção para onde o jogador está virado (para repelir na direção certa).
        """
        # Inverte a direção do projétil
        projectile.direction_x *= -1 
        projectile.direction_y *= -1 
        
        projectile.speed *= 1.5 
        
        projectile.repelled = True 
        projectile.repeller_damage = self.get_damage() 


