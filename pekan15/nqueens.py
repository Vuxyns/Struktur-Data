import tkinter as tk
from tkinter import ttk, messagebox
import threading
from typing import List, Tuple, Optional
import time

class NQueensSolver:
    """Kelas untuk menyelesaikan masalah N-Queens"""
    
    def __init__(self, n: int):
        """Inisialisasi solver"""
        self.n = n
        self.board = [[-1 for _ in range(n)] for _ in range(n)]
        self.solutions = []
        self.steps = 0
        
    def is_safe(self, row: int, col: int) -> bool:
        """Cek apakah posisi aman untuk menempatkan ratu"""
        # Cek baris sebelumnya
        for i in range(row):
            if self.board[i][col] == 1:
                return False
        
        # Cek diagonal kiri-atas
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j -= 1
        
        # Cek diagonal kanan-atas
        i, j = row - 1, col + 1
        while i >= 0 and j < self.n:
            if self.board[i][j] == 1:
                return False
            i -= 1
            j += 1
        
        return True
    
    def solve(self, row: int = 0) -> bool:
        """Fungsi rekursif untuk menyelesaikan N-Queens"""
        self.steps += 1
        
        if row == self.n:
            solution = [row[:] for row in self.board]
            self.solutions.append(solution)
            return True
        
        found = False
        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                if self.solve(row + 1):
                    found = True
                self.board[row][col] = -1
        
        return found


class NQueensGUI:
    """GUI untuk N-Queens Problem Solver"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Problem Solver")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Styling
        self.setup_styles()
        
        # Variables
        self.solver = None
        self.current_solution = 0
        self.cell_size = 50
        
        # Widgets
        self.create_widgets()
        
    def setup_styles(self):
        """Setup theme dan styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors
        bg_color = '#f0f0f0'
        fg_color = '#333333'
        accent_color = '#2c3e50'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground=accent_color)
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TSpinbox', font=('Segoe UI', 10))
        
        self.root.configure(bg=bg_color)
    
    def create_widgets(self):
        """Buat semua widget GUI"""
        
        # ===== HEADER =====
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=15)
        
        title = ttk.Label(header_frame, text="♛ N-Queens Problem Solver", 
                         style='Title.TLabel')
        title.pack(anchor=tk.W)
        
        subtitle = ttk.Label(header_frame, 
                            text="Cari semua solusi untuk masalah penempatan n ratu pada papan berukuran n×n",
                            font=('Segoe UI', 9), foreground='#666666')
        subtitle.pack(anchor=tk.W)
        
        # ===== INPUT FRAME =====
        input_frame = ttk.LabelFrame(self.root, text="Pengaturan Papan", padding=15)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(input_frame, text="Ukuran Papan (n):").grid(row=0, column=0, sticky=tk.W, padx=10)
        
        self.spinbox_n = ttk.Spinbox(input_frame, from_=1, to=13, width=10, 
                                     font=('Segoe UI', 12))
        self.spinbox_n.set(8)
        self.spinbox_n.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Button untuk solve
        self.btn_solve = ttk.Button(input_frame, text="Cari Solusi", 
                                    command=self.on_solve_click)
        self.btn_solve.grid(row=0, column=2, padx=10, pady=5)
        
        # Info label
        self.info_label = ttk.Label(input_frame, text="", foreground='#27ae60')
        self.info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        
        # ===== CANVAS FRAME =====
        canvas_frame = ttk.LabelFrame(self.root, text="Papan Catur", padding=10)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=2,
                               highlightbackground='#333333')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # ===== CONTROL FRAME =====
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(control_frame, text="Navigasi Solusi:").pack(side=tk.LEFT, padx=5)
        
        self.btn_prev = ttk.Button(control_frame, text="◀ Sebelumnya", 
                                   command=self.show_previous_solution, state=tk.DISABLED)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        
        self.label_solution = ttk.Label(control_frame, text="", 
                                       font=('Segoe UI', 11, 'bold'))
        self.label_solution.pack(side=tk.LEFT, padx=10)
        
        self.btn_next = ttk.Button(control_frame, text="Selanjutnya ▶", 
                                   command=self.show_next_solution, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        # Info statistik
        self.stats_label = ttk.Label(control_frame, text="", foreground='#666666')
        self.stats_label.pack(side=tk.RIGHT, padx=5)
    
    def on_solve_click(self):
        """Handler untuk tombol solve"""
        try:
            n = int(self.spinbox_n.get())
            if n < 1 or n > 13:
                messagebox.showerror("Error", "Ukuran papan harus antara 1 dan 13!")
                return
            
            # Nonaktifkan tombol solve
            self.btn_solve.config(state=tk.DISABLED)
            self.spinbox_n.config(state=tk.DISABLED)
            
            # Update info
            self.info_label.config(text=f"⏳ Mencari solusi untuk n={n}...")
            self.root.update()
            
            # Jalankan solver di thread terpisah untuk tidak membekukan GUI
            thread = threading.Thread(target=self.solve_worker, args=(n,))
            thread.daemon = True
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
    
    def solve_worker(self, n):
        """Worker thread untuk menjalankan solver"""
        try:
            start_time = time.time()
            self.solver = NQueensSolver(n)
            self.solver.solve()
            elapsed_time = time.time() - start_time
            
            self.current_solution = 0
            
            # Update GUI di main thread
            self.root.after(0, lambda: self.on_solve_complete(n, elapsed_time))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.root.after(0, lambda: self.btn_solve.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.spinbox_n.config(state=tk.NORMAL))
    
    def on_solve_complete(self, n, elapsed_time):
        """Called setelah solver selesai"""
        if not self.solver.solutions:
            messagebox.showinfo("Hasil", f"Tidak ada solusi untuk n={n}")
            self.info_label.config(text="❌ Tidak ada solusi ditemukan", foreground='#e74c3c')
        else:
            num_solutions = len(self.solver.solutions)
            self.info_label.config(
                text=f"✅ {num_solutions} solusi ditemukan dalam {elapsed_time:.4f} detik",
                foreground='#27ae60'
            )
            self.stats_label.config(
                text=f"Langkah: {self.solver.steps}"
            )
            
            # Aktifkan tombol navigasi
            self.btn_prev.config(state=tk.NORMAL if num_solutions > 1 else tk.DISABLED)
            self.btn_next.config(state=tk.NORMAL if num_solutions > 1 else tk.DISABLED)
            
            # Tampilkan solusi pertama
            self.show_solution(0)
        
        # Aktifkan tombol solve kembali
        self.btn_solve.config(state=tk.NORMAL)
        self.spinbox_n.config(state=tk.NORMAL)
    
    def show_previous_solution(self):
        """Tampilkan solusi sebelumnya"""
        if self.solver and self.current_solution > 0:
            self.current_solution -= 1
            self.show_solution(self.current_solution)
    
    def show_next_solution(self):
        """Tampilkan solusi berikutnya"""
        if self.solver and self.current_solution < len(self.solver.solutions) - 1:
            self.current_solution += 1
            self.show_solution(self.current_solution)
    
    def show_solution(self, index):
        """Tampilkan solusi dengan index tertentu"""
        if not self.solver or index >= len(self.solver.solutions):
            return
        
        solution = self.solver.solutions[index]
        self.label_solution.config(
            text=f"Solusi {index + 1} dari {len(self.solver.solutions)}"
        )
        
        self.draw_board(solution)
    
    def draw_board(self, solution):
        """Gambar papan dengan solusi"""
        self.canvas.delete("all")
        
        n = self.solver.n
        
        # Hitung ukuran cell berdasarkan ukuran canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Default size jika belum di-render
            canvas_width = 400
            canvas_height = 400
        
        cell_size = min(canvas_width, canvas_height) // n
        cell_size = max(20, cell_size)  # Minimum cell size
        
        board_width = cell_size * n
        board_height = cell_size * n
        
        # Center board
        start_x = (canvas_width - board_width) / 2
        start_y = (canvas_height - board_height) / 2
        
        # Draw cells
        for i in range(n):
            for j in range(n):
                x1 = start_x + j * cell_size
                y1 = start_y + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Alternate colors for chessboard
                color = '#d4a574' if (i + j) % 2 == 0 else '#8b7355'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=2)
                
                # Draw queen if present
                if solution[i][j] == 1:
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2
                    
                    # Draw queen symbol
                    self.canvas.create_text(cx, cy, text='♛', font=('Arial', max(20, cell_size - 10)),
                                           fill='#ff0000')
    
    def on_canvas_resize(self, event):
        """Called ketika canvas di-resize"""
        if self.solver and self.solver.solutions:
            self.draw_board(self.solver.solutions[self.current_solution])


def main():
    root = tk.Tk()
    gui = NQueensGUI(root)
    
    # Bind resize event untuk redraw board
    root.bind('<Configure>', lambda e: gui.on_canvas_resize(e) if e.widget == gui.canvas else None)
    
    root.mainloop()


if __name__ == "__main__":
    main()