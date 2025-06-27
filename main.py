import pygame
import sys
from jogo import Jogo
from cena_menu import CenaMenu

def main():
    """
    Função principal que inicializa o Pygame e inicia o jogo.
    """
    # Cria a instância do jogo
    jogo = Jogo()
    
    # Define a cena inicial para o menu
    # O jogo já inicializa com o menu dentro do __init__
    
    # Inicia o loop principal
    jogo.executar()

if __name__ == "__main__":
    main()
