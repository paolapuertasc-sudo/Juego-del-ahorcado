
import tkinter as tk
from tkinter import ttk, messagebox
from .engine_core import GameState, try_letter, start_new_game, ALPHABET

class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ahorcado (GUI)")
        self.resizable(False, False)

        self.state: GameState | None = None

        self._build_controls()
        self._build_canvas()
        self._build_keyboard()
        self._new_game("medio")

    # ---------------- UI BUILD ----------------
    def _build_controls(self):
        top = ttk.Frame(self, padding=10)
        top.grid(row=0, column=0, sticky="ew")

        ttk.Label(top, text="Dificultad:").grid(row=0, column=0, padx=(0,6))
        self.difficulty = tk.StringVar(value="medio")
        for i, (txt, val) in enumerate([("Fácil", "facil"), ("Medio", "medio"), ("Difícil", "dificil")]):
            rb = ttk.Radiobutton(top, text=txt, value=val, variable=self.difficulty, command=self._on_diff_change)
            rb.grid(row=0, column=i+1, padx=4)

        self.progress_lbl = ttk.Label(top, text="", font=("Consolas", 20))
        self.progress_lbl.grid(row=1, column=0, columnspan=5, pady=(10,0))

        stats = ttk.Frame(top)
        stats.grid(row=2, column=0, columnspan=5, pady=(6,0), sticky="ew")
        self.attempts_lbl = ttk.Label(stats, text="Intentos: -")
        self.attempts_lbl.pack(side="left")
        self.used_lbl = ttk.Label(stats, text="Usadas: -")
        self.used_lbl.pack(side="right")

        btns = ttk.Frame(top)
        btns.grid(row=3, column=0, columnspan=5, pady=(8,0))
        ttk.Button(btns, text="Nueva partida", command=lambda: self._new_game(self.difficulty.get())).pack(side="left", padx=4)
        ttk.Button(btns, text="Salir", command=self.destroy).pack(side="left", padx=4)

        self.msg_lbl = ttk.Label(top, text="", foreground="black")
        self.msg_lbl.grid(row=4, column=0, columnspan=5, pady=(8,0))

    def _build_canvas(self):
        mid = ttk.Frame(self, padding=(10,0,10,10))
        mid.grid(row=1, column=0)
        self.canvas = tk.Canvas(mid, width=260, height=260, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack()

    def _build_keyboard(self):
        kb_frame = ttk.Frame(self, padding=(10,0,10,10))
        kb_frame.grid(row=2, column=0)
        rows = ["qwertyuiop", "asdfghjklñ", "zxcvbnm"]
        self.letter_btns: dict[str, ttk.Button] = {}
        for r, row in enumerate(rows):
            fr = ttk.Frame(kb_frame)
            fr.pack()
            for ch in row:
                b = ttk.Button(fr, text=ch.upper(), width=3, command=lambda c=ch: self._press(c))
                b.pack(side="left", padx=2, pady=2)
                self.letter_btns[ch] = b

    # ---------------- GAME LOGIC ----------------
    def _new_game(self, difficulty: str):
        from .engine_core import start_new_game  # lazy import
        self.state = start_new_game(difficulty)
        self.msg_lbl.config(text="Nueva partida iniciada.")
        for b in self.letter_btns.values():
            b.state(["!disabled"])
        self._refresh_ui()

    def _on_diff_change(self):
        # Reiniciar al cambiar dificultad
        self._new_game(self.difficulty.get())

    def _press(self, ch: str):
        if not self.state or self.state.finished():
            return
        ok, msg = try_letter(self.state, ch)
        self.msg_lbl.config(text=msg)
        # Deshabilitar botón usado si es válido
        if ch in self.letter_btns:
            self.letter_btns[ch].state(["disabled"])
        self._refresh_ui()
        if self.state.finished():
            self._end_game()

    def _refresh_ui(self):
        if not self.state:
            return
        self.progress_lbl.config(text=" ".join(self.state.progress).upper())
        self.attempts_lbl.config(text=f"Intentos: {self.state.attempts}")
        used_sorted = " ".join(sorted(self.state.used)).upper() or "-"
        self.used_lbl.config(text=f"Usadas: {used_sorted}")
        self._draw_hangman()

    def _end_game(self):
        if not self.state:
            return
        if self.state.won():
            self.msg_lbl.config(text="🎉 ¡Ganaste!")
            messagebox.showinfo("Fin", "🎉 ¡Ganaste!")
        else:
            self.msg_lbl.config(text=f"💀 Perdiste. La palabra era: {self.state.secret.upper()}")
            messagebox.showwarning("Fin", f"💀 Perdiste.\nLa palabra era: {self.state.secret.upper()}")
        # Deshabilitar teclado
        for b in self.letter_btns.values():
            b.state(["disabled"])

    # ---------------- DRAWING ----------------
    def _draw_hangman(self):
        self.canvas.delete("all")
        if not self.state:
            return
        mistakes = self.state.max_attempts - self.state.attempts
        # Base y poste
        self.canvas.create_line(20,240,240,240)   # base
        self.canvas.create_line(60,240,60,20)     # poste vertical
        self.canvas.create_line(60,20,170,20)     # brazo
        self.canvas.create_line(170,20,170,50)    # cuerda

        steps = [
            lambda: self.canvas.create_oval(150,50,190,90),        # cabeza
            lambda: self.canvas.create_line(170,90,170,160),       # torso
            lambda: self.canvas.create_line(170,110,145,135),      # brazo izq
            lambda: self.canvas.create_line(170,110,195,135),      # brazo der
            lambda: self.canvas.create_line(170,160,150,200),      # pierna izq
            lambda: self.canvas.create_line(170,160,190,200),      # pierna der
            # extras si hay más errores permitidos
            lambda: self.canvas.create_oval(160,65,165,70),        # ojo izq
            lambda: self.canvas.create_oval(175,65,180,70),        # ojo der
        ]

        for i in range(min(mistakes, len(steps))):
            steps[i]()

def main():
    app = HangmanApp()
    app.mainloop()

if __name__ == "__main__":
    main()
