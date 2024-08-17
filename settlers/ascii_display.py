"""A module for displaying the Settlers game-state in ASCII"""

class BoardDisplay:

    def __init__(self, hex_side_length):
        self.hex_side_length = hex_side_length
        self.hex_horizontal = self.hex_side_length * 3
        self.board = self.initialize_board()

    def set_hex_side_length(self, length):
        self.hex_side_length = length
        self.hex_horizontal = self.hex_side_length * 3
        self.board = self.initialize_board()

    def initialize_board(self):
        board = []

        # Board Dimensions
        board_width = (self.hex_horizontal * 7) + 12 + (self.hex_side_length * 4)
        middle_height = (self.hex_side_length * 6) + 7
        triangle_height = 0

        # Initialize Ring
        closed = False
        i = 3
        while not closed:
            inner_offset = board_width - (i * 2) - 2
            board.insert(0, list((i * ' ') + '/' + (inner_offset * ' ') + '\\' + (i * ' ') + '\n'))
            board.append(list((i * ' ') + '\\' + (inner_offset * ' ') + '/' + (i * ' ') + '\n'))
            if inner_offset < 6:
                closed = True
            i += 3
            triangle_height += 1

        for i in range(middle_height):
            board.insert(i + triangle_height, list('|' + ((board_width - 2) * ' ') + '|\n'))

        # Initalize Hexes
        indice_increment = 0
        for i in range(6):

            chars = tuple('*' + ('/' * self.hex_side_length) + '*' + ('\\' * self.hex_side_length) + '*')
            index = 0
            angle_offset = 0

            for j in range(triangle_height + (indice_increment * -1), (triangle_height + middle_height) + indice_increment):
                if index >= len(chars) - 1:
                    index = 0
                if i < 3:
                    string_offset = 1 + self.hex_horizontal + (i * (2 + self.hex_horizontal + self.hex_side_length)) + angle_offset
                    board[j][string_offset] = chars[index]
                    if index == 0:
                        for k in range(1, self.hex_horizontal + 1):
                            board[j][string_offset + k] = '-'
                else:
                    string_offset = (self.hex_horizontal - self.hex_side_length) + (i * (2 + self.hex_horizontal + self.hex_side_length)) - angle_offset
                    board[j][string_offset] = chars[len(chars) - 1 - index]
                    if index == (self.hex_side_length + 1) and i < 5:
                        for k in range(1, self.hex_horizontal + 1):
                            board[j][string_offset + k] = '-'

                index += 1
                if index < len(chars) / 2:
                    angle_offset -= 1
                else:
                    angle_offset += 1

            if i < 2:
                indice_increment += self.hex_side_length + 1
            elif i == 2:
                pass
            else:
                indice_increment -= self.hex_side_length + 1

        return board
    

    def __str__(self):
        board = ''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                board += self.board[i][j]
        return board
    
        



# Build road
# Build settlement
# Build City
# Add Player
# Add Resource Card(Player)
# Add Devlopment Card(Player)
# Change Intersection
# Change Road
# Robber
# Display Tile Letters
# Display Dice(Number)
