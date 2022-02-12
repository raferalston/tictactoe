from tkinter import Label, Tk, Button
import tic_tac_toe

class GameSelector(Tk):
    def __init__(self):
        super().__init__()
        self.title('Tic Tac Toe')
        title = Label(self, text='Welcome to the tictactoe game!', font='Arial 40')
        title.grid(row=0, column=1, sticky="we")
        human_selector = Button(self, text='vs Human', padx=40, pady=20, fg='#faee1c', bg='#f3558e', font='fantasy 40', command=lambda: self.mode_select('human'))
        human_selector.grid(row=1, column=1, sticky="we")
        ai_selector = Button(self, text='vs AI', padx=40, pady=20, fg='#faee1c', bg='#581b98', font='fantasy 40', command=lambda: self.mode_select('ai'))
        ai_selector.grid(row=2, column=1, sticky="we")

    def __str__(self):
        return 'Game selection class'

    def mode_select(self, t):
        """Select game mode: vs AI or vs Human
        """
        self.destroy()
        AI_MODE = False
        if t == 'ai':
            AI_MODE = True
        self.run_game(AI_MODE)
        
    def run_game(self, ai_mode):
        """Initialize game object and execute require methods
        and run the game"""
        game_v1 = tic_tac_toe.Board(ai_mode=ai_mode)
        game_v1.build_grid('white')
        game_v1.mainloop()