"""A module for displaying the Settlers game-state in ASCII"""

class BoardDisplay:

    MAX_INTERSECTION = 53
    COLORS = {
        "RED": "255;0;0",
        "ORANGE": "255:128;0",
        "YELLOW": "255;255;0",
        "GREEN": "0;255;0",
        "BLUE": "0;0;255",
        "PURPLE": "127;0;255", 
        "WHITE": "255; 255; 255"
        }
    INTERSECTION_TYPES = ("*", "s", "C")
    RELATIVE_LOCATIONS = (
        ("0", "0"), ("1d", "1d"), ("2d", "0"), ("2d", "-1h"), ("1d", "-1d,-1h"), ("0", "-1h"),

        ("-2d", "0"), ("-1d", "1d"), ("-1d", "1d,1h"), ("0", "2d,1h"), ("1d", "1d,1h"), ("2d", "2d,1h"),
        ("3d", "1d,1h"), ("3d", "1d"), ("4d", "0"), ("4d", "-1h"), ("3d", "-1d,-1h"), ("3d", "-1d,-2h"),
        ("2d", "-2d,-2h"), ("1d", "-1d,-2h"), ("0", "-2d,-2h"), ("-1d", "-1d,-2h"), ("-1d", "-1d,-1h"), ("-2d", "-1h"),

        ("-4d", "0"), ("-3d", "1d"), ("-3d", "1d,1h"), ("-2d", "2d,1h"), ("-2d", "2d,2h"), ("-1d", "3d,2h"),
        ("0", "2d,2h"), ("1d", "3d,2h"), ("2d", "2d,2h"), ("3d", "3d,2h"), ("4d", "2d,2h"), ("4d", "2d,1h"),
        ("5d", "1d,1h"), ("5d", "1d"), ("6d", "0"), ("6d", "-1h"), ("5d", "-1d,-1h"), ("5d", "-1d,-2h"),
        ("4d", "-2d,-2h"), ("4d", "-2d,-3h"), ("3d", "-3d,-3h"), ("2d", "-2d,-3h"), ("1d", "-3d,-3h"), ("0", "-2d,-3h"),
        ("-1d", "-3d,-3h"), ("-2d", "-2d,-3h"), ("-2d", "-2d,-2h"), ("-3d", "-1d,-2h"), ("-3d", "-1d,-1h"), ("-4d", "-1h")
        )


    def __init__(self):
        self.hex_diagonal_length = 2
        self.hex_horizontal = self.hex_diagonal_length * 3
        self.hex_origin = (0, 0)

        self.board = []
        self.board = self._initialize_border()

    
    def set_intersection(self, color, intersect_type, location):
        if color not in BoardDisplay.COLORS.keys():
            print("Not a valid color. Must be 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', or 'WHITE'.")
            return
        if intersect_type not in BoardDisplay.INTERSECTION_TYPES:
            print("Not a valid building type. Must be '*' for default, 's' for 'settlement', or 'C' for 'City'.")
            return
        if location > BoardDisplay.MAX_INTERSECTION or location < 0 or not isinstance(location, int):
            print("Not a valid intersection location. Must be an integer in range [0, 53], inclusive.")
            return
        
        location = BoardDisplay.RELATIVE_LOCATIONS[location]
        row = location[0].split(',')
        col = location[1].split(',')
        row = self._intersection_relative_location_calc(*row)
        col = self._intersection_relative_location_calc(*col)

        self.board[self.hex_origin[0] + row][self.hex_origin[1] + col] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{intersect_type}\x1b[0m"
        return
    

    def set_road(self, color, location, sublocation=0):
        if color not in BoardDisplay.COLORS.keys():
            print("Not a valid color. Must be 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', or 'WHITE'.")
            return
        if location > BoardDisplay.MAX_INTERSECTION or location < 0 or not isinstance(location, int):
            print("Not a valid intersection location. Must be an integer in range [0, 53], inclusive.")
            return
        if location % 2 == 1 and sublocation != 0:
            print("Not a valid sublocation.")
            return
        if location % 2 == 0 and (sublocation > 1 or sublocation < 0):
            print("Not a valid sublocation.")
            return
        
        num = location
        location = BoardDisplay.RELATIVE_LOCATIONS[location]
        row = location[0].split(',')
        col = location[1].split(',')
        row = self._intersection_relative_location_calc(*row)
        col = self._intersection_relative_location_calc(*col)

        intersect_type = '-'
        if num % 2 == 0:
            for i in range(1, self.hex_diagonal_length + 1):
                if sublocation == 1:
                    intersect_type = "/"
                    self.board[self.hex_origin[0] + row - i][self.hex_origin[1] + col + i] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{intersect_type}\x1b[0m"
                else:
                    intersect_type = "\\"
                    self.board[self.hex_origin[0] + row + i][self.hex_origin[1] + col + i] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{intersect_type}\x1b[0m"
        else:
            for i in range(1, self.hex_horizontal + 1):
                self.board[self.hex_origin[0] + row + i][self.hex_origin[1] + col + i] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{intersect_type}\x1b[0m"

        
    def _initialize_border(self):

        # Board Dimensions
        board_width = (self.hex_horizontal * 7) + 12 + (self.hex_diagonal_length * 4)
        middle_height = (self.hex_diagonal_length * 6) + 7
        triangle_lines = 0

        # Initialize Border
        closed = False
        i = 3
        while not closed:
            inner_offset = board_width - (i * 2) - 2
            self.board.insert(0, list((i * ' ') + '/' + (inner_offset * ' ') + '\\' + (i * ' ') + '\n'))
            self.board.append(list((i * ' ') + '\\' + (inner_offset * ' ') + '/' + (i * ' ') + '\n'))
            if inner_offset < 6:
                closed = True
            i += 3
            triangle_lines += 1

        for i in range(middle_height):
            self.board.insert(i + triangle_lines, list('|' + ((board_width - 2) * ' ') + '|\n'))

        # Set Hex Origin
        self.hex_origin = self._get_hex_origin()

        # Initialize Intersections
        for location in range(len(BoardDisplay.RELATIVE_LOCATIONS)):
            self.set_intersection("WHITE", "*", location)

        return self.board
    

    def _intersection_relative_location_calc(self, *components):
        total = 0
        for component in components:
            if len(component) == 1:
                continue
            elif component[-1] == "d":
                total += int(component[:-1]) * (self.hex_diagonal_length + 1)
            else:
                total += int(component[:-1]) * (self.hex_horizontal + 1)
        return total
    

    def _get_hex_origin(self):
        row = 0
        while self.board[row][0] != "|":
            row += 1
        
        row += 2 + (self.hex_diagonal_length * 2)

        col = (4 * self.hex_horizontal) + 6 + (2 * self.hex_diagonal_length)

        return (row, col)


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
