import tkinter as tk
from tkinter import ttk, messagebox
import time
from enum import Enum


# =====================================================================
# STRATEGY ENUM
# =====================================================================

class Strategy(Enum):

    RECURSIVE = "Recursive Backtracking"

    DYNAMIC = "Dynamic Programming"

    GREEDY = "Greedy Strategy"


# =====================================================================
# KNAPSACK SOLVER
# =====================================================================

class KnapsackSolver:

    def __init__(self, items=None, target=30):

        self.items = items if items else [
            2, 5, 6, 9, 12, 14, 20
        ]

        self.target = target

        self.solution = []

        self.statistics = {
            "strategy": None,
            "time": 0,
            "evaluations": 0,
            "backtracks": 0
        }

    # =================================================================
    # RESET
    # =================================================================

    def reset_statistics(self):

        self.statistics = {
            "strategy": None,
            "time": 0,
            "evaluations": 0,
            "backtracks": 0
        }

    # =================================================================
    # RECURSIVE
    # =================================================================

    def recursive_solver(
            self,
            index=0,
            current=None,
            current_sum=0
    ):

        self.statistics["evaluations"] += 1

        if current is None:
            current = []

        # TARGET FOUND
        if current_sum == self.target:
            return current

        # INVALID
        if (
                current_sum > self.target
                or
                index >= len(self.items)
        ):

            self.statistics["backtracks"] += 1

            return None

        # INCLUDE
        include = self.recursive_solver(
            index + 1,
            current + [self.items[index]],
            current_sum + self.items[index]
        )

        if include:
            return include

        # EXCLUDE
        exclude = self.recursive_solver(
            index + 1,
            current,
            current_sum
        )

        return exclude

    # =================================================================
    # DYNAMIC
    # =================================================================

    def dynamic_solver(self):

        n = len(self.items)

        target = self.target

        dp = [[False for _ in range(target + 1)]
              for _ in range(n + 1)]

        dp[0][0] = True

        for i in range(1, n + 1):

            for w in range(target + 1):

                self.statistics["evaluations"] += 1

                dp[i][w] = dp[i - 1][w]

                if w >= self.items[i - 1]:

                    dp[i][w] = (
                            dp[i][w]
                            or
                            dp[i - 1][w - self.items[i - 1]]
                    )

        if not dp[n][target]:
            return None

        result = []

        w = target

        for i in range(n, 0, -1):

            if not dp[i - 1][w]:

                result.append(self.items[i - 1])

                w -= self.items[i - 1]

        return result[::-1]

    # =================================================================
    # GREEDY
    # =================================================================

    def greedy_solver(self):

        items_sorted = sorted(
            self.items,
            reverse=True
        )

        result = []

        total = 0

        for item in items_sorted:

            self.statistics["evaluations"] += 1

            if total + item <= self.target:

                result.append(item)

                total += item

        return result

    # =================================================================
    # SOLVE
    # =================================================================

    def solve(self, strategy):

        self.reset_statistics()

        self.statistics["strategy"] = strategy.value

        start = time.time()

        if strategy == Strategy.RECURSIVE:

            self.solution = self.recursive_solver()

        elif strategy == Strategy.DYNAMIC:

            self.solution = self.dynamic_solver()

        elif strategy == Strategy.GREEDY:

            self.solution = self.greedy_solver()

        self.statistics["time"] = time.time() - start

        return self.solution


# =====================================================================
# GUI
# =====================================================================

class KnapsackGUI:

    CELL_SIZE = 120

    def __init__(self, root):

        self.root = root

        self.root.title("Knapsack Chess Visual GUI")

        self.root.geometry("1300x850")

        self.root.configure(bg="#1e1e1e")

        self.solver = KnapsackSolver()

        self.history = []

        self.create_widgets()

    # =================================================================
    # CREATE WIDGETS
    # =================================================================

    def create_widgets(self):

        # TITLE
        title = tk.Label(
            self.root,
            text="♞ KNAPSACK CHESS VISUAL",
            font=("Arial", 28, "bold"),
            bg="#1e1e1e",
            fg="white"
        )

        title.pack(pady=15)

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
            width=320
        )

        left_panel.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        # INPUT ITEMS
        tk.Label(
            left_panel,
            text="Daftar Barang",
            font=("Arial", 14, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=(15, 5))

        self.items_entry = tk.Entry(
            left_panel,
            width=30,
            font=("Arial", 12)
        )

        self.items_entry.insert(
            0,
            "2 5 6 9 12 14 20"
        )

        self.items_entry.pack(pady=5)

        # TARGET
        tk.Label(
            left_panel,
            text="Target Berat",
            font=("Arial", 14, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=(15, 5))

        self.target_entry = tk.Entry(
            left_panel,
            width=15,
            font=("Arial", 12)
        )

        self.target_entry.insert(0, "30")

        self.target_entry.pack(pady=5)

        # STRATEGY
        tk.Label(
            left_panel,
            text="Strategy",
            font=("Arial", 14, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=(15, 5))

        self.strategy_var = tk.StringVar(
            value=Strategy.RECURSIVE.value
        )

        strategy_combo = ttk.Combobox(
            left_panel,
            textvariable=self.strategy_var,
            values=[s.value for s in Strategy],
            width=25,
            state="readonly"
        )

        strategy_combo.pack(pady=5)

        # BUTTONS
        self.create_buttons(left_panel)

        # STATISTICS
        tk.Label(
            left_panel,
            text="STATISTICS",
            font=("Arial", 16, "bold"),
            bg="#2c2c2c",
            fg="white"
        ).pack(pady=(20, 5))

        self.stats_text = tk.Text(
            left_panel,
            width=35,
            height=15,
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
            height=700,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack(pady=20)

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
            command=self.solve_problem,
            **style
        ).pack(pady=5)

        tk.Button(
            parent,
            text="⚡ Compare Strategy",
            bg="#2196F3",
            command=self.compare_strategies,
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
    # GET DATA
    # =================================================================

    def get_input_data(self):

        items = list(
            map(
                int,
                self.items_entry.get().split()
            )
        )

        target = int(
            self.target_entry.get()
        )

        return items, target

    # =================================================================
    # DRAW BOARD
    # =================================================================

    def draw_board(self):

        self.canvas.delete("all")

        items = self.solver.items

        cols = 4

        cell = self.CELL_SIZE

        for i, item in enumerate(items):

            row = i // cols
            col = i % cols

            x1 = col * cell + 50
            y1 = row * cell + 50

            x2 = x1 + cell
            y2 = y1 + cell

            color = (
                "#f0d9b5"
                if (row + col) % 2 == 0
                else "#b58863"
            )

            if item in self.solver.solution:
                color = "#4CAF50"

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black",
                width=3
            )

            symbol = (
                "♞"
                if item in self.solver.solution
                else "·"
            )

            self.canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2 - 15,
                text=symbol,
                font=("Arial", 26, "bold")
            )

            self.canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2 + 20,
                text=f"{item}",
                font=("Arial", 16, "bold")
            )

    # =================================================================
    # SOLVE
    # =================================================================

    def solve_problem(self):

        try:

            items, target = self.get_input_data()

            self.solver = KnapsackSolver(
                items,
                target
            )

            strategy_name = self.strategy_var.get()

            strategy = None

            for s in Strategy:

                if s.value == strategy_name:
                    strategy = s

            result = self.solver.solve(strategy)

            self.draw_board()

            self.show_statistics()

            self.history.append({
                "strategy": strategy.value,
                "solution": result
            })

            if result:

                messagebox.showinfo(
                    "Success",
                    f"Solusi ditemukan!\n\n"
                    f"{result}\n"
                    f"Total = {sum(result)}"
                )

            else:

                messagebox.showwarning(
                    "Result",
                    "Tidak ditemukan solusi"
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =================================================================
    # SHOW STATS
    # =================================================================

    def show_statistics(self):

        stats = self.solver.statistics

        text = (
            f"Strategy     : {stats['strategy']}\n"
            f"Evaluations  : {stats['evaluations']:,}\n"
            f"Backtracks   : {stats['backtracks']:,}\n"
            f"Execution    : {stats['time']:.6f} sec\n"
            f"Target       : {self.solver.target}\n"
            f"Solution     : {self.solver.solution}\n"
        )

        self.stats_text.delete(1.0, tk.END)

        self.stats_text.insert(tk.END, text)

    # =================================================================
    # COMPARE
    # =================================================================

    def compare_strategies(self):

        items, target = self.get_input_data()

        result = ""

        for strategy in Strategy:

            solver = KnapsackSolver(
                items,
                target
            )

            solution = solver.solve(strategy)

            result += (
                f"{strategy.value}\n"
                f"Solution    : {solution}\n"
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
    # VALIDATE
    # =================================================================

    def validate_solution(self):

        if not self.solver.solution:

            messagebox.showwarning(
                "Validation",
                "Belum ada solusi!"
            )

            return

        total = sum(self.solver.solution)

        if total <= self.solver.target:

            messagebox.showinfo(
                "Validation",
                "✓ Solusi VALID!"
            )

        else:

            messagebox.showerror(
                "Validation",
                "❌ Solusi TIDAK VALID!"
            )

    # =================================================================
    # ANIMATION
    # =================================================================

    def animate_solution(self):

        self.canvas.delete("all")

        items = self.solver.items

        cols = 4

        cell = self.CELL_SIZE

        for i, item in enumerate(items):

            row = i // cols
            col = i % cols

            x1 = col * cell + 50
            y1 = row * cell + 50

            x2 = x1 + cell
            y2 = y1 + cell

            color = "#b58863"

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="black",
                width=3
            )

            self.canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text=str(item),
                font=("Arial", 16, "bold")
            )

            self.root.update()

            time.sleep(0.2)

            if item in self.solver.solution:

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#4CAF50",
                    outline="black",
                    width=3
                )

                self.canvas.create_text(
                    (x1 + x2) // 2,
                    (y1 + y2) // 2 - 15,
                    text="♞",
                    font=("Arial", 26, "bold")
                )

                self.canvas.create_text(
                    (x1 + x2) // 2,
                    (y1 + y2) // 2 + 20,
                    text=str(item),
                    font=("Arial", 16, "bold")
                )

                self.root.update()

                time.sleep(0.3)

    # =================================================================
    # CLEAR
    # =================================================================

    def clear_board(self):

        self.canvas.delete("all")

        self.stats_text.delete(1.0, tk.END)

        self.solver.solution = []

        self.draw_board()


# =====================================================================
# MAIN
# =====================================================================

def main():

    root = tk.Tk()

    app = KnapsackGUI(root)

    root.mainloop()


# =====================================================================
# START
# =====================================================================

if __name__ == "__main__":

    main()