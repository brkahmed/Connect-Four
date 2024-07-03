import pygame
from pygame.locals import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen_size = pygame.math.Vector2(700, 720)
        self.screen = pygame.display.set_mode(self.screen_size, SCALED)
        pygame.display.set_caption('Connect Four')
        self.event_map = set()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.delta = 1 / self.fps

        self.board = self.new_board()

    def update_event_map(self):
        self.event_map.clear()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.event_map.add(QUIT)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.event_map.add(MOUSEBUTTONDOWN)
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                self.event_map.add(MOUSEBUTTONUP)

    def run(self):
        font = Font(self.screen_size.x // 2)
        players = [Player(1, 'red'), Player(2, 'yellow')]
        while True:
            self.update_event_map()
            if QUIT in self.event_map:
                break
            if MOUSEBUTTONDOWN in self.event_map:
                players[0].add(Token(self, players[0].value))
                players.reverse()

            self.delta = self.clock.tick(self.fps) / 1000

            self.screen.fill('#104a8e')

            self.draw_circle()

            for player in players:
                player.update()
                player.draw()

            if self.is_board_full():
                font.render(self.screen, 'Tie..', '#ddffdd')
                self.reset(players)
            elif self.check_winner(players[1].value):
                font.render(self.screen, f'{players[1].color.capitalize()} Player win!', players[1].color)
                self.reset(players)

            pygame.display.flip()

        pygame.quit()

    def new_board(self):
         return [[0 for __ in range(7)] for _ in range(6)]
    
    def reset(self, players: list['Player']):
        self.board = self.new_board()
        for player in players: player.empty()

    def is_board_full(self) -> bool:
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True
    
    def check_winner(self, target):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                hor = ver = diag1 = diag2 = 0
                for k in range(4):
                    if j + k < len(self.board[i]) and self.board[i][j+k] == target:
                        hor += 1
                    if i + k < len(self.board) and self.board[i+k][j] == target:
                        ver += 1
                    if i + k < len(self.board) and j + k < len(self.board[i]) and self.board[i+k][j+k] == target:
                        diag1 += 1
                    if i + k < len(self.board) and j - k >= 0 and self.board[i+k][j-k] == target:
                        diag2 += 1
                if 4 in [hor, ver, diag1, diag2]: return True
        return False

    def draw_circle(self, radius=45, margin=5):
        for y in range(120 + margin, int(self.screen_size.y), radius * 2 + margin * 2):
            for x in range(margin, int(self.screen_size.x), radius * 2 + margin * 2):
                pygame.draw.circle(self.screen, '#000000', (x+radius, y+radius), radius)

class Font:
    def __init__(self, posx, posy=60, font_size=100) -> None:
        self.font = pygame.font.Font(None, font_size)
        self.posx = posx
        self.posy = posy

    def render(self, surface: pygame.Surface, message: str, color: str):
        f_surf = self.font.render(message, True, color, '#104a8e')
        f_rect = f_surf.get_rect(center=(self.posx, self.posy))
        surface.blit(f_surf, f_rect)
        pygame.display.update(f_rect)
        pygame.time.wait(1500)

class Token(pygame.sprite.Sprite):
    def __init__(self, game: Game, value: int, radius=45) -> None:
        super().__init__()
        self.game = game
        self.value = value
        self.rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        self.rect.center = pygame.mouse.get_pos()
        self.droped = False
        self.dy = 200

    def draw(self, color):
        pygame.draw.circle(self.game.screen,
                           color,
                           self.rect.center,
                           self.rect.width // 2)
        
    def update(self):
        if MOUSEBUTTONUP in self.game.event_map and not self.droped:
            self.column = min(round(self.rect.x / (self.rect.width + 10)), 6)
            self.row = None
            for i in range(len(self.game.board)):
                if self.game.board[i][self.column] == 0:
                    self.row = i
                else: break
            if self.row is None:
                self.kill()
                return
            self.game.board[self.row][self.column] = -1
            self.rect.x = 5 + self.column * (self.rect.width + 10)
            self.droped = True
        if self.droped:
            self.rect.y += self.dy * self.game.delta
            self.dy += 50
            if self.rect.bottom >= 115 + (self.row + 1) * (self.rect.width + 10):
                self.game.board[self.row][self.column] = self.value
                self.rect.bottom = 115 + (self.row + 1) * (self.rect.width + 10)
        else:
            self.rect.centerx = pygame.mouse.get_pos()[0]
            self.rect.centery = 70

class Player(pygame.sprite.Group):
    def __init__(self, value: int, color: str) -> None:
        super().__init__()
        self.value = value
        self.color = color

    def draw(self) -> None:
        for token in self.sprites():
            token.draw(self.color)

if __name__ == '__main__':
    Game().run()