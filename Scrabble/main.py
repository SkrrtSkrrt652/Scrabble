import scrabble

def string_to_rack(string):
    rack = []
    for c in string:
        rack.append(c.upper())
    return rack



game = scrabble.Scrabble(rack=string_to_rack("TBRDKPC"))
game.load_board("bordz/HERBZ.txt")
game.solve()
print("Highest scoring move: ", game.get_best_move())
print("Longest move: ", game.get_longest_move())
print("Success!")
