import pygame
import random

# Ustawienia gry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Inicjalizacja pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PrinShoot")

# Ustawienie ikony aplikacji
try:
    icon = pygame.image.load("prin.png")  # Zmień na nazwę swojego pliku ikony
    pygame.display.set_icon(icon)
except pygame.error:
    print("Nie można załadować ikony. Upewnij się, że plik istnieje.")

clock = pygame.time.Clock()

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (34, 255, 67)

# Klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, hp):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.hp = hp  # Punkty zdrowia

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:  # W lewo
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:  # W prawo
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:  # W górę
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:  # W dół
            self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # Wyświetlenie HP
        font = pygame.font.Font(None, 36)
        text = font.render(f'HP: {self.hp}', True, BLACK)
        surface.blit(text, (10, 10))

# Klasa pocisku
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Klasa wroga
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
            self.rect.y = random.randint(-100, -40)

# Funkcja główna gry
def game_loop(hp, enemy_speed):
    running = True
    player = Player(hp)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    score = 0  # Zmienna do przechowywania punktów

    for _ in range(5):
        enemy = Enemy(enemy_speed)
        enemy_group.add(enemy)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullet_group.add(bullet)

        # Aktualizacja
        player_group.update()
        bullet_group.update()
        enemy_group.update()

        # Sprawdzanie kolizji
        for bullet in bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)
            for enemy in hit_enemies:
                bullet.kill()
                score += 1  # Zwiększ wynik
                enemy = Enemy(enemy_speed)  # Dodaj nowego wroga po trafieniu
                enemy_group.add(enemy)

        # Sprawdzenie kolizji z wrogami
        if pygame.sprite.spritecollide(player, enemy_group, True):
            player.hp -= 1
            if player.hp <= 0:
                game_over_menu(score)  # Przejdź do końcowego menu
                running = False

        # Rysowanie
        screen.fill(WHITE)
        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)
        player.draw(screen)

        # Wyświetlanie wyniku
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Funkcja menu głównego
def main_menu():
    running = True
    while running:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        title_text = font.render('Menu Główne', True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Wybór poziomu trudności
        font = pygame.font.Font(None, 36)
        easy_text = font.render('1. Łatwy (HP: 5, Szybkość wrogów: 3)', True, BLACK)
        medium_text = font.render('2. Średni (HP: 3, Szybkość wrogów: 5)', True, BLACK)
        hard_text = font.render('3. Trudny (HP: 1, Szybkość wrogów: 7)', True, BLACK)
        exit_text = font.render('4. Wyjdź', True, BLACK)

        screen.blit(easy_text, (100, 200))
        screen.blit(medium_text, (100, 250))
        screen.blit(hard_text, (100, 300))
        screen.blit(exit_text, (100, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop(5, 3)  # Łatwy poziom
                elif event.key == pygame.K_2:
                    game_loop(3, 5)  # Średni poziom
                elif event.key == pygame.K_3:
                    game_loop(1, 7)  # Trudny poziom
                elif event.key == pygame.K_4:
                    running = False

    pygame.quit()

# Funkcja końcowego menu
def game_over_menu(score):
    running = True
    while running:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 74)
        title_text = font.render('Koniec Gry', True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Wyświetlenie wyniku
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Twój wynik: {score}', True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

        # Opcje
        restart_text = font.render('Naciśnij R, aby zagrać ponownie', True, BLACK)
        exit_text = font.render('Naciśnij Q, aby wyjść', True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()  # Powrót do menu głównego
                    running = False
                elif event.key == pygame.K_q:
                    running = False

    pygame.quit()

if __name__ == "__main__":
    main_menu()
