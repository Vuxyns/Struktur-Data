import pygame
import math
import random

# PLAYER ENTITY
class Player:
    def __init__(self, name, angle):
        self.name = name
        self.angle = angle
        self.target_angle = angle
        self.active = True

    def update(self):
        # smooth rotation
        self.angle += (self.target_angle - self.angle) * 0.1

    def get_pos(self, cx, cy, r):
        x = cx + r * math.cos(self.angle)
        y = cy + r * math.sin(self.angle)
        return int(x), int(y)


# HOT POTATO SCENE
class HotPotatoScene:
    def __init__(self, manager):
        self.manager = manager

        self.font = pygame.font.SysFont("Segoe UI", 20)
        self.title_font = pygame.font.SysFont("Segoe UI", 30, bold=True)

        names = ["Budi", "Ani", "Citra", "Dedi", "Eka"]

        # create players in circle
        self.players = []
        for i, name in enumerate(names):
            angle = (i / len(names)) * 2 * math.pi
            self.players.append(Player(name, angle))

        self.num_pass = random.randint(3, 6)
        self.current_pass = 0

        self.holder_index = 0
        self.timer = 0

        self.eliminated_text = ""
        self.winner = None

    # =========================
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.go_to("menu")

    # =========================
    def update(self, dt):
        if self.winner:
            return

        self.timer += dt

        if self.timer > 0.8:
            self.timer = 0

            # rotate potato
            self.holder_index = (self.holder_index + 1) % len(self.players)
            self.current_pass += 1
            self.eliminated_text = ""

            if self.current_pass >= self.num_pass:
                # eliminate
                eliminated = self.players.pop(self.holder_index)
                eliminated.active = False
                self.eliminated_text = f"{eliminated.name} tersingkir!"

                self.current_pass = 0

                if len(self.players) == 1:
                    self.winner = self.players[0]

                self.holder_index %= len(self.players)

        # update smooth positions
        for i, p in enumerate(self.players):
            p.target_angle = (i / len(self.players)) * 2 * math.pi
            p.update()

    # =========================
    def draw(self, screen):
        screen.fill((15,23,42))

        WIDTH, HEIGHT = screen.get_size()
        cx, cy = WIDTH//2, HEIGHT//2 + 20
        radius = 180

        # Title
        title = self.title_font.render("Hot Potato Simulation", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - 180, 30))

        # Draw players
        for i, p in enumerate(self.players):
            x, y = p.get_pos(cx, cy, radius)

            color = (99,102,241)

            if self.winner == p:
                color = (34,197,94)

            pygame.draw.circle(screen, color, (x, y), 35)

            # potato highlight
            if i == self.holder_index and not self.winner:
                pygame.draw.circle(screen, (239,68,68), (x, y), 38, 4)

            name_text = self.font.render(p.name, True, (255,255,255))
            screen.blit(name_text, (x - name_text.get_width()//2, y - 10))

        # status
        if self.winner:
            status = f"Winner: {self.winner.name}"
            color = (34,197,94)
        elif self.eliminated_text:
            status = self.eliminated_text
            color = (239,68,68)
        else:
            status = f"Pass: {self.current_pass}/{self.num_pass}"
            color = (255,255,255)

        status_text = self.font.render(status, True, color)
        screen.blit(status_text, (WIDTH//2 - status_text.get_width()//2, HEIGHT - 50))

        # hint
        hint = self.font.render("ESC = Back to Menu", True, (150,150,150))
        screen.blit(hint, (10, HEIGHT - 30))