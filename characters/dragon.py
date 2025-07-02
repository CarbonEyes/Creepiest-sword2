import pygame
import math
from characters.monster import Monster 
from world.projectile import Projectile 
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COINS_PER_DRAGON_KILL, SFX_VOLUME 

class Dragon(Monster):
    def __init__(self, x: int, y: int, initial_data: dict = None) -> None:
        super().__init__(x, y, speed=3, health=100, damage=15, initial_data=initial_data) 
        
        try:
            self.original_image = pygame.image.load("assets/images/dragon.png").convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (250, 200)) 
        except pygame.error:
            print("Erro: Imagem do dragão (dragon.png) não encontrada. Usando um retângulo roxo como placeholder.")
            self.image = pygame.Surface((250, 200), pygame.SRCALPHA) 
            self.image.fill((128, 0, 128))

        self.rect = self.image.get_rect(topleft=(x, y)) 

        self.coins_on_defeat = COINS_PER_DRAGON_KILL 

        self.patrol_start_x: int = x 
        self.patrol_range: int = 200 
        self.detection_range: int = 400 
        self.fireball_attack_range: int = 500 

        self._fireball_cooldown_ms: int = 1500 # Atributo interno para property
        self.last_fireball_time: int = pygame.time.get_ticks()

        self.projectiles: pygame.sprite.Group = pygame.sprite.Group()

        try:
            self.fireball_sound = pygame.mixer.Sound("assets/sounds/fireball_sfx.wav")
            self.fireball_sound.set_volume(SFX_VOLUME) 
        except pygame.error:
            print("Erro: Som fireball_sfx.wav não encontrado.")
            self.fireball_sound = None

        self.velocity_y = 0.0 
        self.gravity = 0.0    
        
        if initial_data: 
            self.from_dict(initial_data)

    @property
    def fireball_cooldown_ms(self) -> int:
        return self._fireball_cooldown_ms

    @fireball_cooldown_ms.setter
    def fireball_cooldown_ms(self, value: int) -> None:
        self._fireball_cooldown_ms = max(0, value) # Garante que o cooldown não seja negativo

    def update(self, player_rect: pygame.Rect) -> None:
        if not self.is_alive: 
            self.projectiles.update() 
            return

        current_time = pygame.time.get_ticks()

        dx = player_rect.centerx - self.rect.centerx
        distance_to_player = math.hypot(dx, player_rect.centery - self.rect.centery)

        if dx > 0: 
            if self.image is not self.original_image: 
                self.image = self.original_image
        elif dx < 0: 
            if self.image is self.original_image: 
                self.image = pygame.transform.flip(self.original_image, True, False)

        if distance_to_player <= self.detection_range:
            if dx > 0:
                self.rect.x += self.speed
            elif dx < 0:
                self.rect.x -= self.speed
            
            if distance_to_player <= self.fireball_attack_range:
                if current_time - self.last_fireball_time > self.fireball_cooldown_ms: # Acessa a property
                    self._shoot_fireball(player_rect.center) 
                    self.last_fireball_time = current_time
        else:
            self.rect.x += self.speed * self.direction
            if self.rect.x <= self.patrol_start_x - self.patrol_range:
                self.direction = 1
            elif self.rect.x >= self.patrol_start_x + self.patrol_range:
                self.direction = -1
        
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

        self.projectiles.update()

    def _shoot_fireball(self, target_pos: tuple[int, int]) -> None: 
        if self.fireball_sound:
            self.fireball_sound.play()
            
        fire_start_x = self.rect.centerx + (self.rect.width // 3 if self.image is self.original_image else -self.rect.width // 3)
        fire_start_y = self.rect.top + (self.rect.height // 4) 

        fireball = Projectile(fire_start_x, fire_start_y, target_pos, speed=7, damage=self.damage)
        self.projectiles.add(fireball)

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_alive: 
            screen.blit(self.image, self.rect)
        self.projectiles.draw(screen) 

    def to_dict(self) -> dict:
        data = super().to_dict() 
        data["type"] = "Dragon" 
        data["last_fireball_time"] = self.last_fireball_time
        data["fireball_cooldown_ms"] = self.fireball_cooldown_ms # Acessa a property
        return data

    def from_dict(self, data: dict) -> None:
        super().from_dict(data) 
        self.last_fireball_time = data.get("last_fireball_time", pygame.time.get_ticks()) 
        self.fireball_cooldown_ms = data.get("fireball_cooldown_ms", self.fireball_cooldown_ms) # Usa o setter da property