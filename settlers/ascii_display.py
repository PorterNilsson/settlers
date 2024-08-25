"""A module for displaying the Settlers game-state in ASCII"""

class BoardDisplay:

    COLORS = {
        "RED": "255;0;0",
        "ORANGE": "255;128;0",
        "YELLOW": "255;255;0",
        "GREEN": "0;255;0",
        "BLUE": "0;0;255",
        "PURPLE": "127;0;255", 
        "WHITE": ""
        }
    INTERSECTION_TYPES = ("*", "s", "C")

    def __init__(self, size, schema=tuple(range(19))):
        # Size maps to the diagonal length of any individual hex.
        self.diagonal_len = BoardDisplay._validate_size(size)
        # Horizontal length in characters is longer as each monospaced character is smaller in width than height.
        self.horizontal_len = self.diagonal_len * 3

        # The board is a 2d array for ease of manipulation until the users requests it; then it is returned as a string.
        self.board = []
        # Number of newlines composing the upper triangular part of the board (and implicitly the lower).
        self.top_height = 0
        # Number of newlines composing the middle portion of the board.
        self.middle_height = 0
        self._initialize_border()

        # Board characteristics to determine row, col locations of all hexes and their intersections (offsets) relative to board size.
        self.hex_schema = BoardDisplay._validate_schema(schema)
        self.hex_origin = self._get_hex_origin()
        self.hex_locations = self._get_hex_locations()
        print(self.hex_locations)
        self.hex_offsets = self._get_hex_offsets()
        self._initialize_intersections()
        self._initialize_roads()
    

    def set_intersection(self, hex, offset, color, intersection_type):
        if color not in BoardDisplay.COLORS.keys():
            print("Not a valid color. Must be 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', or 'WHITE'.")
            return
        if intersection_type not in BoardDisplay.INTERSECTION_TYPES:
            print("Not a valid building type. Must be '*' for default, 's' for 'settlement', or 'C' for 'City'.")
            return
        
        row, col = self._get_location(hex, offset)
        if color == "WHITE":
            self.board[row][col] = intersection_type
        else:
            self.board[row][col] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{intersection_type}\x1b[0m"


    def set_road(self, hex, offset, color):
        next_offset = offset + 1
        if next_offset == 6:
            next_offset = 0
        
        start = list(self._get_location(hex, offset))
        end = list(self._get_location(hex, next_offset))

        char = ""
        row_increment = 0
        col_increment = 0

        row_diff = start[0] - end[0]
        col_diff = start[1] - end[1]
        # 6 conditions
        if row_diff == 0 and col_diff < 0:
            char = "-"
            col_increment = 1
        elif row_diff < 0 and col_diff < 0:
            char = "\\"
            row_increment = 1
            col_increment = 1
        elif row_diff < 0 and col_diff > 0:
            char = "/"
            row_increment = 1
            col_increment = -1
        elif row_diff == 0 and col_diff > 0:
            char = "-"
            col_increment = -1
        elif row_diff > 0 and col_diff > 0:
            char = "\\"
            row_increment = -1
            col_increment= -1
        else:
            char = "/"
            row_increment = -1
            col_increment = 1

        start[0] += row_increment
        start[1] += col_increment
        while start != end:
            if color == "WHITE":
                self.board[start[0]][start[1]] = char
            else:
                self.board[start[0]][start[1]] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{char}\x1b[0m"
            start[0] += row_increment
            start[1] += col_increment


    @staticmethod
    def _validate_size(size):
        default_size = 3
        if size < 1 or size > 8:
            print(f"Invalid board size selected. Defaulting to {default_size}.")
        else:
            return size

    
    def _initialize_border(self):

        # Board Dimensions
        # "7" comes from the length of 5 hexes across the board plus a buffer of the same length on either side.
        # "12" is the number of extra characters (borders, intersections) that add to the width.
        # "4" is the width added by the diagonal 'rising and falling' hex edges.
        board_width = (self.horizontal_len * 7) + 12 + (self.diagonal_len * 4)

        # The middle is 3 hexes tall with 2 diagonal sections each. 2 * 3 = '6' in the calculation
        # "7" is the number of extra characters (intersections) contributing to the middle width of the board.
        middle_height = (self.diagonal_len * 6) + 7

        # Initialize Border

        # "closed" refers to the upper and lower triangular portions of the board which "close." 
        # The space between the left and right side decreases for each iteration
        closed = False
        i = 3
        while not closed:
            # "-2" is to account for the border characters ("/" and "\") themselves.
            inner_offset = board_width - (i * 2) - 2
            self.board.insert(0, list((i * " ") + "/" + (inner_offset * " ") + "\\" + (i * " ") + "\n"))
            self.board.append(list((i * " ") + "\\" + (inner_offset * " ") + "/" + (i * " ") + "\n"))
            # 
            if inner_offset < 6:
                closed = True
            i += 3
            self.top_height += 1

        if (inner_offset) == 5:
            self.board.insert(0, list((i * " ") + '^' + (i * " ") + "\n"))
            self.board.append(list((i * " ") + "v" + (i * " ")))
            self.top_height += 1

        for i in range(middle_height):
            self.board.insert(i + self.top_height, list("|" + ((board_width - 2) * " ") + "|\n"))
    
    @staticmethod
    def _validate_schema(schema):
        default_schema = range(19)
        if len(schema) != 19:
            print("Invalid schema length. Must be length 19 to account for each hex")
            return default_schema
        elif set(schema) != set(default_schema):
            print("Invalid schema. Must contain all numbers 0-18 inclusive.")
            return default_schema
        elif type(schema) != tuple:
            print("Invalid schema type. Must be a Tuple.")
            return default_schema
        else:
            return schema


    def _get_hex_origin(self):
        # Finds indices of the top-middle hex's top-left intersection.
        row = self.top_height - (2 * self.diagonal_len) - 2
        col = (self.horizontal_len * 3) + (self.diagonal_len * 2) + 5
        return (row, col)


    def _get_hex_locations(self):
        hex_arrangement = (
            (0,),
            (-1, 1),
            (-2, 0, 2),
            (-1, 1),
            (-2, 0, 2),
            (-1, 1),
            (-2, 0, 2),
            (-1, 1),
            (0,)
        )

        default_schema_locations = []
        for i in range(len(hex_arrangement)):
            for j in range(len(hex_arrangement[i])):
                row = self.hex_origin[0] + (i * (self.diagonal_len + 1))
                col = self.hex_origin[1] + (hex_arrangement[i][j] * (self.diagonal_len + self.horizontal_len + 2))
                default_schema_locations.append((row, col))

        new_schema_locations = []
        for i in range(len(default_schema_locations)):
            new_schema_locations.insert(self.hex_schema[i], default_schema_locations[self.hex_schema[i]])

        return tuple(new_schema_locations)


    def _get_hex_offsets(self):
        return (
            (0, 0),
            (0, self.horizontal_len + 1),
            (self.diagonal_len + 1, self.horizontal_len + self.diagonal_len + 2),
            (2 * self.diagonal_len + 2, self.horizontal_len + 1),
            (2 * self.diagonal_len + 2, 0),
            (self.diagonal_len + 1, -(self.diagonal_len + 1))
        )


    def _initialize_intersections(self):
        # "19" is the total number of hexes
        for i in range(19):
            # "6" is the total number of intersections for any given hex
            for j in range(6):
                self.set_intersection(i, j, "WHITE", "*")


    def _initialize_roads(self):
        for i in range(19):
            for j in range(6):
                self.set_road(i, j, "WHITE")
    

    def _get_location(self, hex, offset):

        row = self.hex_locations[hex][0] + self.hex_offsets[offset][0]
        col = self.hex_locations[hex][1] + self.hex_offsets[offset][1]

        return row, col


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
