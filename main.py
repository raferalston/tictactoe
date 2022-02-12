from selector import GameSelector

class GameDispatcher:
    def __str__(self):
        return 'Game dispatcher class'

    def run_selector(self):
        """run module for choice game mode"""
        game_start = GameSelector()
        game_start.mainloop()

if __name__ == '__main__':
    game = GameDispatcher()
    game.run_selector()
