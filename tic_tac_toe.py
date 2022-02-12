from tkinter import Canvas, Tk

# Constants
CANVAS_SIZE = 600
INFO_SIZE = CANVAS_SIZE // 10
FIGURE_SIZE = 200
RATIO = CANVAS_SIZE // FIGURE_SIZE
BG_COLOR = 'black'
EMPTY = None

# Players setup
X = 'player 1'
O = 'player 2'
FIRST_PLAYER = X


class Board(Tk):
    def __init__(self, ai_mode, start_player=FIRST_PLAYER):
        super().__init__()
        self.title('Tic Tac Toe')
        self.info = Canvas(height=INFO_SIZE, width=CANVAS_SIZE, bg='white')
        self.info.pack()
        self.prev_info = None
        self.canvas = Canvas(height=CANVAS_SIZE, width=CANVAS_SIZE, bg=BG_COLOR)
        self.canvas.pack()
        self.figure_size = FIGURE_SIZE
        self.current_player = start_player
        self.canvas.bind('<Button-1>', self.click_event)
        self.game_status = True
        self.ai_mode = ai_mode
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
            
        #current player shows in reverse
        self.display_current_player('O')

    def __str__(self):
        return f'Tic tac toe game class'

    def build_grid(self, grid_color):
        """This method require to be executed after initialize object
        Create separating lines on field (3x3)
            __|__|__
            __|__|__
              |  |
        """
        x = CANVAS_SIZE // RATIO
        y1 = 0
        y2 = CANVAS_SIZE
        for _ in range(2):
            self.canvas.create_line(x, y1, x, y2, fill=grid_color)
            self.canvas.create_line(y1, x, y2, x, fill=grid_color)
            x += CANVAS_SIZE // RATIO

    def render_cross(self, posX, posY):
        """Render X on field"""
        f_size = self.figure_size
        self.canvas.create_line(posX, posY, posX + f_size, posY + f_size, fill='red', width=5)
        self.canvas.create_line(posX + f_size, posY, posX, posY + f_size, fill='red', width=5)

    def render_circle(self, posX, posY):
        """Magic number: 5, its a gap between edges and figure
        Render O on field"""
        f_size = self.figure_size - 5
        self.canvas.create_oval(posX + 5, posY + 5, posX + f_size, posY + f_size, outline='blue', width=5)

    def click_event(self, event):
        """Get coordinates of the click, and prccess player/ai move"""
        #player move
        x_coord = event.x // FIGURE_SIZE if event.x // FIGURE_SIZE < 2 else 2
        y_coord = event.y // FIGURE_SIZE if event.y // FIGURE_SIZE < 2 else 2
        self.make_move(x_coord, y_coord)

        #ai move
        if self.game_status and self.ai_mode:
            self.ai_best_move()

    def make_move(self, x, y):
        """Handle all logic in a game
        1) Get coordinates of the click event (x_coord, y_coord)
        2) Update field and change current player
        3) Render X or O on field, depends on current_player and position of click"""
        #TODO make position more flexible for larger game field
        position = {0: 0, 1: 200, 2: 400}
        current_player = self.current_player
        self.display_current_player(current_player)

        if self.board[x][y] == EMPTY:
            if current_player == X:
                self.render_cross(position[x], position[y])
            elif current_player == O:
                self.render_circle(position[x], position[y])

            self.update_board(x, y)
            self.change_player()

    def display_current_player(self, current_player):
        """display who is current player"""
        center = CANVAS_SIZE // 2
        text = 'Current player - O' if current_player == 'player 1' else 'Current player - X'
        if not self.prev_info:
            self.prev_info = self.info.create_text(center, INFO_SIZE // 2, text=text, fill='black', font='Arial 40')
        else:
            self.info.delete(self.prev_info)
            self.prev_info = self.info.create_text(center, INFO_SIZE // 2, text=text, fill='black', font='Arial 40')

    def ai_best_move(self):
        """Uses minimax algorithm to figure out best move
        move[0] Y position
        move[1] X position
        """
        best_score = float('-inf')
        board_len = range(len(self.board))
        board = self.board[:]
        for i in board_len:
            for j in board_len:
                if board[i][j] == EMPTY:
                    board[i][j] = O
                    score = self.minimax(board, False)
                    board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        move = i, j

        self.make_move(move[0], move[1])

    def minimax(self, board, isMax):
        """Minimax https://en.wikipedia.org/wiki/Minimax"""
        board_len = range(len(self.board))

        if self.check_win(board, O):
            return 1
        elif self.check_win(board, X):
            return -1
        elif self.check_draw(board):
            return 0

        if isMax:
            best_score = float('-inf')
            for i in board_len:
                for j in board_len:
                    if board[i][j] == EMPTY:
                        board[i][j] = O
                        score = self.minimax(board, False)
                        board[i][j] = EMPTY
                        best_score = max(score, best_score)
        else:
            best_score = float('inf')
            for i in board_len:
                for j in board_len:
                    if board[i][j] == EMPTY:
                        board[i][j] = X
                        score = self.minimax(board, True)
                        board[i][j] = EMPTY
                        best_score = min(score, best_score)
        return best_score

    def change_player(self):
        """Changes current player"""
        if self.current_player == X:
            self.current_player = O
        else:
            self.current_player = X

    def update_board(self, x, y):
        """Place mark of current player on board
        __|__|__
        __|X_|__
          |  |O
        """
        c_player = self.current_player
        self.board[x][y] = c_player
        if self.check_win(self.board, c_player):
            self.draw_winner_line(self.board, c_player)
            self.winner(c_player)
        elif self.check_draw(self.board):
            self.winner()
    
    def draw_winner_line(self, board, player):
        """Drawing winning line on field"""
        position = {0: 0 + self.figure_size // 2, 1: 200 + self.figure_size // 2, 2: 400 + self.figure_size // 2}
        for i in range(3):
            if board[i] == [player, player, player]:
                self.canvas.create_line(position[i], 0, position[i], CANVAS_SIZE, fill='orange', width=15)
        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] == player:
                self.canvas.create_line(0, position[j], CANVAS_SIZE, position[j], fill='orange', width=15)
        if board[0][0] == board[1][1] == board[2][2] == player:
            self.canvas.create_line(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill='orange', width=15)
        elif board[0][2] == board[1][1] == board[2][0] == player:
            self.canvas.create_line(CANVAS_SIZE, 0, 0, CANVAS_SIZE, fill='orange', width=15)

    def check_win(self, board, player):
        """Checks player win conditions
        Output: True if 'player' win on particular 'board', False otherwise"""
        status = False
        for i in range(3):
            if board[i] == [player, player, player] \
                or board[0][i] == board[1][i] == board[2][i] == player:
                status = True
                break
        if board[0][0] == board[1][1] == board[2][2] == player:
            status = True
        elif board[0][2] == board[1][1] == board[2][0] == player:
            status = True
        return status        

    def check_draw(self, board):
        """Checks draw condition
        Output: True if draw, False otherwise"""
        for row in board:
            if EMPTY in row:
                return False
        return True

    def winner(self, player=None):
        """Display end game text, depends on player attribute
        and shutdown the game"""
        self.game_status = False
        center = CANVAS_SIZE // 2
        if player:
            text = f'''Winner: {'X' if player == FIRST_PLAYER else 'O'}
click on screen
to play more'''
        else:
            text = '''Draw
click on screen
to play more'''
        self.info.delete(self.prev_info)
        self.canvas.create_text(center, center, text=text, fill='white', font='Arial 40')
        self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', self.end_game)

    def end_game(self, event):
        """Executes end game routine
        possible options: start new game or end current game"""
        from __main__ import game
        self.destroy()
        game.run_selector()