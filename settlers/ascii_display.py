"""A module for displaying the Settlers game-state in ASCII"""

class BoardDisplay:

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
    RELATIVE_HEX_LOCATIONS = (
        ("0", "0"), ("-1d", "1d,1h"), ("-2d", "2d,2h"), ("-1d", "3d,3h"), ("0", "4d,4h"), ("2d", "4d,4h"), 
        ("4d", "4d,4h"), ("5d", "3d,3h"), ("6d", "2d,2h"), ("5d", "1d,1h"), ("4d", "0"), ("2d", "0"),
        ("1d", "1d,1h"), ("0", "2d,2h"), ("1d", "3d,3h"), ("3d", "3d,3h"), ("4d", "2d,2h"), ("3d", "1d,1h"), ("2d", "2d,2h")
        )
    RELATIVE_INTERSECTION_LOCATIONS = (
        ("0", "0"), ("0", "1h"), ("1d", "1d,1h"), ("2d", "1h"), ("2d", "0"), ("1d", "-1d")
    )


    def __init__(self):
        self.hex_diagonal_length = 2
        self.hex_horizontal = self.hex_diagonal_length * 3
        self.hex_origin = (0, 0)

        self.board = []
        self.board = self._initialize_border()

    
    def set_intersection(self, color, intersect_type, hex, offset):
        if color not in BoardDisplay.COLORS.keys():
            print("Not a valid color. Must be 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', or 'WHITE'.")
            return
        if intersect_type not in BoardDisplay.INTERSECTION_TYPES:
            print("Not a valid building type. Must be '*' for default, 's' for 'settlement', or 'C' for 'City'.")
            return
        
        length = len(BoardDisplay.RELATIVE_HEX_LOCATIONS) - 1
        if ((hex > length) 
                or hex < (-1 * length) 
                or not isinstance(hex, int)):
            print(f"Not a valid intersection. Must be an integer in range [-{length - 1}, {length}], inclusive.")
            return
        
        length = len(BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS) - 1
        if (offset > length
                or offset < (-1 * length) 
                or not isinstance(offset, int)):
            print(f"Not a valid offset. Must be an integer in range [-{length - 1}, {length}] inclusive.")
            return
        
        hex = BoardDisplay.RELATIVE_HEX_LOCATIONS[hex]
        row = hex[0].split(',')
        col = hex[1].split(',')
        row = self._intersection_relative_location_calc(*row)
        col = self._intersection_relative_location_calc(*col)

        offset = BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS[offset]
        row_offset = offset[0].split(',')
        col_offset = offset[1].split(',')
        row += self._intersection_relative_location_calc(*row_offset)
        col += self._intersection_relative_location_calc(*col_offset)

        self.board[self.hex_origin[0] + row][self.hex_origin[1] + col] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{intersect_type}\x1b[0m"
        return
    

    def set_road(self, color, hex, offset):
        if color not in BoardDisplay.COLORS.keys():
            print("Not a valid color. Must be 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', or 'WHITE'.")
            return
        
        length = len(BoardDisplay.RELATIVE_HEX_LOCATIONS) - 1
        if ((hex > length) 
                or hex < (-1 * length) 
                or not isinstance(hex, int)):
            print(f"Not a valid intersection. Must be an integer in range [-{length - 1}, {length}], inclusive.")
            return
        
        length = len(BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS) - 1
        if (offset > length
                or offset < (-1 * length) 
                or not isinstance(offset, int)):
            print(f"Not a valid offset. Must be an integer in range [-{length - 1}, {length}] inclusive.")
            return
        
        hex = BoardDisplay.RELATIVE_HEX_LOCATIONS[hex]
        row = hex[0].split(',')
        col = hex[1].split(',')
        row = self._intersection_relative_location_calc(*row)
        col = self._intersection_relative_location_calc(*col)

        num = offset
        
        offset = BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS[offset]
        row_offset = offset[0].split(',')
        col_offset = offset[1].split(',')
        row += self._intersection_relative_location_calc(*row_offset)
        col += self._intersection_relative_location_calc(*col_offset)

        d = self.hex_diagonal_length
        h = self.hex_horizontal
        direction_vectors = [
            [0, h], [d, d], [d, -d], [0, -h], [-d, -d], [-d, d]
        ]
        road_types = ("-", "\\", "/", "-", "\\", "/")

        v = direction_vectors[num]
        while v != [0, 0]:
            self.board[self.hex_origin[0] + row + v[0]][self.hex_origin[1] + col + v[1]] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{road_types[num]}\x1b[0m"
        
            if v[0] > 0:
                v[0] -= 1
            if v[1] > 0:
                v[1] -= 1
            if v[0] < 0:
                v[0] += 1
            if v[1] < 0:
                v[1] += 1

        return

        
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

        # Set Hex Origin (Must be done before set_intersection  is called)
        self.hex_origin = self._get_hex_origin()

        # Initialize Intersections and Roads
        for location in range(len(BoardDisplay.RELATIVE_HEX_LOCATIONS)):
            for intersection in range(len(BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS)):
                self.set_intersection("WHITE", "*", location, intersection)
                self.set_road("WHITE", location, intersection)
        
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
        col = self.hex_horizontal + 1
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
