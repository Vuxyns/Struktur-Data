from mazelogic import Maze, MazeSolver

def run_gui(maze, solver):
    """
    GUI untuk visualisasi maze solver

    Fitur:
    - Animasi otomatis
    - Step manual
    - Pause / Resume
    - Reset maze
    - Speed control
    """

    import tkinter as tk

    cell_size = 25
    root = tk.Tk()
    root.title("Maze Solver OOP (Animated + Controls)")

    canvas = tk.Canvas(root,
                       width=maze.cols * cell_size,
                       height=maze.rows * cell_size)
    canvas.pack()

    running = {"value": False}
    delay = {"value": 50}

    def draw():
        """Render maze ke canvas"""
        canvas.delete("all")

        for r in range(maze.rows):
            for c in range(maze.cols):
                x1 = c * cell_size
                y1 = r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                val = maze.grid[r][c]

                color = "white"
                if val == '*': color = "black"
                elif val == 'S': color = "green"
                elif val == 'E': color = "red"
                elif val == 'x': color = "blue"
                elif val == 'o': color = "gray"

                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def solve_step():
        """
        Menjalankan solver 1 langkah (untuk animasi GUI)
        """

        if not running["value"]:
            return

        if not solver.stack:
            solver.stack = [maze.start]

        if solver.stack:
            r, c = solver.stack[-1]

            if (r, c) == maze.end:
                running["value"] = False
                draw()
                return

            solver.visited.add((r, c))
            moved = False

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc

                if solver.is_valid(nr, nc):
                    solver.stack.append((nr, nc))

                    if maze.grid[nr][nc] != 'E':
                        maze.grid[nr][nc] = 'x'

                    moved = True
                    break

            if not moved:
                solver.backtrack()

            draw()
            root.after(delay["value"], solve_step)

    def start():
        running["value"] = True
        solve_step()

    def pause():
        running["value"] = False

    def resume():
        if not running["value"]:
            running["value"] = True
            solve_step()

    def reset():
        running["value"] = False
        solver.stack = []
        solver.visited = set()
        maze.generate_solvable_maze()
        draw()

    def step_manual():
        """Jalankan 1 langkah manual"""
        if not solver.stack:
            solver.stack = [maze.start]

        if solver.stack:
            r, c = solver.stack[-1]

            if (r, c) == maze.end:
                draw()
                return

            solver.visited.add((r, c))
            moved = False

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc

                if solver.is_valid(nr, nc):
                    solver.stack.append((nr, nc))

                    if maze.grid[nr][nc] != 'E':
                        maze.grid[nr][nc] = 'x'

                    moved = True
                    break

            if not moved:
                solver.backtrack()

            draw()

    def update_speed(val):
        delay["value"] = int(val)

    frame = tk.Frame(root)
    frame.pack()

    tk.Button(frame, text="Start", command=start).grid(row=0, column=0)
    tk.Button(frame, text="Pause", command=pause).grid(row=0, column=1)
    tk.Button(frame, text="Resume", command=resume).grid(row=0, column=2)
    tk.Button(frame, text="Step", command=step_manual).grid(row=0, column=3)
    tk.Button(frame, text="Reset", command=reset).grid(row=0, column=4)

    tk.Label(root, text="Speed (ms)").pack()
    speed_slider = tk.Scale(root, from_=10, to=200, orient="horizontal", command=update_speed)
    speed_slider.set(50)
    speed_slider.pack()

    draw()
    root.mainloop()


if __name__ == "__main__":
    """
    PROGRAM UTAMA

    Alur:
    1. Input ukuran maze
    2. Generate maze
    3. Pilih mode (terminal / GUI)
    4. Jalankan solver
    """

    rows = int(input("Baris: "))
    cols = int(input("Kolom: "))

    maze = Maze(rows, cols)
    solver = MazeSolver(maze)

    print("\nPilih mode:")
    print("1. Terminal (animasi)")
    print("2. GUI")

    choice = input("Pilihan: ")

    if choice == '1':
        print("\nMaze awal:\n")
        maze.print_maze()

        found = solver.solve(animate=True)

        print("\nHasil akhir:\n")
        maze.print_maze()

        print("Ditemukan!" if found else "Tidak ada jalur")

    elif choice == '2':
        run_gui(maze, solver)

    else:
        print("Pilihan tidak valid")