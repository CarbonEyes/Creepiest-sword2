import json
import os

class SaveLoad:
    """
    Gerencia o salvamento e carregamento do estado do jogo para um arquivo JSON.
    """
    def __init__(self, save_file_name: str = "savegame.json") -> None:
        """
        Inicializa o sistema de save/load.
        Args:
            save_file_name (str): O nome do arquivo onde o jogo será salvo/carregado.
        """
        self.save_file_path = os.path.join("save_data", save_file_name) # Salva em uma pasta separada
        os.makedirs(os.path.dirname(self.save_file_path), exist_ok=True) # Garante que a pasta 'save_data' exista

    def save_game(self, game_data: dict) -> None:
        """
        Salva o estado atual do jogo para um arquivo.
        Args:
            game_data (dict): Um dicionário contendo todo o estado do jogo a ser salvo.
        """
        try:
            with open(self.save_file_path, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=4) # Salva com indentação para legibilidade
            print(f"Jogo salvo com sucesso em: {self.save_file_path}")
        except IOError as e:
            print(f"Erro ao salvar o jogo: {e}")

    def load_game(self) -> dict | None:
        """
        Carrega o estado do jogo de um arquivo.
        Returns:
            dict | None: O dicionário com o estado do jogo se bem-sucedido, None caso contrário.
        """
        if not os.path.exists(self.save_file_path):
            print("Nenhum arquivo de save encontrado. Iniciando novo jogo.")
            return None
        
        try:
            with open(self.save_file_path, 'r', encoding='utf-8') as f:
                game_data = json.load(f)
            print(f"Jogo carregado com sucesso de: {self.save_file_path}")
            return game_data
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar arquivo de save (JSON corrompido): {e}")
            return None
        except IOError as e:
            print(f"Erro ao carregar o jogo: {e}")
            return None
