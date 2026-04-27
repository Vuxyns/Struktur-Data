import pygame
from collections import deque

# ENTITY: NODE
class Node:
    def __init__(self, name, pos):
        self.name = name
        self.x, self.y = pos
        self.tx, self.ty = pos
        self.state = "idle"  # idle | queued | current | visited
        self.radius = 26
        self.pulse = 0.0

    def update(self, dt):
        # smooth move (kalau nanti mau reposition)
        self.x += (self.tx - self.x) * 0.12
        self.y += (self.ty - self.y) * 0.12

        # pulse untuk node current
        if self.state == "current":
            self.pulse += dt * 6
        else:
            self.pulse = 0

    def draw(self, screen, font):
        # warna berdasarkan state
        if self.state == "current":
            color = (59,130,246)     # biru
        elif self.state == "visited":
            color = (34,197,94)      # hijau
        elif self.state == "queued":
            color = (234,179,8)      # kuning
        else:
            color = (71,85,105)      # abu

        r = self.radius + (2 if self.state == "current" else 0)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), r)

        # outline utk queued biar beda
        if self.state == "queued":
            pygame.draw.circle(screen, (234,179,8), (int(self.x), int(self.y)), r+6, 2)

        # pulse ring saat current
        if self.state == "current":
            pr = r + int(6 + 4 * (1 + pygame.math.Vector2(1,0).rotate_rad(self.pulse).x))
            pygame.draw.circle(screen, (147,197,253), (int(self.x), int(self.y)), pr, 2)

        txt = font.render(self.name, True, (255,255,255))
        screen.blit(txt, (self.x - txt.get_width()//2, self.y - txt.get_height()//2))


# SYSTEM: BFS
class BFSSystem:
    def __init__(self):
        # graph (undirected)
        self.graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E']
        }

        # posisi node (rapi + simetris)
        self.positions = {
            'A': (450, 120),
            'B': (300, 260),
            'C': (600, 260),
            'D': (200, 420),
            'E': (400, 420),
            'F': (650, 420)
        }

        # buat entity node
        self.nodes = {k: Node(k, v) for k, v in self.positions.items()}

        self.q = deque()
        self.visited = set()

        # init BFS dari A
        self.start('A')

        self.current = None
        self.timer = 0
        self.delay = 1.2

    def start(self, start_node):
        self.q.clear()
        self.visited.clear()

        for n in self.nodes.values():
            n.state = "idle"

        self.q.append(start_node)
        self.visited.add(start_node)
        self.nodes[start_node].state = "queued"
        self.current = None

    def step(self):
        # selesai?
        if not self.q:
            if self.current:
                self.nodes[self.current].state = "visited"
            self.current = None
            return

        # ambil node berikutnya
        nxt = self.q.popleft()

        # finalize previous
        if self.current:
            self.nodes[self.current].state = "visited"

        # set current
        self.current = nxt
        self.nodes[nxt].state = "current"

        # enqueue neighbors
        for nb in self.graph[nxt]:
            if nb not in self.visited:
                self.visited.add(nb)
                self.q.append(nb)
                self.nodes[nb].state = "queued"

    def update(self, dt):
        self.timer += dt

        if self.timer > self.delay:
            self.timer = 0
            self.step()

        for n in self.nodes.values():
            n.update(dt)


# SCENE
class BFSScene:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont("Segoe UI", 18)
        self.title_font = pygame.font.SysFont("Segoe UI", 30, bold=True)

        self.sys = BFSSystem()

    # =========================
    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.manager.go_to("menu")
            # restart BFS
            if e.key == pygame.K_r:
                self.sys.start('A')

    # =========================
    def update(self, dt):
        self.sys.update(dt)

    # =========================
    def draw(self, screen):
        screen.fill((15,23,42))
        W, H = screen.get_size()

        # Title
        title = self.title_font.render("BFS (Level-by-Level)", True, (255,255,255))
        screen.blit(title, (W//2 - 160, 30))

        # Edges
        for a, nbrs in self.sys.graph.items():
            for b in nbrs:
                ax, ay = self.sys.nodes[a].x, self.sys.nodes[a].y
                bx, by = self.sys.nodes[b].x, self.sys.nodes[b].y
                pygame.draw.line(screen, (71,85,105), (ax, ay), (bx, by), 2)

        # Nodes
        for n in self.sys.nodes.values():
            n.draw(screen, self.font)

        # Queue display
        q_list = list(self.sys.q)
        q_text = self.font.render(f"Queue: {q_list}", True, (234,179,8))
        screen.blit(q_text, (40, H - 80))

        # Status
        if not self.sys.q and self.sys.current is None:
            status = self.font.render("Traversal selesai", True, (34,197,94))
        else:
            status = self.font.render(f"Current: {self.sys.current}", True, (255,255,255))
        screen.blit(status, (40, H - 50))

        # Legend
        lx, ly = W - 220, 120
        pygame.draw.circle(screen, (59,130,246), (lx, ly), 10)
        screen.blit(self.font.render("Processing", True, (255,255,255)), (lx+20, ly-10))
        pygame.draw.circle(screen, (34,197,94), (lx, ly+30), 10)
        screen.blit(self.font.render("Visited", True, (255,255,255)), (lx+20, ly+20))
        pygame.draw.circle(screen, (234,179,8), (lx, ly+60), 10, 2)
        screen.blit(self.font.render("Queued", True, (255,255,255)), (lx+20, ly+50))

        # Hint
        hint = self.font.render("ESC = Back | R = Restart", True, (150,150,150))
        screen.blit(hint, (10, H - 25))