import scrabble

def string_to_rack(string):
    rack = []
    for c in string:
        rack.append(c.upper())
    return rack



game = scrabble.Scrabble(rack=string_to_rack("eolsebr"), dictfile="collins2019.txt")
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
base_rack = "NIHTNQ"
game.load_board("bordz/TREMZ.txt")


game.solve()
print("Highest scoring move: ", game.get_best_move())
print("Longest move: ", game.get_longest_move())
#print("Opponents rack: ", game.get_opponent_rack_prob_dist())

print("Success!")
