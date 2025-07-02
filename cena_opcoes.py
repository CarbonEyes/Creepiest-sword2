# cena_opcoes.py
import pygame
import sys
from cena import Cena
from botao import Botao

class CenaOpcoes(Cena):
    """
    Representa a cena de opções do jogo, onde o jogador pode configurar volumes.
    """
    def __init__(self, jogo):
        self.jogo = jogo
        self.botoes = []
        self.fonte = pygame.font.SysFont('Arial', 30)

        self.slider_musica_rect = pygame.Rect(self.jogo.largura // 2 - 150, 200, 300, 20)
        self.slider_efeitos_rect = pygame.Rect(self.jogo.largura // 2 - 150, 300, 300, 20)

        btn_voltar = Botao(
            x=self.jogo.largura // 2 - 100,
            y=450,
            largura=200,
            altura=50,
            texto="Voltar",
            cor_normal=(150, 150, 150),
            cor_hover=(100, 100, 100),
            acao=self._voltar_para_menu 
        )
        self.botoes.append(btn_voltar)

        self.arrastando_musica: bool = False
        self.arrastando_efeitos: bool = False
    
    def _voltar_para_menu(self) -> None: 
        from cena_menu import CenaMenu 
        self.jogo.mudar_cena(CenaMenu(self.jogo))

    def atualizar(self, eventos: list) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.slider_musica_rect.collidepoint(mouse_x, mouse_y):
                    self.arrastando_musica = True
                elif self.slider_efeitos_rect.collidepoint(mouse_x, mouse_y):
                    self.arrastando_efeitos = True
            
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.arrastando_musica = False
                self.arrastando_efeitos = False
        
        if self.arrastando_musica:
            novo_x_musica = max(self.slider_musica_rect.left, min(mouse_x, self.slider_musica_rect.right))
            percentual = (novo_x_musica - self.slider_musica_rect.left) / self.slider_musica_rect.width
            self.jogo.volume_musica = percentual # NOVO: Atribui diretamente à property

        if self.arrastando_efeitos:
            novo_x_efeitos = max(self.slider_efeitos_rect.left, min(mouse_x, self.slider_efeitos_rect.right))
            percentual = (novo_x_efeitos - self.slider_efeitos_rect.left) / self.slider_efeitos_rect.width
            self.jogo.volume_efeitos = percentual # NOVO: Atribui diretamente à property

        for botao in self.botoes:
            botao.atualizar(eventos)

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill((200, 200, 220)) 

        fonte_titulo = pygame.font.SysFont('Arial', 40, bold=True)
        titulo = fonte_titulo.render("Opções de Som", True, (0, 0, 0))
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 80))

        pygame.draw.rect(tela, (180, 180, 180), self.slider_musica_rect) 
        indicador_musica_x = self.slider_musica_rect.left + (self.slider_musica_rect.width * self.jogo.volume_musica) # Acessa a property
        pygame.draw.circle(tela, (50, 150, 50), (int(indicador_musica_x), self.slider_musica_rect.centery), 10) 
        
        texto_musica = self.fonte.render(f"Música: {int(self.jogo.volume_musica * 100)}%", True, (0, 0, 0)) # Acessa a property
        tela.blit(texto_musica, (self.slider_musica_rect.x, self.slider_musica_rect.y - 30))

        pygame.draw.rect(tela, (180, 180, 180), self.slider_efeitos_rect) 
        indicador_efeitos_x = self.slider_efeitos_rect.left + (self.slider_efeitos_rect.width * self.jogo.volume_efeitos) # Acessa a property
        pygame.draw.circle(tela, (150, 50, 50), (int(indicador_efeitos_x), self.slider_efeitos_rect.centery), 10) 

        texto_efeitos = self.fonte.render(f"Efeitos: {int(self.jogo.volume_efeitos * 100)}%", True, (0, 0, 0)) # Acessa a property
        tela.blit(texto_efeitos, (self.slider_efeitos_rect.x, self.slider_efeitos_rect.y - 30))

        for botao in self.botoes:
            botao.desenhar(tela)