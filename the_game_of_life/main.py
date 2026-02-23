import tkinter as tk
import random

class GameOfLife:
    def __init__(self, master):
        self.master = master
        master.title("Game of Life")

        # Default parameters
        self.rows = 20
        self.cols = 20
        self.cell_size = 20
        self.speed = 200  # milliseconds
        self.running = False

        # UI controls
        self.controls_frame = tk.Frame(master)
        self.controls_frame.pack()

        tk.Label(self.controls_frame, text="Rows:").grid(row=0, column=0)
        self.rows_entry = tk.Entry(self.controls_frame, width=5)
        self.rows_entry.grid(row=0, column=1)
        self.rows_entry.insert(0, str(self.rows))

        tk.Label(self.controls_frame, text="Cols:").grid(row=0, column=2)
        self.cols_entry = tk.Entry(self.controls_frame, width=5)
        self.cols_entry.grid(row=0, column=3)
        self.cols_entry.insert(0, str(self.cols))

        tk.Label(self.controls_frame, text="Speed(ms):").grid(row=0, column=4)
        self.speed_entry = tk.Entry(self.controls_frame, width=5)
        self.speed_entry.grid(row=0, column=5)
        self.speed_entry.insert(0, str(self.speed))

        # Bind enter key to update grid/speed
        self.rows_entry.bind("<Return>", self.update_from_entry)
        self.cols_entry.bind("<Return>", self.update_from_entry)
        self.speed_entry.bind("<Return>", self.update_from_entry)

        # Start/Stop toggle button
        self.start_stop_button = tk.Button(self.controls_frame, text="Start", command=self.toggle_start)
        self.start_stop_button.grid(row=0, column=6)

        self.reset_button = tk.Button(self.controls_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=7)

        self.random_button = tk.Button(self.controls_frame, text="Random", command=self.randomize)
        self.random_button.grid(row=0, column=8)

        # Canvas for grid
        self.canvas = tk.Canvas(master, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.create_grid()

    def create_grid(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.rects = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.canvas.config(width=self.cols*self.cell_size, height=self.rows*self.cell_size)
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                self.rects[i][j] = rect

    def update_canvas(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = "black" if self.grid[i][j] == 1 else "white"
                self.canvas.itemconfig(self.rects[i][j], fill=color)

    def next_generation(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                alive_neighbors = sum(
                    self.grid[i + x][j + y]
                    for x in [-1, 0, 1]
                    for y in [-1, 0, 1]
                    if (0 <= i + x < self.rows) and (0 <= j + y < self.cols) and not (x == 0 and y == 0)
                )
                if self.grid[i][j] == 1 and alive_neighbors in [2, 3]:
                    new_grid[i][j] = 1
                elif self.grid[i][j] == 0 and alive_neighbors == 3:
                    new_grid[i][j] = 1
        self.grid = new_grid
        self.update_canvas()
        if self.running:
            self.master.after(self.speed, self.next_generation)

    def toggle_start(self):
        if not self.running:
            self.running = True
            self.start_stop_button.config(text="Stop")
            self.next_generation()
        else:
            self.running = False
            self.start_stop_button.config(text="Start")

    def reset(self):
        self.running = False
        self.start_stop_button.config(text="Start")
        self.create_grid()
        self.update_canvas()

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = random.choice([0, 1])
        self.update_canvas()

    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 0 if self.grid[row][col] == 1 else 1
            self.update_canvas()

    def update_from_entry(self, event):
        try:
            new_rows = int(self.rows_entry.get())
            new_cols = int(self.cols_entry.get())
            new_speed = int(self.speed_entry.get())
            self.rows = new_rows
            self.cols = new_cols
            self.speed = new_speed
        except ValueError:
            return
        self.reset()  # Reset grid with updated parameters

if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()