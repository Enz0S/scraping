import tkinter as tk
import random

CELL_SIZE = 10
GRID_WIDTH = 60
GRID_HEIGHT = 40

class GameOfLife:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=CELL_SIZE*GRID_WIDTH, height=CELL_SIZE*GRID_HEIGHT)
        self.canvas.pack()
        self.create_board()
        self.draw_board()
        self.start_button = tk.Button(self.window, text="Start", command=self.start)
        self.start_button.pack(side="left")
        self.stop_button = tk.Button(self.window, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")
        self.clear_button = tk.Button(self.window, text="Clear", command=self.clear)
        self.clear_button.pack(side="left")
        self.quit_button = tk.Button(self.window, text="Quit", command=self.window.quit)
        self.quit_button.pack(side="left")
        self.paused = True
        self.window.mainloop()

    def create_board(self):
        self.board = [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def draw_board(self):
        self.canvas.delete(tk.ALL)
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                if self.board[row][col]:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

    def count_neighbors(self, row, col):
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                elif row + i < 0 or row + i >= GRID_HEIGHT or col + j < 0 or col + j >= GRID_WIDTH:
                    continue
                elif self.board[row + i][col + j]:
                    count += 1
        return count

    def update(self):
        new_board = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                neighbors = self.count_neighbors(row, col)
                if self.board[row][col] and (neighbors == 2 or neighbors == 3):
                    new_board[row][col] = True
                elif not self.board[row][col] and neighbors == 3:
                    new_board[row][col] = True
        self.board = new_board
        self.draw_board()
        if not self.paused:
            self.window.after(100, self.update)

    def start(self):
        self.paused = False
        self.update()

    def stop(self):
        self.paused = True

    def clear(self):
        self.board = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.draw_board()

if __name__ == '__main__':
    game = GameOfLife()
