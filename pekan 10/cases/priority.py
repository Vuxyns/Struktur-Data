import pygame
import random

# ENTITY: PATIENT
class Patient:
    def __init__(self, name, prio, x, y):
        self.name = name
        self.prio = prio
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y

    def update(self):
        # smooth move (lerp)
        self.x += (self.tx - self.x) * 0.15
        self.y += (self.ty - self.y) * 0.15

    def draw(self, screen, font, color):
        pygame.draw.rect(screen, color, (self.x, self.y, 120, 36), border_radius=8)
        txt = font.render(self.name, True, (255,255,255))
        screen.blit(txt, (self.x + 10, self.y + 9))


# SYSTEM: PRIORITY QUEUE
class PrioritySystem:
    def __init__(self):
        self.levels = 4
        self.queues = [[] for _ in range(self.levels)]
        self.current = None
        self.progress = 0

        self.names_pool = ["Gani","Hana","Indra","Juna","Kira","Lutfi","Maya","Nino"]

        # seed awal
        seed = [("Budi",3),("Ani",0),("Citra",2),("Dedi",0),("Eka",1)]
        for i,(n,p) in enumerate(seed):
            self.enqueue(n, p, initial=True, idx=i)

    def enqueue(self, name=None, prio=None, initial=False, idx=0):
        if name is None:
            name = random.choice(self.names_pool)
        if prio is None:
            prio = random.randint(0,3)

        # spawn dari kanan layar
        x0 = 980 + (idx * 20 if initial else 0)
        y0 = 140 + prio * 90
        self.queues[prio].append(Patient(name, prio, x0, y0))

    def dequeue(self):
        # prioritas kecil dulu (0 paling tinggi)
        for lvl in range(self.levels):
            if self.queues[lvl]:
                return self.queues[lvl].pop(0), lvl
        return None, None

    def update(self, dt):
        # layout target per lane
        start_x = 80
        for lvl in range(self.levels):
            lane = self.queues[lvl]
            for i, p in enumerate(lane):
                p.tx = start_x + i * 140
                p.ty = 150 + lvl * 90
                p.update()

        # ambil pasien jika dokter kosong
        if self.current is None:
            p, lvl = self.dequeue()
            if p:
                self.current = p
                self.progress = 0

        # proses layanan
        if self.current:
            self.progress += 60 * dt
            # kunci posisi di area dokter
            self.current.tx = 760
            self.current.ty = 240
            self.current.update()

            if self.progress >= 100:
                self.current = None


# SCENE
class PriorityScene:
    def __init__(self, manager):
        self.manager = manager

        self.font = pygame.font.SysFont("Segoe UI", 18)
        self.title_font = pygame.font.SysFont("Segoe UI", 30, bold=True)

        self.system = PrioritySystem()
        self.spawn_timer = 0

        self.colors = [
            (239,68,68),   # 0 kritis (merah)
            (234,179,8),   # 1 darurat (kuning)
            (59,130,246),  # 2 menengah (biru)
            (34,197,94)    # 3 ringan (hijau)
        ]
        self.labels = ["KRITIS (0)", "DARURAT (1)", "MENENGAH (2)", "RINGAN (3)"]

    # =========================
    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.manager.go_to("menu")
            # input manual (opsional)
            if e.key == pygame.K_1: self.system.enqueue(prio=0)
            if e.key == pygame.K_2: self.system.enqueue(prio=1)
            if e.key == pygame.K_3: self.system.enqueue(prio=2)
            if e.key == pygame.K_4: self.system.enqueue(prio=3)

    # =========================
    def update(self, dt):
        # random arrival
        self.spawn_timer += dt
        if self.spawn_timer > 2.5:
            self.spawn_timer = 0
            if random.random() < 0.7:
                self.system.enqueue()

        self.system.update(dt)

    # =========================
    def draw(self, screen):
        screen.fill((15,23,42))
        W, H = screen.get_size()

        # Title
        title = self.title_font.render("Hospital Priority Queue", True, (255,255,255))
        screen.blit(title, (W//2 - 190, 30))

        # lanes
        start_x = 60
        lane_w = 620
        for i in range(4):
            y = 140 + i*90
            pygame.draw.rect(screen, (30,41,59), (start_x-20, y-10, lane_w, 60), border_radius=10)

            # label
            lab = self.font.render(self.labels[i], True, self.colors[i])
            screen.blit(lab, (start_x-20, y-35))

        # draw patients
        for lvl in range(4):
            for p in self.system.queues[lvl]:
                p.draw(screen, self.font, self.colors[lvl])

        # doctor area
        pygame.draw.rect(screen, (30,41,59), (740, 170, 140, 180), border_radius=12)
        dlab = self.font.render("DOKTER", True, (255,255,255))
        screen.blit(dlab, (760, 180))

        # current patient + progress
        if self.system.current:
            p = self.system.current
            p.draw(screen, self.font, self.colors[p.prio])

            # progress bar
            pygame.draw.rect(screen, (255,255,255), (740, 360, 140, 10), 1)
            pygame.draw.rect(screen, (34,197,94),
                             (740, 360, (self.system.progress/100)*140, 10))

        # hint
        hint = self.font.render("ESC = Back | 1-4 = Add Patient", True, (150,150,150))
        screen.blit(hint, (10, H - 30))