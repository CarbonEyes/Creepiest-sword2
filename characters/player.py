import pygame
from characters.sword import Sword 
from core.settings import PLAYER_SPEED, PLAYER_HEALTH, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, initial_data: dict = None) -> None:
        super().__init__() 

        try:
            self.image = pygame.image.load("assets/images/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 110)) 
        except pygame.error:
            print("Erro: Imagem do jogador (player.png) não encontrada. Usando um retângulo como placeholder.")
            self.image = pygame.Surface((80, 110), pygame.SRCALPHA) 
            self.image.fill((0, 150, 255)) 
        
        self.rect = self.image.get_rect(topleft=(x, y)) 

        self.speed: int = PLAYER_SPEED 
        self._health: int = PLAYER_HEALTH # Atributo interno para a property
        self._coins: int = 0             # Atributo interno para a property
        self.sword: Sword = Sword() 
        
        self.velocity_y: float = 0.0
        self.is_jumping: bool = False
        self.gravity: float = 0.8 
        self.jump_power: float = -15.0 

        self.moving_left: bool = False
        self.moving_right: bool = False
        self.facing_right: bool = True 

        self.swing_initiated_by_movement: bool = False

        if initial_data: 
            self.from_dict(initial_data)
    
    @property # Getter para health
    def health(self) -> int:
        return self._health

    @health.setter # Setter para health
    def health(self, amount: int) -> None:
        self._health = max(0, amount) # Garante que a vida não seja negativa
        print(f"Jogador: Vida restante: {self._health}")
        if self._health <= 0:
            print("Jogador foi derrotado! (Lógica de Game Over deve ser acionada externamente)")
            # Nota: O controle de Game Over está na CenaJogo, que verificará esta property.

    @property # Getter para coins
    def coins(self) -> int:
        return self._coins

    @coins.setter # Setter para coins
    def coins(self, amount: int) -> None:
        self._coins = max(0, amount) # Moedas não devem ser negativas
        print(f"Moedas: {self._coins}")
        self.sword._try_grow_by_coins(self._coins) # Dispara a lógica da espada automaticamente

    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
                self.facing_right = False
                if not self.sword.swing_active and not self.swing_initiated_by_movement:
                    self.sword.start_swing(-1) 
                    self.swing_initiated_by_movement = True
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
                self.facing_right = True
                if not self.sword.swing_active and not self.swing_initiated_by_movement:
                    self.sword.start_swing(1) 
                    self.swing_initiated_by_movement = True
            elif event.key == pygame.K_SPACE: 
                if not self.is_jumping and self.velocity_y == 0: 
                    self.velocity_y = self.jump_power
                    self.is_jumping = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
                self.swing_initiated_by_movement = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False
                self.swing_initiated_by_movement = False
        
    def update(self, platforms: pygame.sprite.Group) -> None: 
        self._handle_horizontal_movement()      
        self._apply_gravity_and_collisions(platforms) 
        self.sword.update(self.rect.center, self.facing_right)

    def _handle_horizontal_movement(self) -> None: 
        if self.moving_left and not self.moving_right:
            self.rect.x -= self.speed
        elif self.moving_right and not self.moving_left:
            self.rect.x += self.speed
        
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

    def _apply_gravity_and_collisions(self, platforms: pygame.sprite.Group) -> None: 
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        ground_level = SCREEN_HEIGHT - 50 
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0
            self.is_jumping = False 

        collided_platforms = pygame.sprite.spritecollide(self, platforms, False) 
        
        if self.velocity_y > 0: 
            for platform in collided_platforms:
                if self.rect.bottom - self.velocity_y <= platform.rect.top and \
                   self.rect.bottom >= platform.rect.top:
                    self.rect.bottom = platform.rect.top 
                    self.velocity_y = 0 
                    self.is_jumping = False 
                    break 

        elif self.velocity_y < 0: 
            for platform in collided_platforms:
                if self.rect.top >= platform.rect.bottom - abs(self.velocity_y) and \
                   self.rect.top <= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom 
                    self.velocity_y = 0 
                    break 

    def draw(self, screen: pygame.Surface) -> None:
        if not self.facing_right:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        
        self.sword.draw(screen)

    def collect_coin(self, amount: int = 1) -> None:
        """
        Aumenta o número de moedas do jogador.
        O crescimento da espada é acionado pelo setter de `coins`.
        """
        self.coins += amount # Isso chamará o setter de coins

    def take_damage(self, amount: int) -> None:
        """
        Reduz a saúde do jogador.
        """
        self.health -= amount # Isso chamará o setter de health

    def to_dict(self) -> dict:
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "health": self.health, # Acessa a property
            "coins": self.coins,   # Acessa a property
            "facing_right": self.facing_right,
            "sword_growth_level": self.sword.current_growth_level,
            "sword_current_damage": self.sword.current_damage 
        }

    def from_dict(self, data: dict) -> None:
        self.rect.x = data.get("x", self.rect.x)
        self.rect.y = data.get("y", self.rect.y)
        self.health = data.get("health", self.health) # Usa o setter, que fará a validação
        self.coins = data.get("coins", self.coins)   # Usa o setter, que acionará o crescimento da espada
        self.facing_right = data.get("facing_right", self.facing_right)
        
        self.sword.current_growth_level = data.get("sword_growth_level", 0)
        self.sword.current_damage = data.get("sword_current_damage", 5) 
        # A chamada a _try_grow_by_coins aqui pode ser removida
        # porque o setter de 'coins' já fará isso.
        # No entanto, se o from_dict for chamado com coins=0 mas sword_growth_level > 0,
        # pode ser útil re-chamar para garantir que a espada seja do tamanho correto.
        # Deixarei a chamada para robustez no carregamento.
        self.sword._try_grow_by_coins(self.coins)