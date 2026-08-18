import math
import random
import tkinter as tk
from tkinter import messagebox


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ristinolla")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        self.board = [' ' for _ in range(9)]
        self.error_chance = 0.10  # Oletusarvo (vaikea)
        self.human_turn = True
        self.game_active = False

        # käyttöliittymän osat
        self.create_menu()
        self.create_board_ui()

    #vaikeustason valinta
    def create_menu(self):

        self.menu_frame = tk.Frame(self.root, pady=10)
        self.menu_frame.pack()

        self.label = tk.Label(self.menu_frame, text="Valitse vaikeustaso ", font=("Arial", 12))
        self.label.pack()

        self.btn_frame = tk.Frame(self.menu_frame, pady=5)
        self.btn_frame.pack()

        self.easy_btn = tk.Button(self.btn_frame, text="Helppo ", font=("Arial", 10),
                                  command=lambda: self.start_game(0.50), bg="#a3e4d7", width=15)
        self.easy_btn.grid(row=0, column=0, padx=5)

        self.hard_btn = tk.Button(self.btn_frame, text="Vaikea ", font=("Arial", 10),
                                  command=lambda: self.start_game(0.10), bg="#f9e79f", width=15)
        self.hard_btn.grid(row=0, column=1, padx=5)

    # 3 x 3 ruudukko
    def create_board_ui(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(expand=True)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.board_frame, text="", font=("Arial", 24, "bold"), width=5, height=2,
                            command=lambda idx=i: self.on_click(idx), state=tk.DISABLED, disabledforeground="#333")
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(btn)

    #aloittaa uuden pelikierroksen
    def start_game(self, chance):
        self.error_chance = chance
        self.board = [' ' for _ in range(9)]
        self.game_active = True

        # Valintanappien lukitus, pelilaudan aktivointi
        self.easy_btn.config(state=tk.DISABLED)
        self.hard_btn.config(state=tk.DISABLED)

        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, bg="#f2f3f4")

        # Aloittajan arvonta
        self.human_turn = random.choice([True, False])
        if self.human_turn:
            self.label.config(text="Peli alkoi: Sinun vuorosi (X)")
        else:
            self.label.config(text="Peli alkoi: Tietokoneen vuoro (O)")
            self.root.after(600, self.ai_move_trigger)


    def check_winner(self, b, player):
        r1, r2, r3 =[0, 1, 2], [3, 4, 5], [6, 7, 8]
        p1, p2, p3 =[0, 3, 6], [1, 4, 7], [2, 5, 8]
        v1, v2 =[0, 4, 8], [2, 4, 6]
        win_conditions = [r1, r2, r3, p1, p2, p3, v1, v2]
        return any(all(b[cell] == player for cell in condition) for condition in win_conditions)

    def board_full(self, b):
        return ' ' not in b

    def minimax_alphabeta(self, b, depth, alpha, beta, is_maximizing):
        if self.check_winner(b, 'O'): return 10 - depth
        if self.check_winner(b, 'X'): return depth - 10
        if self.board_full(b): return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'O'
                    score = self.minimax_alphabeta(b, depth + 1, alpha, beta, False)
                    b[i] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha: break
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if b[i] == ' ':
                    b[i] = 'X'
                    score = self.minimax_alphabeta(b, depth + 1, alpha, beta, True)
                    b[i] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha: break
            return best_score

    def find_best_move(self):
        best_score = -math.inf
        best_move = -1
        alpha, beta = -math.inf, math.inf
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax_alphabeta(self.board, 0, alpha, beta, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    #Peliklikkauksen käsittely
    def on_click(self, idx):
        if not self.game_active or not self.human_turn or self.board[idx] != ' ':
            return

        # Pelaajan siirto
        self.board[idx] = 'X'
        self.buttons[idx].config(text="X", fg="#2e86c1", state=tk.DISABLED)

        if self.check_game_over('X', "Voitit"):
            return

        self.human_turn = False
        self.label.config(text="Tietokone miettii...")
        # Viive tekemään pelistä luonnollisemman oloisen
        self.root.after(500, self.ai_move_trigger)

    #Tietokoneen siirto laudalla
    def ai_move_trigger(self):
        if not self.game_active:
            return

        if random.random() < self.error_chance:
            empty_cells = [i for i in range(9) if self.board[i] == ' ']
            ai_move = random.choice(empty_cells) if empty_cells else -1
        else:
            ai_move = self.find_best_move()

        if ai_move != -1:
            self.board[ai_move] = 'O'
            self.buttons[ai_move].config(text="O", fg="#cb4335", state=tk.DISABLED)

        if self.check_game_over('O', "Tietokone voitti"):
            return

        self.human_turn = True
        self.label.config(text="Sinun vuorosi (X)")

    def check_game_over(self, player, win_message):
        if self.check_winner(self.board, player) or self.board_full(self.board):
            self.game_active = False
            msg = win_message if self.check_winner(self.board, player) else "Tasapeli!"

            # Kysyy haluaako pelaaja jatkaa
            play_again = messagebox.askyesno("Peli ohi", f"{msg}\nHaluatko pelata uudelleen?")

            if play_again:
                self.easy_btn.config(state=tk.NORMAL)
                self.hard_btn.config(state=tk.NORMAL)
                self.label.config(text="Valitse vaikeustaso aloittaaksesi:")
                for btn in self.buttons:
                    btn.config(text="", state=tk.DISABLED, bg="#f2f3f4")
            else:
                self.root.destroy()
            return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
