from math import inf


class Board:
    FIRST_PLAYER_TURN = 'X'
    SECOND_PLAYER_TURN = 'O'
    FREE_SLOT = ' '
    PLAYERS = [FIRST_PLAYER_TURN, SECOND_PLAYER_TURN]

    def __init__(self):
        self.board = [[' ' for j in range(3)]for i in range(3)]

    def __str__(self):
        a, s = "+---+---+---+", ""
        for row in self.board:
            s += a + '\n' + '| ' + \
                row[0] + ' | ' + row[1] + ' | ' + \
                row[2] + ' |' + '\n'
        s += a
        return s

    def player_change(self, item):
        if item == self.FIRST_PLAYER_TURN:
            return self.SECOND_PLAYER_TURN
        else:
            return self.FIRST_PLAYER_TURN

    def clear_board(self):
        for i in range(3):
            for j in range(3):
                self.board = self.FREE_SLOT

    def win_check(self, item):
        for i in range(3):
            rows = col = diag1 = diag2 = 0
            for j in range(3):
                if self.board[i][j] == item:
                    rows += 1
                if self.board[j][i] == item:
                    col += 1
                if self.board[j][j] == item:
                    diag1 += 1
                if self.board[2 - j][i] == item:
                    diag2 += 1
            if rows == 3 or col == 3 or diag1 == 3 or diag2 == 3:
                self.winner = item
                return True
        return False

    def is_tie(self):
        f = self.FREE_SLOT
        for i in range(3):
            if self.board[i][0] == f or self.board[i][1] == f or self.board[i][2] == f:
                return False
        return True


class Player:
    def __init__(self, name, move_item):
        self.name = name
        self.move_item = move_item

    def make_move(self):
        raise NotImplementedError("Method of abstract class")

    def congrats(self):
        print(f"{self.name} won this game!")


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(self, name)
        self.ask_for_item()

    def make_move(self, board):
        x, y = map(int, input(
            "Enter 2 coordinates separated with space").split())
        if board.board[x][y] == " ":
            board.board[x][y] = self.move_item
        else:
            print("U will miss your turn because of bad params")

    def ask_for_item(self):
        item = input("Choose your move item from: X or O   ")
        item = item.upper()
        if item not in ["X", "O"]:
            raise TypeError("You entered wrong params")
        else:
            self.move_item = item


class PcPlayer(Player):
    def __init__(self, name, move_item):
        super().__init__(name, move_item)

    def make_move(self, board):
        def minmax(board, lvl, isMax):
            if board.win_check(self.move_item):
                return 10/lvl
            if board.win_check(board.player_change(self.move_item)):
                return -10/lvl
            elif board.is_tie():
                return 0
            n = 0
            if isMax:
                value = -inf
                for i in range(3):
                    for j in range(3):
                        if n >= 2:
                            break
                        if board.board[i][j] == board.FREE_SLOT:
                            board.board[i][j] = self.move_item
                            value = max(value, minmax(
                                board, lvl + 1, not isMax))
                            n += 1
                            board.board[i][j] = board.FREE_SLOT
                    if n >= 2:
                        break
            else:
                value = inf
                for i in range(3):
                    for j in range(3):
                        if n >= 2:
                            break
                        if board.board[i][j] == board.FREE_SLOT:
                            board.board[i][j] = board.player_change(
                                self.move_item)
                            value = min(value, minmax(
                                board, lvl+1, not isMax))
                            n += 1
                            board.board[i][j] = board.FREE_SLOT
                    if n >= 2:
                        break
            return value

        best = -inf
        n = 0
        for i in range(3):
            for j in range(3):
                if (board.board[i][j] == board.FREE_SLOT):
                    if n >= 2:
                        break
                    board.board[i][j] = self.move_item
                    move = minmax(board, 1, False)
                    n += 1
                    board.board[i][j] = board.FREE_SLOT
                    if move > best:
                        x = i
                        y = j
                        best = move
                if n >= 2:
                    break
        board.board[x][y] = self.move_item


class Game:
    def __init__(self, player1, player2, board):
        self.players = [player1, player2]
        self.field = board

    def start(self):
        current = 0
        while not self.field.is_tie():
            print(self.field)
            self.players[current].make_move(self.field)
            for player in range(2):
                if self.field.win_check(self.players[player].move_item):
                    player = self.players[player]
                    print(self.field)
                    print(f"Player {player} wins!")
                    return
            current = (current + 1) % 2
        print("It`s a draw guys!")


if __name__ == "__main__":
    board = Board()
    player1 = HumanPlayer('1')
    print(player1.move_item)
    item2 = board.player_change(player1.move_item)
    player2 = PcPlayer('2', item2)
    game = Game(player1, player2, board)
    game.start()
