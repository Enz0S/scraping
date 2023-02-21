import random
import time

GRID_WIDTH = 30
GRID_HEIGHT = 30

class GameOfLife:
    def __init__(self):
        self.createBoard()
        self.drawBoard()
        self.paused = True

    def createBoard(self):
        self.board = [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def drawBoard(self):
        board_str = ""
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.board[row][col]:
                    board_str += "⬜"
                else:
                    board_str += "⬛"
            board_str += "\n"
        print(board_str)

    def countNeighbors(self, row, col):
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
                neighbors = self.countNeighbors(row, col)
                if self.board[row][col] and (neighbors == 2 or neighbors == 3):
                    new_board[row][col] = True
                elif not self.board[row][col] and neighbors == 3:
                    new_board[row][col] = True
        self.board = new_board
        self.drawBoard()
        if not self.paused:
            time.sleep(0.5)
            print("==============================================")
            self.update()

    def start(self):
        self.paused = False
        self.update()

    def clear(self):
        self.board = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.drawBoard()

    def regenerate(self):
        self.createBoard()
        self.drawBoard()

def main():
    game = GameOfLife()
    while True:
        try:
            print("\n\n\n")
            print("Jeu de la vie")
            print("Commande:")
            print("start - commence le jeu")
            print("clear - vide le tableau")
            print("regenerate - genere un nouveau tableau")
            print("quit - quitte le jeu")

            command = input("> ")
            if command == "start":
                game.start()
            elif command == "clear":
                game.clear()
            elif command == "regenerate":
                game.regenerate()
            elif command == "quit":
                break
            else:
                print("Invalid command")
        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    main()