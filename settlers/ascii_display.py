'''A module for displaying the Settlers game-state in ASCII'''

class Display:

    def __init__(self) -> None:

        self.currently_displayed: bool = False

        self.board_width: int = 82
        self.board_height: int = 50

    def display_board(self) -> None:


        if (self.currently_displayed):
            print('\r' * self.board_height)

        print('                                          / \\                                          ')
        print('                                       /       \\                                       ')
        print('                                    /             \\                                    ')
        print('                                 /                   \\                                 ')
        print('                              /                         \\                              ')
        print('                           /                               \\                           ')
        print('                        /             *---------*             \\                        ')
        print('                     /               /           \\               \\                     ')
        print('                  /                 /             \\                 \\                  ')
        print('               /                   /               \\                   \\               ')
        print('            /           *---------*                 *---------*           \\            ')
        print('         /             /           \\               /           \\             \\         ')
        print('      /               /             \\             /             \\               \\      ')
        print('   /                 /               \\           /               \\                 \\   ')
        print('|         *---------*                 *---------*                 *---------*         |')
        print('|        /           \\               /           \\               /           \\        |')
        print('|       /             \\             /             \\             /             \\       |')
        print('|      /               \\           /               \\           /               \\      |')
        print('|     *                 *---------*                 *---------*                 *     |')
        print('|      \\               /           \\               /           \\               /      |')
        print('|       \\             /             \\             /             \\             /       |')
        print('|        \\           /               \\           /               \\           /        |')
        print('|         *---------*                 *---------*                 *---------*         |')
        print('|        /           \\               /           \\               /           \\        |')
        print('|       /             \\             /             \\             /             \\       |')
        print('|      /               \\           /               \\           /               \\      |')
        print('|     *                 *---------*                 *---------*                 *     |')
        print('|      \\               /           \\               /           \\               /      |')
        print('|       \\             /             \\             /             \\             /       |')
        print('|        \\           /               \\           /               \\           /        |')
        print('|         *---------*                 *---------*                 *---------*         |')
        print('|        /           \\               /           \\               /           \\        |')
        print('|       /             \\             /             \\             /             \\       |')
        print('|      /               \\           /               \\           /               \\      |')
        print('|     *                 *---------*                 *---------*                 *     |')
        print('|      \\               /           \\               /           \\               /      |')
        print('|       \\             /             \\             /             \\             /       |')
        print('|        \\           /               \\           /               \\           /        |')
        print('|         *---------*                 *---------*                 *---------*         |')
        print('   \\                 \\               /           \\               /                 /   ')
        print('      \\               \\             /             \\             /               /      ')
        print('         \\             \\           /               \\           /             /         ')
        print('            \\           *---------*                 *---------*           /            ')
        print('               \\                   \\               /                   /               ')
        print('                  \\                 \\             /                 /                  ')
        print('                     \\               \\           /               /                     ')
        print('                        \\             *---------*             /                        ')
        print('                           \\                               /                           ')
        print('                              \\                         /                              ')
        print('                                 \\                   /                                 ')
        print('                                    \\             /                                    ')
        print('                                       \\       /                                       ')
        print('                                          \\ /                                          ')

        self.currently_displayed = True    

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

def main():
    
    display: Display = Display()

    display.display_board()
    display.display_board()

if __name__ == "__main__":
    main()

