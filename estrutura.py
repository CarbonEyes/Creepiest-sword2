import pygame
import sys
from abc import ABC, abstractmethod

class Jogo:
    def __init__(self, largura=800, altura=600):
        pygame.init()
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Meu Jogo POO")
        self.clock = pygame.time.Clock()
        self.cena_atual = None
        self.largura = largura
        self.altura = altura
        
    def executar(self):
        while True:
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if self.cena_atual:
                self.cena_atual.atualizar(eventos)
                self.cena_atual.desenhar(self.tela)
            
            pygame.display.flip()
            self.clock.tick(60)

class Cena(ABC):
    @abstractmethod
    def atualizar(self, eventos):
        pass
    
    @abstractmethod
    def desenhar(self, tela):
        pass