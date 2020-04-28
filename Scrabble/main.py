import scrabble

def string_to_rack(string):
    rack = []
    for c in string:
        rack.append(c.upper())
    return rack



game = scrabble.Scrabble(rack=string_to_rack("RBNRPRS"))
game.load_board("bordz/SARGZ.txt")
best_move = game.get_best_move()
print(best_move)
print("Success!")
