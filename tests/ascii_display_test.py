from settlers.display import board_display

def test_display_board():
    assert board_display.display_board() == 'ASCII Board'
    