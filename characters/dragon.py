# characters/dragon.py
import pygame
import math
from characters.monster import Monster # Dragão herda do Monstro 
from world.projectile import Projectile # Para as bolas de fogo 
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COINS_PER_DRAGON_KILL, SFX_VOLUME 

class Dragon(Monster):
    """
    Representa um dragão inimigo com comportamento inteligente, que voa e atira bolas de fogo.
    """
    def __init__(self, x: int, y: int, initial_data: dict = None) -> None:
        """
        Inicializa um dragão.
        Args:
            x (int): Posição inicial X.
            y (int): Posição inicial Y.
            initial_data (dict | None): Dados para restaurar o estado do dragão.
        """
        # Chama o construtor da classe base (Monster)
        # O dragão será mais forte, então ajustamos vida, velocidade e dano base.
        super().__init__(x, y, speed=3, health=100, damage=15, initial_data=initial_data) 
        
        # Sobrescreve a imagem do Monster
        try:
            self.original_image = pygame.image.load("assets/images/dragon.png").convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (250, 200)) # Tamanho do dragão 
        except pygame.error:
            print("Erro: Imagem do dragão (dragon.png) não encontrada. Usando um retângulo roxo como placeholder.")
            self.image = pygame.Surface((250, 200), pygame.SRCALPHA) # Placeholder 
            self.image.fill((128, 0, 128))

        self.rect = self.image.get_rect(topleft=(x, y)) # Garante que o rect seja com a imagem do dragão

        self.coins_on_defeat = COINS_PER_DRAGON_KILL # Dragão dá mais moedas 

        # Atributos de IA de Voo e Ataque
        self.patrol_start_x: int = x # Ponto de partida da patrulha horizontal
        self.patrol_range: int = 200 # Distância que ele patrulha para cada lado
        self.detection_range: int = 400 # Raio para detectar o jogador
        self.fireball_attack_range: int = 500 # Raio para ataque de bola de fogo

        # Cooldown de ataque (em frames)
        self.fireball_cooldown_ms: int = 1500 # Cooldown em milissegundos 
        self.last_fireball_time: int = pygame.time.get_ticks()

        # Grupo para gerenciar projéteis do dragão
        self.projectiles: pygame.sprite.Group = pygame.sprite.Group()

        # Sons do dragão
        try:
            self.fireball_sound = pygame.mixer.Sound("assets/sounds/fireball_sfx.wav")
            self.fireball_sound.set_volume(SFX_VOLUME) # Aplica o volume de efeitos
        except pygame.error:
            print("Erro: Som fireball_sfx.wav não encontrado.")
            self.fireball_sound = None

        # Dragão voa, então não tem gravidade nem velocidade vertical (para Monster base)
        self.velocity_y = 0.0 
        self.gravity = 0.0    
        
        if initial_data: # Restaura o estado do dragão se dados forem fornecidos
            self.from_dict(initial_data)

    def update(self, player_rect: pygame.Rect) -> None:
        """
        Atualiza a lógica do dragão, incluindo IA, movimento de voo e ataques.
        Args:
            player_rect (pygame.Rect): O retângulo de colisão do jogador.
        """
        if not self.is_alive:
            self.projectiles.update() # Ainda atualiza projéteis mesmo morto para eles sumirem
            return

        current_time = pygame.time.get_ticks()

        dx = player_rect.centerx - self.rect.centerx
        # dy não é mais usado para movimento vertical do dragão, apenas para virar
        distance_to_player = math.hypot(dx, player_rect.centery - self.rect.centery)

        # Lógica de virar o dragão (para onde o jogador está)
        if dx > 0: # Jogador à direita
            if self.image is not self.original_image: # Evita flip repetido
                self.image = self.original_image
        elif dx < 0: # Jogador à esquerda
            if self.image is self.original_image: # Evita flip repetido
                self.image = pygame.transform.flip(self.original_image, True, False)

        # --- Comportamento: Perseguir ou Patrulhar Horizontalmente ---
        if distance_to_player <= self.detection_range:
            # Perseguir o jogador horizontalmente
            if dx > 0:
                self.rect.x += self.speed
            elif dx < 0:
                self.rect.x -= self.speed
            
            # Lógica de Ataque de Bola de Fogo (voando)
            if distance_to_player <= self.fireball_attack_range:
                if current_time - self.last_fireball_time > self.fireball_cooldown_ms: # Usa cooldown em ms
                    self._shoot_fireball(player_rect.center)
                    self.last_fireball_time = current_time
        else:
            # Patrulhar horizontalmente
            self.rect.x += self.speed * self.direction
            if self.rect.x <= self.patrol_start_x - self.patrol_range:
                self.direction = 1
            elif self.rect.x >= self.patrol_start_x + self.patrol_range:
                self.direction = -1
        
        # Manter dragão dentro dos limites da tela (X e Y)
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        # Opcional: Limitar altura de voo (se ele pode subir/descer um pouco, mas não cair)
        # self.rect.y = max(50, min(self.rect.y, SCREEN_HEIGHT // 2)) # Exemplo: entre 50px e metade da tela

        # Atualiza os projéteis do dragão
        self.projectiles.update()

    def _shoot_fireball(self, target_pos: tuple[int, int]) -> None:
        """
        Cria e lança uma bola de fogo em direção ao alvo.
        Args:
            target_pos (tuple[int, int]): Posição (x, y) do alvo (jogador).
        """
        if self.fireball_sound:
            self.fireball_sound.play()
            
        # Ponto de origem da bola de fogo (ex: boca do dragão)
        # Ajuste este offset para a boca do seu sprite de dragão
        fire_start_x = self.rect.centerx + (self.rect.width // 3 if self.image is self.original_image else -self.rect.width // 3)
        fire_start_y = self.rect.top + (self.rect.height // 4) # Mais perto do topo para sair da boca 

        fireball = Projectile(fire_start_x, fire_start_y, target_pos, speed=7, damage=self.damage)
        self.projectiles.add(fireball)
        # print("Dragão atirou bola de fogo!") # Debug removido

    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha o dragão e seus projéteis.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        if self.is_alive:
            screen.blit(self.image, self.rect)
        self.projectiles.draw(screen) # Desenha os projéteis gerenciados pelo dragão

    def to_dict(self) -> dict:
        """Converte o estado do dragão em um dicionário para salvamento."""
        data = super().to_dict() # Pega os dados da classe base (Monster)
        data["type"] = "Dragon" # Indica o tipo para instanciar corretamente ao carregar
        # Adicione dados específicos do Dragão que precisam ser salvos aqui, se houver
        data["last_fireball_time"] = self.last_fireball_time
        # Projéteis não são salvos, eles são transitórios
        return data

    def from_dict(self, data: dict) -> None:
        """Restaura o estado do dragão a partir de um dicionário."""
        super().from_dict(data) # Restaura dados da classe base (Monster)
        self.last_fireball_time = data.get("last_fireball_time", pygame.time.get_ticks()) # Restaura o tempo do último ataque
        # Não restaura projéteis, eles devem ser recriados no jogo
