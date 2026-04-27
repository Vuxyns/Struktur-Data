import pygame
import random

# ENTITY: DOCUMENT
class Document:
    def __init__(self, name, x):
        self.name = name
        self.x = x
        self.y = 260
        self.target_x = x
        self.state = "waiting"  # waiting | printing

    def update(self):
        # smooth move (lerp)
        self.x += (self.target_x - self.x) * 0.12

    def draw(self, screen, font):
        if self.state == "printing":
            color = (234,179,8)  # yellow
        else:
            color = (59,130,246)  # blue

        pygame.draw.rect(screen, color, (self.x, self.y, 80, 50), border_radius=10)

        txt = font.render(self.name, True, (255,255,255))
        screen.blit(txt, (self.x + 10, self.y + 15))


# SYSTEM: PRINTER
class PrinterSystem:
    def __init__(self):
        self.queue = []
        self.current = None
        self.progress = 0

        # initial docs
        for i in range(3):
            self.add_document(initial=True, idx=i)

    def add_document(self, initial=False, idx=0):
        name = f"D{random.randint(10,99)}" if not initial else f"Doc{idx+1}"
        doc = Document(name, 900 + idx*90)
        self.queue.append(doc)

    def update(self, dt):
        # set target positions
        for i, doc in enumerate(self.queue):
            doc.target_x = 120 + i * 100
            doc.update()

        # start printing
        if self.current is None and self.queue:
            self.current = self.queue.pop(0)
            self.current.state = "printing"
            self.progress = 0

        # printing process
        if self.current:
            self.progress += 70 * dt
            self.current.x = 650  # lock near printer

            if self.progress >= 100:
                self.current = None


# SCENE
class PrinterScene:
    def __init__(self, manager):
        self.manager = manager

        self.font = pygame.font.SysFont("Segoe UI", 18)
        self.title_font = pygame.font.SysFont("Segoe UI", 30, bold=True)

        self.system = PrinterSystem()
        self.timer = 0

    # =========================
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.go_to("menu")

    # =========================
    def update(self, dt):
        self.timer += dt

        # random arrival
        if self.timer > 2:
            self.timer = 0
            if random.random() < 0.6:
                self.system.add_document()

        self.system.update(dt)

    # =========================
    def draw(self, screen):
        screen.fill((15,23,42))
        WIDTH, HEIGHT = screen.get_size()

        # Title
        title = self.title_font.render("Printer Queue Simulation", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - 180, 30))

        # Flow line
        pygame.draw.line(screen, (71,85,105), (100, 285), (750, 285), 2)

        # Draw queue
        for i, doc in enumerate(self.system.queue):
            doc.draw(screen, self.font)

            # label next
            if i == 0:
                label = self.font.render("NEXT", True, (200,200,200))
                screen.blit(label, (doc.x + 20, doc.y - 25))

        # Draw printer box
        pygame.draw.rect(screen, (30,41,59), (750, 220, 110, 140), border_radius=12)

        ptxt = self.font.render("PRINTER", True, (255,255,255))
        screen.blit(ptxt, (760, 260))

        # Draw current printing
        if self.system.current:
            self.system.current.draw(screen, self.font)

            # progress bar
            pygame.draw.rect(screen, (255,255,255), (630, 380, 180, 12), 1)
            pygame.draw.rect(screen, (34,197,94),
                             (630, 380, (self.system.progress/100)*180, 12))

        # hint
        hint = self.font.render("ESC = Back to Menu", True, (150,150,150))
        screen.blit(hint, (10, HEIGHT - 30))