# main.py
import pygame
import sys
import importlib

# Import module scenes (ringkas)
from cases import printer, hot_potato, priority, bfs, ticket

pygame.init()

WIDTH, HEIGHT = 900, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Queue Visual Simulator")

clock = pygame.time.Clock()

# SCENE MAP
SCENE_MAP = {
    "printer": printer.PrinterScene,
    "hot": hot_potato.HotPotatoScene,
    "priority": priority.PriorityScene,
    "bfs": bfs.BFSScene,
    "ticket": ticket.TicketScene
}

# BASE SCENE
class Scene:
    def __init__(self, manager):
        self.manager = manager

    def handle_event(self, e): pass
    def update(self, dt): pass
    def draw(self, screen): pass


# BUTTON UI
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.hover = False
        self.font = pygame.font.SysFont("Segoe UI", 20)

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        color = (79,70,229) if self.hover else (51,65,85)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        txt = self.font.render(self.text, True, (255,255,255))
        screen.blit(txt, (
            self.rect.centerx - txt.get_width()//2,
            self.rect.centery - txt.get_height()//2
        ))


# MENU SCENE
class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        self.title_font = pygame.font.SysFont("Segoe UI", 36, bold=True)

        self.menu_items = [
            ("Printer Queue", "printer"),
            ("Hot Potato", "hot"),
            ("Priority Queue", "priority"),
            ("BFS Graph", "bfs"),
            ("Ticket Simulation", "ticket")
        ]

        self.buttons = []
        for i, (txt, scene) in enumerate(self.menu_items):
            btn = Button(txt, 300, 150 + i*65, 300, 50)
            self.buttons.append((btn, scene))

    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            for btn, scene in self.buttons:
                if btn.rect.collidepoint(e.pos):
                    self.manager.go_to(scene)

    def update(self, dt):
        mouse = pygame.mouse.get_pos()
        for btn, _ in self.buttons:
            btn.update(mouse)

    def draw(self, screen):
        screen.fill((15,23,42))

        title = self.title_font.render("Queue Visual Simulator", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - 230, 70))

        for btn, _ in self.buttons:
            btn.draw(screen)


# SCENE MANAGER
class SceneManager:
    def __init__(self):
        self.scene = MenuScene(self)

    def go_to(self, name):
        if name == "menu":
            self.scene = MenuScene(self)
            return

        # 1. pakai map (utama)
        if name in SCENE_MAP:
            self.scene = SCENE_MAP[name](self)
            return

        # 2. fallback auto import
        try:
            module = importlib.import_module(f"scenes.{name}")
            class_name = ''.join(word.capitalize() for word in name.split('_')) + "Scene"
            SceneClass = getattr(module, class_name)
            self.scene = SceneClass(self)
        except Exception as e:
            print(f"[ERROR] Scene '{name}' tidak ditemukan:", e)
            self.scene = MenuScene(self)

    def handle_event(self, e):
        self.scene.handle_event(e)

    def update(self, dt):
        self.scene.update(dt)

    def draw(self, screen):
        self.scene.draw(screen)


# MAIN LOOP
def main():
    manager = SceneManager()

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            manager.handle_event(e)

        manager.update(dt)
        manager.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()