import pygame
from core.settings import COINS_PER_MONSTER_KILL, SCREEN_HEIGHT

class Monster(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, speed: int = 2, health: int = 20, damage: int = 5, initial_data: dict = None) -> None:
        super().__init__()
        try:
            self.image = pygame.image.load("assets/images/monster.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (90, 90))
        except pygame.error:
            print("Erro: Imagem do monstro (monster.png) não encontrada. Usando um retângulo vermelho como placeholder.")
            self.image = pygame.Surface((90, 90), pygame.SRCALPHA)
            self.image.fill((255, 0, 0)) 
        
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed: int = speed
        self._health: int = health    # Atributo interno
        self.damage: int = damage 
        self.coins_on_defeat: int = COINS_PER_MONSTER_KILL
        self._is_alive: bool = True # Atributo interno

        self.velocity_y: float = 0.0
        self.gravity: float = 0.8

        self.direction: int = 1 
        self.patrol_start_x: int = x 
        self.walk_limit_left: int = x - 100 
        self.walk_limit_right: int = x + 100 

        if initial_data: 
            self.from_dict(initial_data)

    @property # Getter para health
    def health(self) -> int:
        return self._health

    @health.setter # Setter para health
    def health(self, value: int) -> None:
        self._health = max(0, value) # Garante que a vida não seja negativa
        if self._health <= 0:
            self.is_alive = False # Se a vida chegar a zero, o monstro não está mais vivo

    @property # Getter para is_alive
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter # Setter para is_alive
    def is_alive(self, value: bool) -> None:
        if not value and self._is_alive: # Transição de vivo para morto
            print(f"{self.__class__.__name__} derrotado!")
            # TODO: Tocar som de monstro morrendo (se não for feito em Environment)
        self._is_alive = value

    def take_damage(self, damage: int) -> int:
        """
        Recebe dano. Reduz a saúde do monstro e retorna moedas se derrotado.
        """
        if not self.is_alive: # Acessa a property
            return 0

        self.health -= damage # Chama o setter de health

        if not self.is_alive: # Acessa a property
            return self.coins_on_defeat
        return 0

    def update(self) -> None: 
        if not self.is_alive: # Acessa a property
            return

        self._handle_patrol_movement() 
        self._apply_physics()          
            
    def _handle_patrol_movement(self) -> None: 
        self.rect.x += self.speed * self.direction
        
        if self.direction == 1 and self.rect.x >= self.walk_limit_right:
            self.direction = -1
        elif self.direction == -1 and self.rect.x <= self.walk_limit_left:
            self.direction = 1

    def _apply_physics(self) -> None: 
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        ground_level = SCREEN_HEIGHT - 50 
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0 
            
    def draw(self, screen: pygame.Surface) -> None:
        if self.is_alive: # Acessa a property
            if self.direction == -1:
                flipped_image = pygame.transform.flip(self.image, True, False)
                screen.blit(flipped_image, self.rect)
            else:
                screen.blit(self.image, self.rect)

    def to_dict(self) -> dict:
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "health": self.health, # Acessa a property
            "is_alive": self.is_alive, # Acessa a property
            "speed": self.speed,
            "damage": self.damage,
            "direction": self.direction,
            "patrol_start_x": self.patrol_start_x,
            "type": "Monster" 
        }

    def from_dict(self, data: dict) -> None:
        self.rect.x = data.get("x", self.rect.x)
        self.rect.y = data.get("y", self.rect.y)
        self.health = data.get("health", self.health) # Usa o setter da property
        self.is_alive = data.get("is_alive", self.is_alive) # Usa o setter da property
        self.speed = data.get("speed", self.speed) 
        self.damage = data.get("damage", self.damage)
        self.direction = data.get("direction", self.direction)
        self.patrol_start_x = data.get("patrol_start_x", self.patrol_start_x)
        self.walk_limit_left = self.patrol_start_x - 100
        self.walk_limit_right = self.patrol_start_x + 100