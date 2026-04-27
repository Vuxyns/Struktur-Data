import pygame
import random

# ENTITY: PASSENGER
class Passenger:
    def __init__(self, arrival_time, x):
        self.arrival = arrival_time
        self.x = x
        self.y = 420
        self.tx = x

    def update(self):
        self.x += (self.tx - self.x) * 0.15

    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (int(self.x), int(self.y)), 10)


# ENTITY: AGENT
class Agent:
    def __init__(self, x, idx):
        self.x = x
        self.y = 220
        self.idx = idx

        self.busy = False
        self.timer = 0
        self.duration = 0

    def start(self, duration):
        self.busy = True
        self.timer = 0
        self.duration = duration

    def update(self, dt):
        if self.busy:
            self.timer += dt
            if self.timer >= self.duration:
                self.busy = False
                return True
        return False

    def draw(self, screen, font):
        color = (239,68,68) if self.busy else (34,197,94)

        pygame.draw.rect(screen, (30,41,59), (self.x, self.y, 100, 100), border_radius=12)
        pygame.draw.circle(screen, color, (self.x+50, self.y+50), 30)

        label = font.render(f"Loket {self.idx}", True, (255,255,255))
        screen.blit(label, (self.x+50 - label.get_width()//2, self.y+110))


# SYSTEM
class TicketSystem:
    def __init__(self):
        self.queue = []
        self.agents = [Agent(350 + i*140, i+1) for i in range(3)]

        self.time = 0
        self.spawn_timer = 0

        self.total_served = 0
        self.total_wait = 0

    def update(self, dt):
        self.time += dt
        self.spawn_timer += dt

        # random arrival
        if self.spawn_timer > 0.4:
            self.spawn_timer = 0
            if random.random() < 0.6:
                self.queue.append(Passenger(self.time, 1000))

        # set queue positions
        for i, p in enumerate(self.queue):
            p.tx = 120 + i * 35
            p.update()

        # agent logic
        for agent in self.agents:
            finished = agent.update(dt)

            if finished:
                self.total_served += 1

            if not agent.busy and self.queue:
                p = self.queue.pop(0)
                wait = self.time - p.arrival
                self.total_wait += wait

                agent.start(random.uniform(1.0, 3.0))

    def avg_wait(self):
        return self.total_wait / self.total_served if self.total_served > 0 else 0


# SCENE
class TicketScene:
    def __init__(self, manager):
        self.manager = manager

        self.font = pygame.font.SysFont("Segoe UI", 18)
        self.title_font = pygame.font.SysFont("Segoe UI", 28, bold=True)

        self.sys = TicketSystem()

    # =========================
    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.manager.go_to("menu")

    # =========================
    def update(self, dt):
        self.sys.update(dt)

    # =========================
    def draw(self, screen):
        screen.fill((15,23,42))
        W, H = screen.get_size()

        # Title
        title = self.title_font.render("Airport Ticket Simulation", True, (255,255,255))
        screen.blit(title, (W//2 - 170, 30))

        # Draw agents
        for a in self.sys.agents:
            a.draw(screen, self.font)

        # Draw queue
        for i, p in enumerate(self.sys.queue):
            p.draw(screen)
            if i == 0:
                pygame.draw.circle(screen, (234,179,8), (int(p.x), int(p.y)), 13, 2)

        # Stats panel
        stats = [
            f"Served: {self.sys.total_served}",
            f"In Queue: {len(self.sys.queue)}",
            f"Avg Wait: {self.sys.avg_wait():.2f}s"
        ]

        for i, txt in enumerate(stats):
            render = self.font.render(txt, True, (255,255,255))
            screen.blit(render, (20, 80 + i*25))

        # hint
        hint = self.font.render("ESC = Back to Menu", True, (150,150,150))
        screen.blit(hint, (10, H - 30))