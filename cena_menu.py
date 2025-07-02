import pygame
import sys
from botao import Botao
import pygame
from cena import Cena

class CenaMenu(Cena):
    """
    Representa a cena do menu principal do jogo.
    """
    def __init__(self, jogo):
        """
        Inicializa a CenaMenu, criando os botões e configurando o título.
        Args:
            jogo: A instância do jogo principal.
        """
        self.jogo = jogo
        self.botoes = []  

        btn_jogar = Botao(
            x=jogo.largura//2 - 100,
            y=200,
            largura=200,
            altura=50,
            texto="Novo Jogo", 
            cor_normal=(100, 255, 100),
            cor_hover=(50, 200, 50),
            acao=self._iniciar_novo_jogo # Chamando o método privado
        )

        btn_continuar = Botao(
            x=jogo.largura//2 - 100,
            y=275, 
            largura=200,
            altura=50,
            texto="Continuar",
            cor_normal=(100, 150, 255),
            cor_hover=(50, 100, 200),
            acao=self._continuar_jogo # Chamando o método privado
        )
        
        btn_opcoes = Botao(
            x=jogo.largura//2 - 100,
            y=350, 
            largura=200,
            altura=50,
            texto="Opções",
            cor_normal=(100, 100, 255),
            cor_hover=(50, 50, 200),
            acao=self._ir_para_opcoes # Chamando o método privado
        )
        
        btn_sair = Botao(
            x=jogo.largura//2 - 100,
            y=425, 
            largura=200,
            altura=50,
            texto="Sair",
            cor_normal=(255, 100, 100),
            cor_hover=(200, 50, 50),
            acao=self._sair # Chamando o método privado
        )
        
        self.botoes.extend([btn_jogar, btn_continuar, btn_opcoes, btn_sair]) 
    
    def _iniciar_novo_jogo(self) -> None: # TORNADO PRIVADO
        """
        Função chamada ao clicar no botão "Novo Jogo".
        Inicia uma nova CenaJogo.
        """
        print("Iniciando novo jogo...")
        from cena_jogo import CenaJogo 
        self.jogo.mudar_cena(CenaJogo(self.jogo)) 
    
    def _continuar_jogo(self) -> None: # TORNADO PRIVADO
        """
        Função chamada ao clicar no botão "Continuar".
        Tenta carregar um jogo salvo através do objeto Jogo.
        """
        print("Tentando carregar jogo...")
        self.jogo.load_game_state() 

    def _ir_para_opcoes(self) -> None: # TORNADO PRIVADO
        """
        Função chamada ao clicar no botão "Opções", muda para a cena de opções.
        """
        from cena_opcoes import CenaOpcoes 
        self.jogo.mudar_cena(CenaOpcoes(self.jogo))
        
    def _sair(self) -> None: # TORNADO PRIVADO
        """
        Função chamada ao clicar no botão "Sair", encerra o Pygame e o sistema.
        """
        self.jogo.rodando = False 
    
    def atualizar(self, eventos: list) -> None:
        """
        Atualiza o estado da cena do menu, processando eventos para os botões.
        Args:
            eventos (list): Lista de eventos do Pygame.
        """
        for botao in self.botoes:
            botao.atualizar(eventos)
    
    def desenhar(self, tela: pygame.Surface) -> None:
        """
        Desenha a cena do menu na tela.
        Args:
            tela (pygame.Surface): A superfície onde a cena será desenhada.
        """
        tela.fill((240, 240, 240))  
        
        fonte_titulo = pygame.font.SysFont('Arial', 48, bold=True)
        titulo = fonte_titulo.render("Creepiest SWORD", True, (0, 0, 0))
        tela.blit(titulo, (self.jogo.largura//2 - titulo.get_width()//2, 80))
        
        for botao in self.botoes:
            botao.desenhar(tela)