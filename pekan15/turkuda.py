import tkinter as tk
from tkinter import ttk, messagebox
import time
from enum import Enum


# =====================================================================
# STRATEGY ENUM
# =====================================================================

class SearchStrategy(Enum):

    BASIC = "Basic Backtracking"

    WARNSDORFF = "Warnsdorff Heuristic"

    GREEDY = "Greedy Strategy"


# =====================================================================
# KNIGHT TOUR SOLVER
# =====================================================================

class KnightsTourAdvanced:

    KNIGHT_MOVES = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]

    def __init__(self, board_size=8):

        self.board_size = board_size

        self.board = [
            [-1 for _ in range(board_size)]
            for _ in range(board_size)
        ]

        self.tour_path = []

        self.statistics = {
            "evaluations": 0,
            "backtracks": 0,
            "time": 0,
            "strategy": None
        }

    # =================================================================
    # VALID MOVE
    # =================================================================

    def is_valid_move(self, x, y):

        return (
            0 <= x < self.board_size
            and
            0 <= y < self.board_size
            and
            self.board[x][y] == -1
        )

    # =================================================================
    # COUNT ONWARD
    # =================================================================

    def count_onward_moves(self, x, y):

        count = 0

        for dx, dy in self.KNIGHT_MOVES:

            if self.is_valid_move(x + dx, y + dy):

                count += 1

        return count

    # =================================================================
    # WARNSDORFF
    # =================================================================

    def get_next_moves_warnsdorff(self, x, y):

        moves = []

        for dx, dy in self.KNIGHT_MOVES:

            nx = x + dx
            ny = y + dy

            if self.is_valid_move(nx, ny):

                onward = self.count_onward_moves(nx, ny)

                moves.append((nx, ny, onward))

        moves.sort(key=lambda m: m[2])

        return [(m[0], m[1]) for m in moves]

    # =================================================================
    # SOLVER
    # =================================================================

    def solve_recursive(
            self,
            x,
            y,
            move_count,
            strategy
    ):

        self.statistics["evaluations"] += 1

        self.board[x][y] = move_count

        self.tour_path.append((x, y))

        # FINISH
        if move_count == self.board_size * self.board_size - 1:

            return True

        # NEXT MOVES
        if strategy == SearchStrategy.WARNSDORFF:

            next_moves = self.get_next_moves_warnsdorff(x, y)

        else:

            next_moves = []

            for dx, dy in self.KNIGHT_MOVES:

                nx = x + dx
                ny = y + dy

                if self.is_valid_move(nx, ny):

                    next_moves.append((nx, ny))

        # TRY MOVE
        for nx, ny in next_moves:

            if self.solve_recursive(
                    nx,
                    ny,
                    move_count + 1,
                    strategy
            ):

                return True

        # BACKTRACK
        self.statistics["backtracks"] += 1

        self.board[x][y] = -1

        self.tour_path.pop()

        return False

    # =================================================================
    # SOLVE
    # =================================================================

    def solve(self, start_x, start_y, strategy):

        self.board = [
            [-1 for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]

        self.tour_path = []

        self.statistics["evaluations"] = 0
        self.statistics["backtracks"] = 0
        self.statistics["strategy"] = strategy.value

        start_time = time.time()

        result = self.solve_recursive(
            start_x,
            start_y,
            0,
            strategy
        )

        self.statistics["time"] = (
                time.time() - start_time
        )

        return result

    # =================================================================
    # VALIDATE
    # =================================================================

    def validate_solution(self):

        if len(self.tour_path) != (
                self.board_size * self.board_size
        ):

            return False

        for i in range(len(self.tour_path) - 1):

            x1, y1 = self.tour_path[i]

            x2, y2 = self.tour_path[i + 1]

            dx = abs(x1 - x2)

            dy = abs(y1 - y2)

            if not (
                    (dx == 2 and dy == 1)
                    or
                    (dx == 1 and dy == 2)
            ):

                return False

        return True


# =====================================================================
# GUI
# =====================================================================

class KnightsTourGUI:

    CELL_SIZE = 70

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Knight's Tour Advanced GUI"
        )

        self.root.geometry("1400x900")

        self.root.configure(bg="#1e1e1e")

        self.board_size = 8

        self.solver = KnightsTourAdvanced(
            self.board_size
        )

        self.create_widgets()

    # =================================================================
    # CREATE WIDGETS
    # =================================================================

    def create_widgets(self):

        # TITLE
        title = tk.Label(
            self.root,
            text="♘ KNIGHT'S TOUR ADVANCED",
            font=("Arial", 28, "bold"),
            bg="#1e1e1e",
            fg="white"
        )

        title.pack(pady=10)

        # MAIN FRAME
        main_frame = tk.Frame(
            self.root,
            bg="#1e1e1e"
        )

        main_frame.pack(fill="both", expand=True)

        # =============================================================
        # LEFT PANEL
        # =============================================================

        left_panel = tk.Frame(
            main_frame,
            bg="#2c2c2c",
            width=300
        )

        left_panel.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        # START POSITION
        tk.Label(
            left_panel,
            text="Posisi Awal",
            font=("Arial", 14, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        pos_frame = tk.Frame(
            left_panel,
            bg="#2c2c2c"
        )

        pos_frame.pack()

        self.x_entry = tk.Entry(
            pos_frame,
            width=5,
            font=("Arial", 12)
        )

        self.x_entry.insert(0, "0")

        self.x_entry.grid(row=0, column=0, padx=5)

        self.y_entry = tk.Entry(
            pos_frame,
            width=5,
            font=("Arial", 12)
        )

        self.y_entry.insert(0, "0")

        self.y_entry.grid(row=0, column=1, padx=5)

        # BOARD SIZE
        tk.Label(
            left_panel,
            text="Ukuran Board",
            font=("Arial", 14, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        self.size_var = tk.StringVar(value="8")

        size_combo = ttk.Combobox(
            left_panel,
            textvariable=self.size_var,
            values=["4", "5", "6", "7", "8"],
            width=10,
            state="readonly"
        )

        size_combo.pack()

        # STRATEGY
        tk.Label(
            left_panel,
            text="Strategy",
            font=("Arial", 14, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        self.strategy_var = tk.StringVar(
            value=SearchStrategy.WARNSDORFF.value
        )

        strategy_combo = ttk.Combobox(
            left_panel,
            textvariable=self.strategy_var,
            values=[s.value for s in SearchStrategy],
            width=25,
            state="readonly"
        )

        strategy_combo.pack()

        # BUTTONS
        self.create_buttons(left_panel)

        # STATISTICS
        tk.Label(
            left_panel,
            text="STATISTICS",
            font=("Arial", 16, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=10)

        self.stats_text = tk.Text(
            left_panel,
            width=35,
            height=18,
            bg="#111111",
            fg="#00ff88",
            font=("Consolas", 10)
        )

        self.stats_text.pack(pady=5)

        # =============================================================
        # RIGHT PANEL
        # =============================================================

        right_panel = tk.Frame(
            main_frame,
            bg="#1e1e1e"
        )

        right_panel.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            right_panel,
            width=850,
            height=850,
            bg="white"
        )

        self.canvas.pack(pady=10)

        self.draw_board()

    # =================================================================
    # BUTTONS
    # =================================================================

    def create_buttons(self, parent):

        style = {
            "font": ("Arial", 11, "bold"),
            "width": 25,
            "height": 2,
            "fg": "white",
            "cursor": "hand2"
        }

        tk.Button(
            parent,
            text="▶ Solve",
            bg="#4CAF50",
            command=self.solve_tour,
            **style
        ).pack(pady=5)

        tk.Button(
            parent,
            text="🎬 Animate",
            bg="#9C27B0",
            command=self.animate_solution,
            **style
        ).pack(pady=5)

        tk.Button(
            parent,
            text="⚡ Compare",
            bg="#2196F3",
            command=self.compare_strategies,
            **style
        ).pack(pady=5)

        tk.Button(
            parent,
            text="✓ Validate",
            bg="#FF9800",
            command=self.validate_solution,
            **style
        ).pack(pady=5)

        tk.Button(
            parent,
            text="🧹 Clear",
            bg="#f44336",
            command=self.clear_board,
            **style
        ).pack(pady=5)

        tk.Button(
            parent,
            text="❌ Exit",
            bg="#607D8B",
            command=self.root.destroy,
            **style
        ).pack(pady=5)

    # =================================================================
    # DRAW BOARD
    # =================================================================

    def draw_board(self):

        self.canvas.delete("all")

        size = self.board_size

        cell = self.CELL_SIZE

        for row in range(size):

            for col in range(size):

                x1 = col * cell + 40
                y1 = row * cell + 40

                x2 = x1 + cell
                y2 = y1 + cell

                color = (
                    "#f0d9b5"
                    if (row + col) % 2 == 0
                    else "#b58863"
                )

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="black"
                )

                value = self.solver.board[row][col]

                if value != -1:

                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text=str(value),
                        font=("Arial", 14, "bold"),
                        fill="blue"
                    )

        # DRAW PATH
        for i in range(len(self.solver.tour_path) - 1):

            x1, y1 = self.solver.tour_path[i]

            x2, y2 = self.solver.tour_path[i + 1]

            cx1 = y1 * cell + 40 + cell // 2
            cy1 = x1 * cell + 40 + cell // 2

            cx2 = y2 * cell + 40 + cell // 2
            cy2 = x2 * cell + 40 + cell // 2

            self.canvas.create_line(
                cx1,
                cy1,
                cx2,
                cy2,
                fill="red",
                width=3,
                arrow=tk.LAST
            )

    # =================================================================
    # SOLVE
    # =================================================================

    def solve_tour(self):

        try:

            self.board_size = int(
                self.size_var.get()
            )

            x = int(self.x_entry.get())

            y = int(self.y_entry.get())

            self.solver = KnightsTourAdvanced(
                self.board_size
            )

            strategy_name = self.strategy_var.get()

            strategy = None

            for s in SearchStrategy:

                if s.value == strategy_name:

                    strategy = s

            found = self.solver.solve(
                x,
                y,
                strategy
            )

            self.draw_board()

            self.show_statistics()

            if found:

                messagebox.showinfo(
                    "Success",
                    "✓ Solusi ditemukan!"
                )

            else:

                messagebox.showerror(
                    "Result",
                    "❌ Tidak ditemukan solusi!"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =================================================================
    # STATISTICS
    # =================================================================

    def show_statistics(self):

        stats = self.solver.statistics

        text = (
            f"Strategy      : {stats['strategy']}\n"
            f"Evaluations   : {stats['evaluations']:,}\n"
            f"Backtracks    : {stats['backtracks']:,}\n"
            f"Execution     : {stats['time']:.6f} sec\n"
            f"Path Length   : {len(self.solver.tour_path)}\n"
            f"Board Size    : {self.board_size}x{self.board_size}\n"
        )

        self.stats_text.delete(1.0, tk.END)

        self.stats_text.insert(tk.END, text)

    # =================================================================
    # VALIDATE
    # =================================================================

    def validate_solution(self):

        if self.solver.validate_solution():

            messagebox.showinfo(
                "Validation",
                "✓ Solusi VALID!"
            )

        else:

            messagebox.showerror(
                "Validation",
                "❌ Solusi tidak valid!"
            )

    # =================================================================
    # COMPARE
    # =================================================================

    def compare_strategies(self):

        x = int(self.x_entry.get())

        y = int(self.y_entry.get())

        result = ""

        for strategy in SearchStrategy:

            solver = KnightsTourAdvanced(
                self.board_size
            )

            found = solver.solve(
                x,
                y,
                strategy
            )

            result += (
                f"{strategy.value}\n"
                f"Found       : {found}\n"
                f"Time        : "
                f"{solver.statistics['time']:.6f}s\n"
                f"Evaluations : "
                f"{solver.statistics['evaluations']:,}\n\n"
            )

        messagebox.showinfo(
            "Compare Strategy",
            result
        )

    # =================================================================
    # ANIMATION
    # =================================================================

    def animate_solution(self):

        self.canvas.delete("all")

        size = self.board_size

        cell = self.CELL_SIZE

        for step, (row, col) in enumerate(
                self.solver.tour_path
        ):

            self.draw_board()

            x1 = col * cell + 40
            y1 = row * cell + 40

            x2 = x1 + cell
            y2 = y1 + cell

            self.canvas.create_oval(
                x1 + 10,
                y1 + 10,
                x2 - 10,
                y2 - 10,
                fill="gold"
            )

            self.canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text="♘",
                font=("Arial", 24, "bold")
            )

            self.root.update()

            time.sleep(0.15)

    # =================================================================
    # CLEAR
    # =================================================================

    def clear_board(self):

        self.solver = KnightsTourAdvanced(
            self.board_size
        )

        self.stats_text.delete(1.0, tk.END)

        self.draw_board()


# =====================================================================
# MAIN
# =====================================================================

def main():

    root = tk.Tk()

    app = KnightsTourGUI(root)

    root.mainloop()


# =====================================================================
# START PROGRAM
# =====================================================================

if __name__ == "__main__":

    main()