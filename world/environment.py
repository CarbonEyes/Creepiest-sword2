import pygame
import random
from world.tree import Tree
from world.coin import Coin
from world.platform import Platform # NOVO: Importa a classe Platform
from characters.monster import Monster
from characters.dragon import Dragon 
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT # [cite: 9a]

class Environment:
    """
    Gerencia os elementos do cenário, como árvores, moedas, inimigos e plataformas.
    É responsável por gerar, atualizar e desenhar esses elementos.
    """
    def __init__(self, initial_data: dict = None) -> None:
        """
        Inicializa o ambiente, criando grupos de sprites.
        Se initial_data for fornecido, restaura o estado; caso contrário, gera elementos iniciais.
        Args:
            initial_data (dict | None): Dados para restaurar o ambiente, se existirem.
        """
        self.trees: pygame.sprite.Group = pygame.sprite.Group() 
        self.coins: pygame.sprite.Group = pygame.sprite.Group() 
        self.monsters: pygame.sprite.Group = pygame.sprite.Group() 
        self.platforms: pygame.sprite.Group = pygame.sprite.Group() # NOVO: Grupo para plataformas

        if initial_data:
            self.from_dict(initial_data)
        else:
            self._generate_initial_elements()

    def _generate_initial_elements(self) -> None:
        """
        Gera os elementos iniciais para o cenário, posicionando-os no chão ou em alturas específicas.
        """
        ground_y_top = SCREEN_HEIGHT - 50 # A linha Y onde o chão começa [cite: 9a]

        # Árvores (altura 180px)
        for _ in range(3):
            x = random.randint(100, SCREEN_WIDTH - 200)
            y = ground_y_top - 180 
            self.trees.add(Tree(x, y))

        # Monstros genéricos (altura 90px)
        for _ in range(2):
            x = random.randint(150, SCREEN_WIDTH - 150)
            y = ground_y_top - 90 
            self.monsters.add(Monster(x, y))
        
        # Dragão (altura 200px)
        dragon_x = SCREEN_WIDTH // 4 
        dragon_y = 150 
        self.monsters.add(Dragon(dragon_x, dragon_y))

        # NOVO: Geração de Plataformas
        # Plataforma 1: Mais à esquerda, baixa
        self.platforms.add(Platform(SCREEN_WIDTH // 4 - 100, ground_y_top - 150, 150, 30))
        # Plataforma 2: No centro, média altura
        self.platforms.add(Platform(SCREEN_WIDTH // 2 - 75, ground_y_top - 250, 150, 30))
        # Plataforma 3: Mais à direita, alta
        self.platforms.add(Platform(SCREEN_WIDTH * 3 // 4 - 50, ground_y_top - 350, 100, 30))


    def update(self, player_rect: pygame.Rect) -> None:
        """
        Atualiza a lógica de todos os elementos do ambiente, como movimento de monstros,
        queda de moedas e remoção de objetos derrotados/coletados.
        Args:
            player_rect (pygame.Rect): O retângulo de colisão do jogador, necessário para a IA de alguns monstros.
        """
        # Atualiza monstros individualmente
        for monster in self.monsters:
            if isinstance(monster, Dragon): 
                monster.update(player_rect)
            else: 
                monster.update()
        
        self.coins.update() # [cite: 9a]

        # Lógica de remoção e geração de moedas
        for tree in self.trees.copy(): 
            if tree.is_cut:
                for _ in range(tree.coins_on_cut):
                    coin_x = tree.rect.x + random.randint(0, tree.rect.width - 30)
                    coin_y = tree.rect.y + (tree.rect.height // 4) 
                    self.coins.add(Coin(coin_x, coin_y))
                self.trees.remove(tree) 

        for monster in self.monsters.copy():
            if not monster.is_alive:
                for _ in range(monster.coins_on_defeat):
                    coin_x = monster.rect.x + random.randint(0, monster.rect.width - 30)
                    coin_y = monster.rect.y + (monster.rect.height // 4) 
                    self.coins.add(Coin(coin_x, coin_y))
                self.monsters.remove(monster) 

    def to_dict(self) -> dict:
        """Converte o estado do ambiente e seus sprites em um dicionário para salvamento."""
        trees_data = [tree.to_dict() for tree in self.trees]
        monsters_data = [monster.to_dict() for monster in self.monsters]
        coins_data = [coin.to_dict() for coin in self.coins] 
        platforms_data = [platform.to_dict() for platform in self.platforms] # NOVO: Salva dados das plataformas

        return {
            "trees": trees_data,
            "monsters": monsters_data,
            "coins": coins_data,
            "platforms": platforms_data # NOVO: Inclui plataformas nos dados salvos
        }

    def from_dict(self, data: dict) -> None:
        """Restaura o estado do ambiente e seus sprites a partir de um dicionário."""
        self.trees.empty() 
        for tree_data in data.get("trees", []):
            self.trees.add(Tree(0, 0, initial_data=tree_data)) 

        self.monsters.empty()
        for monster_data in data.get("monsters", []):
            monster_type = monster_data.get("type", "Monster") 
            if monster_type == "Dragon": 
                self.monsters.add(Dragon(0, 0, initial_data=monster_data))
            else:
                self.monsters.add(Monster(0, 0, initial_data=monster_data))

        self.coins.empty()
        for coin_data in data.get("coins", []):
            self.coins.add(Coin(0, 0, initial_data=coin_data))

        self.platforms.empty() # NOVO: Limpa plataformas existentes
        for platform_data in data.get("platforms", []): # NOVO: Restaura plataformas
            self.platforms.add(Platform(0, 0, 1, 1, initial_data=platform_data)) # Largura/Altura temp, from_dict irá restaurar


    def draw(self, screen: pygame.Surface) -> None:
        """
        Desenha todos os elementos do ambiente na tela.
        Args:
            screen (pygame.Surface): A superfície da tela do Pygame.
        """
        self.trees.draw(screen)
        self.monsters.draw(screen) 
        self.coins.draw(screen)
        self.platforms.draw(screen) # NOVO: Desenha as plataformas
