"""A module for displaying the Settlers game-state in ASCII"""

class BoardDisplay:

    BOARD_HEIGHT = 39
    BOARD_WIDTH = 63

    def __init__(self):
        self.board = [[' ' for _ in range(BoardDisplay.BOARD_WIDTH)] for _ in range(BoardDisplay.BOARD_HEIGHT)]
        self._init_board()

    
    def _init_board(self):
        self._init_border()
        self._init_intersections()
        self._init_roads()
        self._init_ports()
        self._init_ocean()
        self._init_hexes()
        self._init_robber()

        
    @staticmethod
    def _color_character(color, char):
        return f"\x1b[38;2;{color}m{char}\x1b[0m"
    

    @staticmethod
    def _color_background(color, char=""):
        return f"\x1b[48;2;{color}m{char}\x1b[0m"


    def __str__(self):
        board = ''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                board += self.board[i][j]
        return board


    # Helper Methods
    
    def _init_border(self):

        for row in range(BoardDisplay.BOARD_HEIGHT):
            self.board[row][BoardDisplay.BOARD_WIDTH - 1] = "\n"

        col = 3
        for row in range(9, -1, -1):
            self.board[row][col] = "/"
            self.board[row][BoardDisplay.BOARD_WIDTH - col - 2] = "\\"
            self.board[BoardDisplay.BOARD_HEIGHT - row - 1][col] = "\\"
            self.board[BoardDisplay.BOARD_HEIGHT - row - 1][BoardDisplay.BOARD_WIDTH - col - 2] = "/"

            self.board[10 + row][0] = "|"
            self.board[10 + row][BoardDisplay.BOARD_WIDTH - 2] = "|"
            self.board[BoardDisplay.BOARD_HEIGHT - 11 - row][0] = "|"
            self.board[BoardDisplay.BOARD_HEIGHT - 11 - row][BoardDisplay.BOARD_WIDTH - 2] = "|"

            col += 3


    def _init_intersections(self):
        pass


    def _init_roads(self):
        pass


    def _init_ports(self):
        pass


    def _init_ocean(self):
        pass

    
    def _init_hexes(self):
        pass


    def _init_robber(self):
        pass
    
