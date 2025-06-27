import pygame
import sys
from abc import ABC, abstractmethod
import os 

from cena import Cena 
from cena_menu import CenaMenu
from cena_opcoes import CenaOpcoes
from cena_jogo import CenaJogo 
from save_system.save_load import SaveLoad # Importa SaveLoad [cite: 9a]
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION # Importa configurações básicas [cite: 9a]


class Jogo:
    """Classe principal que controla o loop do jogo e gerencia as cenas"""
    
    def __init__(self, largura: int = SCREEN_WIDTH, altura: int = SCREEN_HEIGHT, titulo: str = CAPTION):
        """
        Inicializa o jogo com configurações básicas
        
        Args:
            largura (int): Largura da janela em pixels
            altura (int): Altura da janela em pixels
            titulo (str): Título da janela
        """
        pygame.init()
        pygame.mixer.init() # Inicializa o módulo de mixer para áudio
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption(titulo)
        self.clock = pygame.time.Clock()
        self.cena_atual: Cena | None = None # Tipagem para cena_atual
        self.largura = largura
        self.altura = altura
        self.rodando = True

        # Atributos para controle de volume
        self.volume_musica: float = 0.5  # 50% do volume [cite: 10d]
        self.volume_efeitos: float = 0.75 # 75% do volume [cite: 10d]
        
        # Caminhos dos arquivos de música
        self.musica_fundo_menu_path = os.path.join("assets", "sounds", "orb8bt.mp3") # [cite: 9a]
        self.musica_fundo_jogo_path = os.path.join("assets", "sounds", "game_music.mp3") # Exemplo: outra música para o jogo [cite: 9a]
        
        self.musica_atual_tocando: str | None = None # Atributo para guardar o caminho da música que está atualmente tocando

        self.save_load_system = SaveLoad() # Instancia o sistema de save/load [cite: 9a]

        # Começa com a cena do menu
        # NOTA: Passa 'self' (a instância do Jogo) para a CenaMenu.
        self.mudar_cena(CenaMenu(self)) 
        
    def mudar_musica(self, caminho_nova_musica: str) -> None:
        """
        Carrega e toca uma nova música, ou continua a atual se for a mesma.
        Args:
            caminho_nova_musica (str): O caminho para o arquivo de música a ser tocado.
        """
        # Se a música que queremos tocar já é a que está tocando, não faz nada
        if self.musica_atual_tocando == caminho_nova_musica and pygame.mixer.music.get_busy():
            # Apenas ajusta o volume caso tenha mudado
            pygame.mixer.music.set_volume(self.volume_musica) # [cite: 10d]
            return

        # Parar a música atual se houver
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            # print("Parando música atual.") # Debug removido

        # Carregar e tocar a nova música
        if os.path.exists(caminho_nova_musica):
            try:
                pygame.mixer.music.load(caminho_nova_musica)
                pygame.mixer.music.set_volume(self.volume_musica) # [cite: 10d]
                pygame.mixer.music.play(-1) # -1 para loop infinito
                self.musica_atual_tocando = caminho_nova_musica
                # print(f"Tocando nova música: {caminho_nova_musica} com volume: {self.volume_musica}") # Debug removido
            except pygame.error as e:
                print(f"Erro ao carregar ou tocar música {caminho_nova_musica}: {e}")
                self.musica_atual_tocando = None # Resetar se falhar
        else:
            print(f"Música não encontrada em: {caminho_nova_musica}") # [cite: 9a]
            self.musica_atual_tocando = None # Resetar se falhar

    def parar_musica(self) -> None:
        """
        Para a reprodução da música atual.
        """
        if pygame.mixer.music.get_busy(): # Só para se algo estiver tocando
            pygame.mixer.music.stop()
            self.musica_atual_tocando = None
            # print("Música parada.") # Debug removido

    def definir_volume_musica(self, volume: float) -> None: # [cite: 10d]
        """
        Define o volume da música de fundo e aplica ao mixer.
        Args:
            volume (float): Volume entre 0.0 e 1.0.
        """
        self.volume_musica = max(0.0, min(1.0, volume)) # Garante que o volume esteja entre 0 e 1
        # Aplica o volume imediatamente à música que está tocando
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.volume_musica)
        # print(f"Volume da música definido para: {self.volume_musica}") # Debug removido

    def definir_volume_efeitos(self, volume: float) -> None: # [cite: 10d]
        """
        Define o volume dos efeitos sonoros.
        Args:
            volume (float): Volume entre 0.0 e 1.0.
        """
        self.volume_efeitos = max(0.0, min(1.0, volume)) # Garante que o volume esteja entre 0 e 1
        # Este volume será aplicado a cada som de efeito ao ser carregado/tocado (não afeta mixer globalmente)
        # print(f"Volume dos efeitos definido para: {self.volume_efeitos}") # Debug removido
        
    def executar(self) -> None: 
        """
        Executa o loop principal do jogo.
        """
        while self.rodando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.rodando = False
            
            if self.cena_atual:
                self.cena_atual.atualizar(eventos)
                self.cena_atual.desenhar(self.tela)
            
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit() # Garante que o Pygame seja encerrado corretamente ao sair do loop
        sys.exit()

    def mudar_cena(self, nova_cena: Cena) -> None: # Tipagem Cena
        """
        Altera a cena atual do jogo.
        Args:
            nova_cena (Cena): A nova cena a ser exibida.
        """
        self.cena_atual = nova_cena
        
        # Controlar a música com base na cena
        if isinstance(nova_cena, CenaMenu): # [cite: 9a]
            self.mudar_musica(self.musica_fundo_menu_path) 
        elif isinstance(nova_cena, CenaOpcoes): # Se for para a cena de opções
            self.mudar_musica(self.musica_fundo_menu_path) # Mantém a música do menu na tela de opções
        elif isinstance(nova_cena, CenaJogo): # [cite: 9a]
            self.mudar_musica(self.musica_fundo_jogo_path) # Toca a música do jogo
        else:
            self.parar_musica() # Para a música para outras cenas (ex: Game Over, se não tiver música própria)

    def save_game_state(self, player_data: dict, environment_data: dict) -> None:
        """
        Salva o estado atual do jogo.
        Args:
            player_data (dict): Dados serializados do jogador.
            environment_data (dict): Dados serializados do ambiente.
        """
        game_state = {
            "player": player_data,
            "environment": environment_data,
            "current_scene": "CenaJogo", # Indica a cena para a qual o jogo deve voltar
            "music_volume": self.volume_musica,
            "sfx_volume": self.volume_efeitos
        }
        self.save_load_system.save_game(game_state)

    def load_game_state(self) -> dict | None:
        """
        Carrega o estado do jogo salvo e muda para a cena de jogo com esses dados.
        Returns:
            dict | None: Os dados do jogo carregados, ou None se falhar.
        """
        loaded_data = self.save_load_system.load_game()
        if loaded_data:
            print("Dados carregados com sucesso. Preparando para iniciar CenaJogo com dados...")
            # Aplica os volumes salvos
            self.definir_volume_musica(loaded_data.get("music_volume", self.volume_musica))
            self.definir_volume_efeitos(loaded_data.get("sfx_volume", self.volume_efeitos))

            # Mude para a cena do jogo passando os dados carregados
            self.mudar_cena(CenaJogo(self, initial_game_data=loaded_data)) # Passa os dados para a CenaJogo
        return loaded_data
