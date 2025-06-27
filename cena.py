import pygame
from abc import ABC, abstractmethod

class Cena(ABC):
    """Classe abstrata base para todas as cenas do jogo"""
    @abstractmethod
    def atualizar(self, eventos: list) -> None:
        pass
    
    @abstractmethod
    def desenhar(self, tela: pygame.Surface) -> None:
        pass
