import random, time

class Maze:
    """
    =========================
    MAZE ADT (Abstract Data Type)
    =========================

    Class ini bertanggung jawab untuk:
    - Menyimpan struktur grid (labirin)
    - Menentukan posisi start (S) dan end (E)
    - Generate labirin random yang pasti solvable

    Representasi:
    - '*' = dinding
    - ' ' = jalan
    - 'S' = start
    - 'E' = exit
    """

    def __init__(self, rows, cols):
        """
        Inisialisasi maze dengan ukuran tertentu

        rows : jumlah baris
        cols : jumlah kolom
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.start = None
        self.end = None

        # langsung generate maze
        self.generate_solvable_maze()

    def generate_solvable_maze(self):
        """
        Membuat maze random
        + Dijamin ADA jalur dari start ke end

        Strategi:
        1. Isi grid random (dinding/jalan)
        2. Paksa jalur dari (0,0) ke (rows-1, cols-1)
        """

        # isi random
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = '*' if random.random() < 0.3 else ' '

        # paksa jalur
        r, c = 0, 0
        self.grid[r][c] = ' '

        while r < self.rows - 1 or c < self.cols - 1:
            if random.random() < 0.5 and r < self.rows - 1:
                r += 1
            elif c < self.cols - 1:
                c += 1

            self.grid[r][c] = ' '

        # set start & end
        self.start = (0, 0)
        self.end = (self.rows - 1, self.cols - 1)

        self.grid[0][0] = 'S'
        self.grid[self.rows - 1][self.cols - 1] = 'E'

    def print_maze(self):
        """
        Menampilkan maze ke terminal
        """
        for row in self.grid:
            print(' '.join(row))
        print()


class MazeSolver:
    """
    =========================
    MAZE SOLVER (Backtracking)
    =========================

    Class ini bertanggung jawab untuk:
    - Mencari jalur dari S ke E
    - Menggunakan algoritma DFS (Depth First Search)
    - Implementasi NON-RECURSIVE (pakai stack)

    Penandaan:
    - 'x' = jalur benar
    - 'o' = jalan buntu
    """

    def __init__(self, maze):
        """
        maze : objek Maze yang akan diselesaikan
        """
        self.maze = maze
        self.stack = []      # stack untuk backtracking
        self.visited = set() # menyimpan posisi yang sudah dikunjungi

    def solve(self, animate=False):
        """
        Menjalankan algoritma pencarian jalur

        Langkah:
        1. Mulai dari S
        2. Coba bergerak ke 4 arah
        3. Jika buntu → mundur (backtrack)
        4. Jika sampai E → selesai

        animate = True → tampilkan animasi di terminal
        """

        self.stack = [self.maze.start]

        while self.stack:
            r, c = self.stack[-1]

            # jika sampai tujuan
            if (r, c) == self.maze.end:
                return True

            self.visited.add((r, c))

            moved = False

            # arah gerak: atas, bawah, kiri, kanan
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc

                if self.is_valid(nr, nc):
                    # maju
                    self.stack.append((nr, nc))

                    # tandai jalur
                    if self.maze.grid[nr][nc] != 'E':
                        self.maze.grid[nr][nc] = 'x'

                    moved = True
                    break

            # jika tidak bisa maju → backtrack
            if not moved:
                self.backtrack()

            # animasi terminal
            if animate:
                time.sleep(0.05)
                print("\033[H\033[J", end="")
                self.maze.print_maze()

        return False

    def is_valid(self, r, c):
        """
        Mengecek apakah posisi valid untuk dikunjungi

        Syarat:
        - Tidak keluar grid
        - Bukan dinding (*)
        - Belum pernah dikunjungi
        """
        return (
            0 <= r < self.maze.rows and
            0 <= c < self.maze.cols and
            self.maze.grid[r][c] != '*' and
            (r, c) not in self.visited
        )

    def backtrack(self):
        """
        Proses mundur saat jalan buntu

        - Pop dari stack
        - Tandai sebagai 'o'
        """
        r, c = self.stack.pop()

        if self.maze.grid[r][c] not in ['S', 'E']:
            self.maze.grid[r][c] = 'o'