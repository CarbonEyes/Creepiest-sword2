import pygame
from cena import Cena 
from characters.player import Player 
from characters.dragon import Dragon
from world.environment import Environment 
from world.coin import Coin 
from cena_menu import CenaMenu 


class CenaJogo(Cena):
    def __init__(self, jogo, initial_game_data: dict = None) -> None:
        self.jogo = jogo
        
        player_height = 110 
        ground_y_top = jogo.altura - 50 
        player_y = ground_y_top - player_height

        self.monster_attack_cooldown_ms: int = 1000 
        self.monster_last_attack_time: int = 0 

        if initial_game_data:
            # CORREÇÃO AQUI: Usar 'initial_game_data' que é o parâmetro de entrada
            player_data = initial_game_data.get("player") 
            environment_data = initial_game_data.get("environment")

            self.player = Player(0, 0, initial_data=player_data) 
            self.environment = Environment(initial_data=environment_data) 
            print("Jogo restaurado de save.")
        else:
            self.player = Player(jogo.largura // 2 - (80//2), player_y) 
            self.environment = Environment() 
            print("Iniciando novo jogo (sem save).")

    def atualizar(self, eventos: list) -> None:
        for evento in eventos:
            self.player.handle_input(evento)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_c: 
                    self.player.coins += 1 
                elif evento.key == pygame.K_x: 
                    self.player.coins += 10 

        self.player.update(self.environment.platforms) 
        self.environment.update(self.player.rect) 

        self._handle_collisions() 
        self._check_game_over()   

    def _handle_collisions(self) -> None: 
        current_time = pygame.time.get_ticks() 

        if self.player.sword.swing_active: 
            player_sword_damage = self.player.sword.get_damage() 

            hit_trees = pygame.sprite.spritecollide(self.player.sword, self.environment.trees, False) 
            for tree in hit_trees:
                coins_gained = tree.take_hit(player_sword_damage) 
                if coins_gained > 0:
                    self.player.coins += coins_gained 

            hit_monsters = pygame.sprite.spritecollide(self.player.sword, self.environment.monsters, False) 
            for monster in hit_monsters:
                coins_gained = monster.take_damage(player_sword_damage) 
                if coins_gained > 0:
                    self.player.coins += coins_gained 
        
            for monster in self.environment.monsters:
                if isinstance(monster, Dragon) and monster.is_alive: 
                    colliding_projectiles = pygame.sprite.spritecollide(self.player.sword, monster.projectiles, False) 
                    for projectile in colliding_projectiles:
                        if not projectile.repelled: 
                            self.player.sword.repel_projectile(projectile, self.player.facing_right) 

        if current_time - self.monster_last_attack_time > self.monster_attack_cooldown_ms:
            colliding_monsters = pygame.sprite.spritecollide(self.player, self.environment.monsters, False)
            for monster in colliding_monsters:
                if monster.is_alive:
                    self.player.health -= monster.damage 
                    self.monster_last_attack_time = current_time 

        for monster_source in self.environment.monsters:
            if isinstance(monster_source, Dragon):
                hit_player_by_projectiles = pygame.sprite.spritecollide(self.player, monster_source.projectiles, True) 
                for projectile in hit_player_by_projectiles:
                    if not projectile.repelled: 
                        self.player.health -= projectile.damage 
                        print(f"Jogador atingido por projétil! Dano: {projectile.damage}")

                for target_monster in self.environment.monsters:
                    if target_monster.is_alive: 
                        repelled_hit_target = pygame.sprite.spritecollide(target_monster, monster_source.projectiles, True) 
                        for projectile in repelled_hit_target:
                            if projectile.repelled and target_monster != self.player: 
                                print(f"{target_monster.__class__.__name__} atingido por projétil repelido! Dano: {projectile.repeller_damage}")
                                coins_gained = target_monster.take_damage(projectile.repeller_damage)
                                if coins_gained > 0:
                                    self.player.coins += coins_gained 

        collected_coins = pygame.sprite.spritecollide(self.player, self.environment.coins, True) 
        for coin in collected_coins:
            self.player.coins += coin.value 

    def _check_game_over(self) -> None: 
        if self.player.health <= 0: 
            print("GAME OVER!")
            from cena_menu import CenaMenu 
            self.jogo.mudar_cena(CenaMenu(self.jogo)) 

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.fill((135, 206, 235)) 
        pygame.draw.rect(tela, (34, 139, 34), (0, self.jogo.altura - 50, self.jogo.largura, 50)) 

        self.environment.draw(tela) 
        self.player.draw(tela) 

        font = pygame.font.SysFont('Arial', 30)
        coin_text = font.render(f"Moedas: {self.player.coins}", True, (0, 0, 0)) 
        tela.blit(coin_text, (10, 10))

        sword_height = self.player.sword.image.get_height()
        sword_size_text = font.render(f"Espada: {sword_height}px", True, (0, 0, 0))
        tela.blit(sword_size_text, (10, 50))

        health_text = font.render(f"Vida: {self.player.health}", True, (0, 0, 0)) 
        tela.blit(health_text, (10, 90))

    # Métodos para fornecer dados para o sistema de save
    def get_player_data(self) -> dict:
        return self.player.to_dict()

    def get_environment_data(self) -> dict:
        return self.environment.to_dict()