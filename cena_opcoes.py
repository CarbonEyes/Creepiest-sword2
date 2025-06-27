import pygame
import sys
from cena import Cena
from botao import Botao
# Importação local de CenaMenu para evitar dependência circular
# from cena_menu import CenaMenu 

class CenaOpcoes(Cena):
    """
    Representa a cena de opções do jogo, onde o jogador pode configurar volumes.
    """
    def __init__(self, jogo):
        """
        Inicializa a CenaOpcoes, configurando sliders e o botão de voltar.
        Args:
            jogo: A instância do jogo principal.
        """
        self.jogo = jogo
        self.botoes = []
        self.fonte = pygame.font.SysFont('Arial', 30)

        # Configurações de sliders
        self.slider_musica_rect = pygame.Rect(self.jogo.largura // 2 - 150, 200, 300, 20)
        self.slider_efeitos_rect = pygame.Rect(self.jogo.largura // 2 - 150, 300, 300, 20)

        # Botão Voltar
        btn_voltar = Botao(
            x=self.jogo.largura // 2 - 100,
            y=450,
            largura=200,
            altura=50,
            texto="Voltar",
            cor_normal=(150, 150, 150),
            cor_hover=(100, 100, 100),
            acao=self.voltar_para_menu
        )
        self.botoes.append(btn_voltar)

        # Variáveis para controle do arrasto dos sliders
        self.arrastando_musica: bool = False
        self.arrastando_efeitos: bool = False
    
    def voltar_para_menu(self) -> None:
        """
        Retorna para a cena do menu principal.
        """
        from cena_menu import CenaMenu # Importação local para evitar ciclo
        self.jogo.mudar_cena(CenaMenu(self.jogo))

    def atualizar(self, eventos: list) -> None:
        """
        Atualiza o estado da cena de opções, processando eventos de mouse para os sliders e botões.
        Args:
            eventos (list): Lista de eventos do Pygame.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Verifica se o mouse está sobre o slider de música
                if self.slider_musica_rect.collidepoint(mouse_x, mouse_y):
                    self.arrastando_musica = True
                # Verifica se o mouse está sobre o slider de efeitos
                elif self.slider_efeitos_rect.collidepoint(mouse_x, mouse_y):
                    self.arrastando_efeitos = True
            
            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                self.arrastando_musica = False
                self.arrastando_efeitos = False
        
        # Lógica para arrastar os sliders
        if self.arrastando_musica:
            novo_x_musica = max(self.slider_musica_rect.left, min(mouse_x, self.slider_musica_rect.right))
            percentual = (novo_x_musica - self.slider_musica_rect.left) / self.slider_musica_rect.width
            self.jogo.definir_volume_musica(percentual) # [cite: 10d]

        if self.arrastando_efeitos:
            novo_x_efeitos = max(self.slider_efeitos_rect.left, min(mouse_x, self.slider_efeitos_rect.right))
            percentual = (novo_x_efeitos - self.slider_efeitos_rect.left) / self.slider_efeitos_rect.width
            self.jogo.definir_volume_efeitos(percentual) # [cite: 10d]

        # Atualiza os botões
        for botao in self.botoes:
            botao.atualizar(eventos)

    def desenhar(self, tela: pygame.Surface) -> None:
        """
        Desenha a cena de opções, incluindo sliders de volume e botões.
        Args:
            tela (pygame.Surface): A superfície onde a cena será desenhada.
        """
        tela.fill((200, 200, 220)) # Fundo cinza azulado claro

        # Desenha título
        fonte_titulo = pygame.font.SysFont('Arial', 40, bold=True)
        titulo = fonte_titulo.render("Opções de Som", True, (0, 0, 0))
        tela.blit(titulo, (self.jogo.largura // 2 - titulo.get_width() // 2, 80))

        # Desenha sliders
        # Slider de Música
        pygame.draw.rect(tela, (180, 180, 180), self.slider_musica_rect) # Fundo do slider
        indicador_musica_x = self.slider_musica_rect.left + (self.slider_musica_rect.width * self.jogo.volume_musica)
        pygame.draw.circle(tela, (50, 150, 50), (int(indicador_musica_x), self.slider_musica_rect.centery), 10) # Indicador verde
        
        texto_musica = self.fonte.render(f"Música: {int(self.jogo.volume_musica * 100)}%", True, (0, 0, 0))
        tela.blit(texto_musica, (self.slider_musica_rect.x, self.slider_musica_rect.y - 30))

        # Slider de Efeitos Sonoros
        pygame.draw.rect(tela, (180, 180, 180), self.slider_efeitos_rect) # Fundo do slider
        indicador_efeitos_x = self.slider_efeitos_rect.left + (self.slider_efeitos_rect.width * self.jogo.volume_efeitos)
        pygame.draw.circle(tela, (150, 50, 50), (int(indicador_efeitos_x), self.slider_efeitos_rect.centery), 10) # Indicador vermelho

        texto_efeitos = self.fonte.render(f"Efeitos: {int(self.jogo.volume_efeitos * 100)}%", True, (0, 0, 0))
        tela.blit(texto_efeitos, (self.slider_efeitos_rect.x, self.slider_efeitos_rect.y - 30))

        # Desenha botões
        for botao in self.botoes:
            botao.desenhar(tela)