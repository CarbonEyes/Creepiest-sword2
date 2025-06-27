import pygame
from typing import Callable # Para tipagem de Callables

class Botao:
    """
    Representa um botão interativo na interface do usuário.
    """
    def __init__(self, x: int, y: int, largura: int, altura: int, texto: str, cor_normal: tuple, cor_hover: tuple, acao: Callable | None = None) -> None:
        """
        Inicializa um botão.
        Args:
            x (int): Posição X do botão.
            y (int): Posição Y do botão.
            largura (int): Largura do botão.
            altura (int): Altura do botão.
            texto (str): Texto a ser exibido no botão.
            cor_normal (tuple): Cor do botão quando o mouse não está sobre ele.
            cor_hover (tuple): Cor do botão quando o mouse está sobre ele.
            acao (Callable | None): Função a ser chamada quando o botão é clicado.
        """
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.acao = acao 
        self.cor_atual = cor_normal # Inicializa a cor atual
        
        pygame.font.init() # Garante que o módulo de fontes do Pygame esteja inicializado
        self.fonte = pygame.font.SysFont('Arial', 30) 
        self.clicado: bool = False # Flag para rastrear se foi clicado

    def atualizar(self, eventos: list) -> None:
        """
        Atualiza o estado do botão, verificando hover e cliques.
        Args:
            eventos (list): Lista de eventos do Pygame.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.clicado = False # Reseta o estado de clique a cada atualização

        # Verifica hover
        if self.rect.collidepoint(mouse_pos):
            self.cor_atual = self.cor_hover
            # Verifica clique
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # Botão esquerdo do mouse
                    self.clicado = True
                    if self.acao:
                        self.acao() # Executa a ação associada ao botão
        else:
            self.cor_atual = self.cor_normal
            
    def desenhar(self, tela: pygame.Surface) -> None:
        """
        Desenha o botão na tela.
        Args:
            tela (pygame.Surface): A superfície onde o botão será desenhado.
        """
        # Desenha o retângulo do botão
        pygame.draw.rect(tela, self.cor_atual, self.rect)
        pygame.draw.rect(tela, (0, 0, 0), self.rect, 2)  # Borda preta

        # Desenha o texto
        texto_surf = self.fonte.render(self.texto, True, (0, 0, 0)) # Texto preto
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)
