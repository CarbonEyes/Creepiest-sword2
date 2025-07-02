import pygame
import sys
from abc import ABC, abstractmethod
import os 

from cena import Cena 
from cena_menu import CenaMenu
from cena_opcoes import CenaOpcoes
from cena_jogo import CenaJogo 
from save_system.save_load import SaveLoad 
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION 


class Jogo:
    """Classe principal que controla o loop do jogo e gerencia as cenas"""
    
    def __init__(self, largura: int = SCREEN_WIDTH, altura: int = SCREEN_HEIGHT, titulo: str = CAPTION):
        """
        Inicializa o jogo com configurações básicas
        """
        pygame.init()
        pygame.mixer.init() 
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption(titulo)
        self.clock = pygame.time.Clock()
        self.cena_atual: Cena | None = None 
        self.largura = largura
        self.altura = altura
        self.rodando = True
        self.pausado: bool = False 

        # Atributos "reais" que serão gerenciados pelos getters/setters
        self._volume_musica: float = 0.5  # Prefixo "_" para o atributo interno
        self._volume_efeitos: float = 0.75 # Prefixo "_" para o atributo interno
        
        self.musica_fundo_menu_path = os.path.join("assets", "sounds", "orb8bt.mp3")
        self.musica_fundo_jogo_path = os.path.join("assets", "sounds", "game_music.mp3")
        
        self.musica_atual_tocando: str | None = None 

        self.save_load_system = SaveLoad() 

        self.mudar_cena(CenaMenu(self))

    @property # Getter para volume_musica
    def volume_musica(self) -> float:
        """Retorna o volume atual da música de fundo."""
        return self._volume_musica

    @volume_musica.setter # Setter para volume_musica
    def volume_musica(self, volume: float) -> None:
        """
        Define o volume da música de fundo e aplica ao mixer.
        Garate que o volume esteja entre 0.0 e 1.0.
        """
        self._volume_musica = max(0.0, min(1.0, volume)) 
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self._volume_musica)
    
    @property # Getter para volume_efeitos
    def volume_efeitos(self) -> float:
        """Retorna o volume atual dos efeitos sonoros."""
        return self._volume_efeitos

    @volume_efeitos.setter # Setter para volume_efeitos
    def volume_efeitos(self, volume: float) -> None:
        """
        Define o volume dos efeitos sonoros.
        Garate que o volume esteja entre 0.0 e 1.0.
        """
        self._volume_efeitos = max(0.0, min(1.0, volume))
        # Nota: Efeitos sonoros individuais precisariam verificar este volume antes de tocar.
        # Ex: pygame.mixer.Sound("sfx.wav").set_volume(self.volume_efeitos)
        # O SFX_VOLUME em core.settings já ajuda nisso na inicialização dos sons.

    def _mudar_musica(self, caminho_nova_musica: str) -> None: 
        """
        Carrega e toca uma nova música, ou continua a atual se for a mesma.
        """
        try:
                pygame.mixer.music.load(caminho_nova_musica)
                pygame.mixer.music.set_volume(self._volume_musica) # Usa o atributo gerenciado pela property
                pygame.mixer.music.play(-1) 
                self.musica_atual_tocando = caminho_nova_musica
                
        except pygame.error as e:
                print(f"Erro ao carregar ou tocar música {caminho_nova_musica}: {e}")
                self.musica_atual_tocando = None 

    def _parar_musica(self) -> None: 
        """
        Para a reprodução da música atual.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.musica_atual_tocando = None
            
    # Removido os métodos definir_volume_musica e definir_volume_efeitos,
    # pois agora são controlados pelas properties volume_musica e volume_efeitos.
    # Se você ainda precisar de métodos para o SLIDER no menu, eles chamarão diretamente as properties:
    # self.jogo.volume_musica = percentual 

    def alternar_pausa(self) -> None:
        """
        Alterna o estado de pausa do jogo.
        Se o jogo estiver em pausa, para a música. Se estiver despausado, retoma a música.
        """
        self.pausado = not self.pausado
        if self.pausado:
            print("Jogo Pausado. Pressione ESC para despausar ou 'S' para Salvar.")
            pygame.mixer.music.pause() 
        else:
            print("Jogo Despausado.")
            pygame.mixer.music.unpause() 

    def executar(self) -> None: 
        """
        Executa o loop principal do jogo.
        """
        while self.rodando:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.rodando = False
                
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if isinstance(self.cena_atual, CenaJogo): 
                             self.alternar_pausa()
                    if self.pausado and evento.key == pygame.K_s: 
                        if isinstance(self.cena_atual, CenaJogo):
                            print("Tentando salvar jogo...")
                            # Estes métodos get_player_data e get_environment_data
                            # precisarão ser implementados em CenaJogo para fornecer os dados.
                            player_data = self.cena_atual.get_player_data() if hasattr(self.cena_atual, 'get_player_data') else {}
                            environment_data = self.cena_atual.get_environment_data() if hasattr(self.cena_atual, 'get_environment_data') else {}
                            self.save_game_state(player_data, environment_data)
                            print("Jogo salvo!")
                        else:
                            print("Não é possível salvar fora da cena de jogo.")

            if self.cena_atual:
                if not self.pausado:
                    self.cena_atual.atualizar(eventos)
                
                self.cena_atual.desenhar(self.tela)
                
                if self.pausado:
                    font = pygame.font.Font(None, 74)
                    text_surface = font.render("PAUSADO", True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(self.largura // 2, self.altura // 2 - 50))
                    self.tela.blit(text_surface, text_rect)

                    save_text_surface = font.render("Pressione 'S' para Salvar", True, (200, 200, 200))
                    save_text_rect = save_text_surface.get_rect(center=(self.largura // 2, self.altura // 2 + 50))
                    self.tela.blit(save_text_surface, save_text_rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def mudar_cena(self, nova_cena: Cena) -> None: 
        """
        Altera a cena atual do jogo.
        """
        self.cena_atual = nova_cena
        self.pausado = False 

        if isinstance(nova_cena, CenaMenu):
            self._mudar_musica(self.musica_fundo_menu_path) 
        elif isinstance(nova_cena, CenaOpcoes): 
            self._mudar_musica(self.musica_fundo_menu_path) 
        elif isinstance(nova_cena, CenaJogo): 
            self._mudar_musica(self.musica_fundo_jogo_path) 
        else:
            self._parar_musica() 

    def save_game_state(self, player_data: dict, environment_data: dict) -> None:
        """
        Salva o estado atual do jogo.
        """
        game_state = {
            "player": player_data,
            "environment": environment_data,
            "current_scene": "CenaJogo", 
            "music_volume": self.volume_musica, # Acessa a property
            "sfx_volume": self.volume_efeitos   # Acessa a property
        }
        self.save_load_system.save_game(game_state)
        print("Estado do jogo salvo com sucesso!")

    def load_game_state(self) -> dict | None:
        """
        Carrega o estado do jogo salvo e muda para a cena de jogo com esses dados.
        """
        loaded_data = self.save_load_system.load_game()
        if loaded_data:
            print("Dados carregados com sucesso. Preparando para iniciar CenaJogo com dados...")
            self.volume_musica = loaded_data.get("music_volume", self.volume_musica) # Usa o setter da property
            self.volume_efeitos = loaded_data.get("sfx_volume", self.volume_efeitos)   # Usa o setter da property

            self.mudar_cena(CenaJogo(self, initial_game_data=loaded_data)) 
            self.pausado = False 
        return loaded_data