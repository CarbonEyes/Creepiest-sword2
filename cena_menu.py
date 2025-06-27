import pygame
import sys
from botao import Botao
import pygame
from cena import Cena
# Importações locais de CenaJogo e CenaOpcoes para evitar dependências circulares
# from cena_opcoes import CenaOpcoes
# from cena_jogo import CenaJogo

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

        # Criar botões
        btn_jogar = Botao(
            x=jogo.largura//2 - 100,
            y=200,
            largura=200,
            altura=50,
            texto="Novo Jogo", 
            cor_normal=(100, 255, 100),
            cor_hover=(50, 200, 50),
            acao=self.iniciar_novo_jogo 
        )

        btn_continuar = Botao(
            x=jogo.largura//2 - 100,
            y=275, # Posição ajustada para o novo botão
            largura=200,
            altura=50,
            texto="Continuar",
            cor_normal=(100, 150, 255),
            cor_hover=(50, 100, 200),
            acao=self.continuar_jogo
        )
        
        btn_opcoes = Botao(
            x=jogo.largura//2 - 100,
            y=350, # Posição ajustada
            largura=200,
            altura=50,
            texto="Opções",
            cor_normal=(100, 100, 255),
            cor_hover=(50, 50, 200),
            acao=self.ir_para_opcoes 
        )
        
        btn_sair = Botao(
            x=jogo.largura//2 - 100,
            y=425, # Posição ajustada
            largura=200,
            altura=50,
            texto="Sair",
            cor_normal=(255, 100, 100),
            cor_hover=(200, 50, 50),
            acao=self.sair
        )
        
        self.botoes.extend([btn_jogar, btn_continuar, btn_opcoes, btn_sair]) 
    
    def iniciar_novo_jogo(self) -> None:
        """
        Função chamada ao clicar no botão "Novo Jogo".
        Inicia uma nova CenaJogo.
        """
        print("Iniciando novo jogo...")
        from cena_jogo import CenaJogo # Importação local para evitar ciclo
        self.jogo.mudar_cena(CenaJogo(self.jogo)) # Inicia CenaJogo sem dados iniciais
    
    def continuar_jogo(self) -> None:
        """
        Função chamada ao clicar no botão "Continuar".
        Tenta carregar um jogo salvo através do objeto Jogo.
        """
        print("Tentando carregar jogo...")
        self.jogo.load_game_state() # Chama o método de carregamento do Jogo

    def ir_para_opcoes(self) -> None:
        """
        Função chamada ao clicar no botão "Opções", muda para a cena de opções.
        """
        from cena_opcoes import CenaOpcoes # Importação local para evitar ciclo
        self.jogo.mudar_cena(CenaOpcoes(self.jogo))
        
    def sair(self) -> None:
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
        tela.fill((240, 240, 240))  # Fundo cinza claro
        
        fonte_titulo = pygame.font.SysFont('Arial', 48, bold=True)
        titulo = fonte_titulo.render("CYBERBUG 2077", True, (0, 0, 0))
        tela.blit(titulo, (self.jogo.largura//2 - titulo.get_width()//2, 80))
        
        for botao in self.botoes:
            botao.desenhar(tela)
