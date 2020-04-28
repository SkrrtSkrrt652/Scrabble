import scrabble

game = scrabble.Scrabble(rack=['A', 'Z', 'S', 'C', 'R', 'D', 'N'])
game.load_board("boarsample.txt")
best_move = game.get_best_move()


print("Success!")
