import pygame
from characters.sword import Sword 
from core.settings import PLAYER_SPEED, PLAYER_HEALTH, SCREEN_WIDTH, SCREEN_HEIGHT
class Player(pygame.sprite.Sprite):
    """
    Representa o personagem jogável, gerenciando seu movimento, física, vida,
    interação com a espada e coleta de moedas.
    """
    def __init__(self, x: int, y: int, initial_data: dict = None) -> None:
        """
        Inicializa o jogador.
        Args:
            x (int): Posição inicial X do jogador.
            y (int): Posição inicial Y do jogador.
        """
        super().__init__() 

        try:
            self.image = pygame.image.load("assets/images/player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (80, 110)) 
        except pygame.error:
            print("Erro: Imagem do jogador (player.png) não encontrada. Usando um retângulo como placeholder.")
            self.image = pygame.Surface((80, 110), pygame.SRCALPHA) # Placeholder
            self.image.fill((0, 150, 255)) 
        
        self.rect = self.image.get_rect(topleft=(x, y)) 

        self.speed: int = PLAYER_SPEED # Velocidade de movimento horizontal 
        self.health: int = PLAYER_HEALTH
        self.coins: int = 0
        self.sword: Sword = Sword() # A espada é instanciada sem posições iniciais 
        
        # Atributos de Física (Pulo/Gravidade)
        self.velocity_y: float = 0.0
        self.is_jumping: bool = False
        self.gravity: float = 0.8 
        self.jump_power: float = -15.0 

        # Estado de movimento e direção
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.facing_right: bool = True 

        # Flag para controlar se um swing já foi iniciado por um movimento (evita spam)
        self.swing_initiated_by_movement: bool = False

        if initial_data: # Restaura o estado do jogador se dados forem fornecidos
            self.from_dict(initial_data)

    def handle_input(self, event: pygame.event.Event) -> None:
        """
        Processa eventos de teclado para movimento do jogador e aciona o balanço da espada.
        Args:
            event (pygame.event.Event): O evento do Pygame.
        """
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
            elif event.key == pygame.K_SPACE: # Pulo
                # Só permite pular se não estiver pulando e estiver no chão (ou plataforma)
                # Verifica se está no chão ou em plataforma (velocity_y == 0)
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
        

    def update(self, platforms: pygame.sprite.Group) -> None: # Recebe o grupo de plataformas
        """
        Atualiza a lógica do jogador (movimento, física, e a espada), e verifica colisões com plataformas.
        Args:
            platforms (pygame.sprite.Group): O grupo de sprites das plataformas para verificação de colisão.
        """
        # Movimento Horizontal
        # Atualiza a posição X baseada nas flags de movimento
        if self.moving_left and not self.moving_right:
            self.rect.x -= self.speed
        elif self.moving_right and not self.moving_left:
            self.rect.x += self.speed
        
        # Manter jogador dentro da tela
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

        # Aplicar Gravidade
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Colisão com o CHÃO VERDE (definido em cena_jogo.py como SCREEN_HEIGHT - 50)
        ground_level = SCREEN_HEIGHT - 50 
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0
            self.is_jumping = False # Não está pulando se está no chão

        # Colisão com Plataformas
        # Cria um retângulo de teste para prever a próxima posição Y (apenas para colisão vertical)
        # É importante mover o jogador para a próxima posição ANTES de verificar a colisão
        # para que o colisor do Pygame funcione corretamente para "pousar"
        
        # Move o rect Y primeiro, então verifica colisão
        collided_platforms = pygame.sprite.spritecollide(self, platforms, False) 
        
        # Lógica de pouso em plataforma (quando o jogador está caindo)
        if self.velocity_y > 0: # Se o jogador está caindo
            for platform in collided_platforms:
                # Verifica se o jogador está caindo sobre a plataforma (topo do rect do jogador está ACIMA do topo da plataforma)
                # Adicionamos uma pequena tolerância (self.gravity * 2 ou similar) para garantir que ele não "atravesse" a plataforma
                # se estiver se movendo muito rápido.
                if self.rect.bottom - self.velocity_y <= platform.rect.top and \
                   self.rect.bottom >= platform.rect.top:
                    self.rect.bottom = platform.rect.top # Aterriza no topo da plataforma
                    self.velocity_y = 0 # Para a queda
                    self.is_jumping = False # Não está pulando
                    break # Aterriza em uma plataforma, não precisa verificar mais

        # Lógica de bater a cabeça em plataforma (quando o jogador está subindo)
        elif self.velocity_y < 0: # Se o jogador está subindo
            for platform in collided_platforms:
                # Verifica se o jogador está subindo e colide com a parte de baixo da plataforma
                if self.rect.top >= platform.rect.bottom - abs(self.velocity_y) and \
                   self.rect.top <= platform.rect.bottom:
                    self.rect.top = platform.rect.bottom # Colide com a parte de baixo da plataforma
                    self.velocity_y = 0 # Para a subida (cairá depois se não houver mais plataforma abaixo)
                    break # Bateu, não precisa verificar mais

        # Atualiza a espada, passando o centro do jogador e a direção para onde ele está virado
        self.sword.update(self.rect.center, self.facing_right)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o jogador e sua espada na tela.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        # Desenha o jogador, espelhando a imagem se ele estiver virado para a esquerda
        if not self.facing_right:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        
        self.sword.draw(screen)

    def collect_coin(self, amount: int = 1) -> None:
        """
        Aumenta o número de moedas do jogador e tenta aumentar o tamanho da espada.
        Args:
            amount (int): A quantidade de moedas coletadas.
        """
        self.coins += amount
        print(f"Moedas: {self.coins}")
        self.sword.try_grow_by_coins(self.coins)

    def take_damage(self, amount: int) -> None:
        """
        Reduz a saúde do jogador.
        Args:
            amount (int): Quantidade de dano a ser aplicada.
        """
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Jogador tomou {amount} de dano. Vida restante: {self.health}")

    def to_dict(self) -> dict:
        """Converte o estado do jogador em um dicionário para salvamento."""
        return {
            "x": self.rect.x,
            "y": self.rect.y,
            "health": self.health,
            "coins": self.coins,
            "facing_right": self.facing_right,
            "sword_growth_level": self.sword.current_growth_level,
            "sword_current_damage": self.sword.current_damage 
        }

    def from_dict(self, data: dict) -> None:
        """Restaura o estado do jogador a partir de um dicionário."""
        self.rect.x = data.get("x", self.rect.x)
        self.rect.y = data.get("y", self.rect.y)
        self.health = data.get("health", self.health)
        self.coins = data.get("coins", self.coins)
        self.facing_right = data.get("facing_right", self.facing_right)
        
        self.sword.current_growth_level = data.get("sword_growth_level", 0)
        self.sword.current_damage = data.get("sword_current_damage", 5) 
        self.sword.try_grow_by_coins(self.coins)
