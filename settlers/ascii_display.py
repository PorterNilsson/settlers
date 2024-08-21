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
    HEX_ARRANGEMENT = (
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


    def __init__(self, size):
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
        # Updates "self.board", "self.top_height", and "self.middle_height"
        self._initialize_border()

        # Array indices for the upper-left intersection of the first hex
        self.hex_origin = self._get_hex_origin()
        self.hex_offsets = self._get_hex_offsets()
        self._initialize_intersections()
    

    def set_intersection(self, hex, offset, color, intersection):
        if color not in BoardDisplay.COLORS.keys():
            print("Not a valid color. Must be 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', or 'WHITE'.")
            return
        if intersection not in BoardDisplay.INTERSECTION_TYPES:
            print("Not a valid building type. Must be '*' for default, 's' for 'settlement', or 'C' for 'City'.")
            return
        
        row, col = self._get_location(hex, offset)
        # print(f"Hex: {hex}, Offset: {offset}, Row: {row}, Col: {col}")
        if color == "WHITE":
            self.board[row][col] = intersection
        else:
            self.board[row][col] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{intersection}\x1b[0m"


    # def set_road(self, color, hex, offset):
    #     if color not in BoardDisplay.COLORS.keys():
    #         print("Not a valid color. Must be 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'PURPLE', or 'WHITE'.")
    #         return
        
    #     length = len(BoardDisplay.RELATIVE_HEX_LOCATIONS) - 1
    #     if ((hex > length) 
    #             or hex < (-1 * length) 
    #             or not isinstance(hex, int)):
    #         print(f"Not a valid intersection. Must be an integer in range [-{length - 1}, {length}], inclusive.")
    #         return
        
    #     length = len(BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS) - 1
    #     if (offset > length
    #             or offset < (-1 * length) 
    #             or not isinstance(offset, int)):
    #         print(f"Not a valid offset. Must be an integer in range [-{length - 1}, {length}] inclusive.")
    #         return
        
    #     hex = BoardDisplay.RELATIVE_HEX_LOCATIONS[hex]
    #     row = hex[0].split(',')
    #     col = hex[1].split(',')
    #     row = self._intersection_relative_location_calc(*row)
    #     col = self._intersection_relative_location_calc(*col)

    #     num = offset
        
    #     offset = BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS[offset]
    #     row_offset = offset[0].split(',')
    #     col_offset = offset[1].split(',')
    #     row += self._intersection_relative_location_calc(*row_offset)
    #     col += self._intersection_relative_location_calc(*col_offset)

    #     d = self.diagonal_len
    #     h = self.horizontal_len
    #     direction_vectors = [
    #         [0, h], [d, d], [d, -d], [0, -h], [-d, -d], [-d, d]
    #     ]
    #     road_types = ("-", "\\", "/", "-", "\\", "/")

    #     v = direction_vectors[num]
    #     while v != [0, 0]:
    #         if color == "WHITE":
    #             self.board[self.hex_origin[0] + row + v[0]][self.hex_origin[1] + col + v[1]] = road_types[num]
    #         else:
    #             self.board[self.hex_origin[0] + row + v[0]][self.hex_origin[1] + col + v[1]] = f"\x1b[38;2;{BoardDisplay.COLORS.get(color)}m{road_types[num]}\x1b[0m"
        
    #         if v[0] > 0:
    #             v[0] -= 1
    #         if v[1] > 0:
    #             v[1] -= 1
    #         if v[0] < 0:
    #             v[0] += 1
    #         if v[1] < 0:
    #             v[1] += 1

    #     return


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

        # # Set Hex Origin (Must be done before set_intersection  is called)
        # self.hex_origin = self._get_hex_origin()

        # # Initialize Intersections and Roads
        # for location in range(len(BoardDisplay.RELATIVE_HEX_LOCATIONS)):
        #     for intersection in range(len(BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS)):
        #         self.set_intersection("WHITE", "*", location, intersection)
        #         self.set_road("WHITE", location, intersection)

        # # Initialize Ports
        # for port in BoardDisplay.RELATIVE_PORT_LOCATIONS_AND_ROTATIONS:

        #     hex = BoardDisplay.RELATIVE_HEX_LOCATIONS[port[0]]
        #     row = hex[0].split(',')
        #     col = hex[1].split(',')
        #     row = self._intersection_relative_location_calc(*row)
        #     col = self._intersection_relative_location_calc(*col)

        #     offset = BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS[port[1]]
        #     row_offset = offset[0].split(',')
        #     col_offset = offset[1].split(',')
        #     row_one = self._intersection_relative_location_calc(*row_offset) + row
        #     col_one = self._intersection_relative_location_calc(*col_offset) + col

        #     offset = BoardDisplay.RELATIVE_INTERSECTION_LOCATIONS[port[1] + 1]
        #     row_offset = offset[0].split(',')
        #     col_offset = offset[1].split(',')
        #     row_two = self._intersection_relative_location_calc(*row_offset) + row
        #     col_two = self._intersection_relative_location_calc(*col_offset) + col
            
        #     # Filtering for beginning on a straightedge
        #     row, col = self._draw_port_from_offset(row_one, col_one, port[2])

        
        # return self.board
    

    def _get_hex_origin(self):
        # Finds indices of the top-middle hex's top-left intersection.
        row = self.top_height - (2 * self.diagonal_len) - 2
        col = (self.horizontal_len * 3) + (self.diagonal_len * 2) + 5
        return (row, col)


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


    def _get_location(self, hex, offset):
        row = 0
        col = 0
        for i in range(len(BoardDisplay.HEX_ARRANGEMENT)):
            for j in range(len(BoardDisplay.HEX_ARRANGEMENT[i])):
                if hex == 0:
                    row = self.hex_origin[0] + (i * (self.diagonal_len + 1))
                    col = self.hex_origin[1] + (BoardDisplay.HEX_ARRANGEMENT[i][j] * (self.diagonal_len + self.horizontal_len + 2))
                hex -= 1

        row += self.hex_offsets[offset][0]
        col += self.hex_offsets[offset][1]

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
