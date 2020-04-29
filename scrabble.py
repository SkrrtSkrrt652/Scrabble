'''
A Scrabble game
'''
from lexicon import Lexicon
import copy

class Scrabble():
    def __init__(self, rack):
        '''
        The constructor initializes the following
        Two boards (regular and transposed)
        Two special square dictionaries (regular and transposed)
        Loads the trie into memory

        '''
        # Initialize board, dictionary special spots and points per letter
        self.board = []
        self.board_transp = []
        self.rack = rack[:]
        self.best_move = dict()
        self.best_score = 0
        self.best_word = ""
        self.longest_move = dict()
        self.longest_score = 0
        self.longest_length = 0
        self.longest_word = ""
        self.dictionary = Lexicon("sowpods.txt")
        self.cross_checks = []
        self.cross_checks_transp = []
        print("Loaded dictionary!")
        self.points = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
            'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
            'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
            'Y': 4, 'Z': 10
        }
        
        for i in range(15):
            row = []
            for j in range(15):
                row.append(None)
            self.board.append(row)
        self.board_transp = copy.deepcopy(self.board)

        self.specials = {
            (0, 0): "TW", (0, 7): "TW", (0, 14): "TW",
            (7, 0): "TW", (7, 7): "TW", (7, 14): "TW",
            (14, 0): "TW", (14, 7): "TW", (14, 14): "TW",
            (1, 1): "DW", (2, 2): "DW", (3, 3): "DW", (4, 4): "DW",
            (7, 7): "DW", (10, 10): "DW", (11, 11):"DW", (12, 12): "DW", (13, 13): "DW",
            (1, 13): "DW", (2, 12): "DW", (3, 11): "DW", (4, 10): "DW",
            (10, 4): "DW", (11, 3): "DW", (12, 2): "DW", (13, 1): "DW",
            (0, 3): "DL", (0, 11): "DL", (2, 6): "DL", (2, 8): "DL",
            (3, 0): "DL", (3, 7): "DL", (3, 14): "DL",
            (6, 2): "DL", (6, 6): "DL", (6, 8): "DL", (6, 12): "DL",
            (7, 3): "DL", (7, 11): "DL",
            (14, 3): "DL", (14, 11): "DL", (12, 6): "DL", (12, 8): "DL",
            (11, 0): "DL", (11, 7): "DL", (11, 14): "DL",
            (8, 2): "DL", (8, 6): "DL", (8, 8): "DL", (8, 12): "DL",
            (1, 5): "TL", (1, 9): "TL",
            (5, 1): "TL", (5, 5): "TL", (5, 9): "TL", (5, 13): "TL",
            (13, 5): "TL", (13, 9): "TL",
            (9, 1): "TL", (9, 5): "TL", (9, 9): "TL", (9, 13): "TL",
        }

        self.specials_transp = dict()
        for special_sq in self.specials:
            self.specials_transp[special_sq[::-1]] = self.specials[special_sq]
    

    def load_board(self, filename):
        '''
        Load a certain scrabble state from a file 'filename'
        '''

        with open(filename) as f:
            lc = 0
            for line in f:
                for i in range(len(line)-1):
                    if line[i] != '.':
                        self.board[lc][i] = line[i]
                        self.board_transp[i][lc] = line[i]
                lc += 1
        self.cross_checks = [self.cross_checks_row(i,0) for i in range(15)]
        self.cross_checks_transp = [self.cross_checks_row(i,1) for i in range(15)]
    
    def get_anchors(self, row, transp=0):
        '''
        Get the anchors from a given row.
        row is the index of the row on the board
        returns a list of numbers, where each number is the column of the anchor in the row
        '''
        anchors = set()
        if not transp:
            for i in range(15):
                if (i > 0 and self.board[row][i] is None and self.board[row][i-1] is not None or 
                    i < 14 and self.board[row][i] is None and self.board[row][i+1] is not None or
                    row > 0 and self.board[row][i] is None and self.board[row-1][i] is not None or
                    row < 14 and self.board[row][i] is None and self.board[row+1][i] is not None):
                    anchors.add(i)
        else:
             for i in range(15):
                if (i > 0 and self.board_transp[row][i] is None and self.board_transp[row][i-1] is not None or 
                    i < 14 and self.board_transp[row][i] is None and self.board_transp[row][i+1] is not None or
                    row > 0 and self.board_transp[row][i] is None and self.board_transp[row-1][i] is not None or
                    row < 14 and self.board_transp[row][i] is None and self.board_transp[row+1][i] is not None):
                    anchors.add(i)
        return anchors
    
    def cross_checks_row(self, row, transp):
        '''
        Cross checks  every square in the row and returns a list containing the set of
        playable letters from the rack for each square in the row
        row is the index of the row in the board
        rack is a list of strings representing the rack
        '''
        if transp:
            board = self.board_transp
        else:
            board = self.board
        cross_checks = []
        for i in range(15):
            if board[row][i] is not None:
                cross_checks.append(set())
                continue
            up_count = row-1
            crossed_word = ""
            while up_count >= 0 and board[up_count][i] is not None:
                crossed_word += board[up_count][i]
                up_count -= 1
            crossed_word = crossed_word[::-1]

            place_letter_index = len(crossed_word)
            down_count = row+1
            while down_count < 15 and board[down_count][i] is not None:
                crossed_word += board[down_count][i]
                down_count += 1

            if crossed_word == "":
                cross_checks.append(set(self.rack))
            else:
                valid_letters = set()
                for letter in self.rack:
                    candidate_word = crossed_word[:place_letter_index] + letter + crossed_word[place_letter_index:]
                    if self.dictionary.check(candidate_word):
                        valid_letters.add(letter)
                cross_checks.append(valid_letters)
        return cross_checks
    
    def get_points(self, placement, across=1):
        '''
        Returns the total points acquired after playing a move
        placement is a dictionary mapping coordinate on the board(tuple) to letter played(string)
        across is a boolean to denote whether the move was played across or not
        Function does not check for legality of the move
        '''
        points = 0
        row = None
        # If the word is played across, no transposition needed
        if across:
            board = self.board
            specials = self.specials
            corrected_placement = placement
        # If played down use transposed board, specials and placement coordinates
        else:
            board = self.board_transp
            specials = self.specials_transp
            # Transpose placement coordinates as well
            corrected_placement = dict()
            for place in placement:
                corrected_placement[place[::-1]] = placement[place]

        # Score all the vertical words first
        for place in corrected_placement:
            letter_played = corrected_placement[place]
            word_points = 0
            row = place[0] #inefficient, row needs to be taken only once
            column = place[1]
            # Check upwards for part of vertical word
            up_count = row-1
            while up_count > 0 and board[up_count][column] is not None:
                word_points += self.points[board[up_count][column]]
                up_count -= 1
            # Check downwards for part of vertical word
            down_count = row+1
            while down_count < 15 and board[down_count][column] is not None:
                word_points += self.points[board[down_count][column]]
                down_count += 1
            # Score the vertical word
            if place in specials:
                special = specials[place]
                if special == "DW":
                    word_points = (self.points[letter_played] + word_points)*2 if word_points != 0 else 0
                elif special == "TW":
                    word_points = (self.points[letter_played] + word_points)*3 if word_points != 0 else 0
                elif special == "DL":
                    word_points = (self.points[letter_played]*2 + word_points) if word_points != 0 else 0
                elif special == "TL":
                    word_points = (self.points[letter_played]*3 + word_points) if word_points != 0 else 0
            else:
                word_points = word_points + self.points[letter_played] if word_points != 0 else 0
            points += word_points
        
        # Score the word across
        # Get the first letter of the word across
        first_letter_col = None
        for place in corrected_placement:
            if first_letter_col is None or place[1] < first_letter_col:
                first_letter_col = place[1]
        
        column_iter = first_letter_col
        word_points = 0
        multiplier = 1
        # Look at the word rightwards from the first letter placed 
        while (column_iter < 15 and (board[row][column_iter] is not None or (row, column_iter) in corrected_placement) ):
            letter = board[row][column_iter]
            if letter is None:
                letter = corrected_placement[row, column_iter] 
            letter_pos = (row, column_iter)

            if letter in corrected_placement.values() and letter_pos in corrected_placement and letter_pos in specials:
                if specials[letter_pos] == "TW":
                    multiplier *= 3
                elif specials[letter_pos] == "DW":
                    multiplier *= 2
                elif specials[letter_pos] == "TL":
                    word_points += self.points[letter]*2
                elif specials[letter_pos] == "DL":
                    word_points += self.points[letter]
            word_points += self.points[letter]
            column_iter += 1

        # Look at the word leftwards from the first letter placed
        column_iter = first_letter_col - 1
        while (column_iter >= 0 and (board[row][column_iter] is not None or (row, column_iter) in corrected_placement)):
            letter = board[row][column_iter]
            if letter is None:
                letter = corrected_placement[row, column_iter] 
            letter_pos = (row, column_iter)
            if letter in corrected_placement.values() and letter_pos in corrected_placement and letter_pos in specials:
                if specials[letter_pos] == "TW":
                    multiplier *= 3
                elif specials[letter_pos] == "DW":
                    multiplier *= 2
                elif specials[letter_pos] == "TL":
                    word_points += self.points[letter]*2
                elif specials[letter_pos] == "DL":
                    word_points += self.points[letter]
            word_points += self.points[letter]
            column_iter -= 1
        # Account for multipliers
        word_points *= multiplier
        points += word_points
        # Check for bingo
        if len(placement) == 7:
            points += 50
        return points


    def solve(self):
        if '*' in self.rack:
            self.blank_solve()
        else:
            # Search all fifteen rows for best move(s)
            for i in range(15):
                row_anchors = self.get_anchors(i)
                for anchor in row_anchors:
                    if anchor != 0 and self.board[i][anchor-1] is not None:
                        prefix = ""
                        column_iter = anchor-1
                        while column_iter >= 0 and self.board[i][column_iter] is not None:
                            prefix += self.board[i][column_iter]
                            column_iter -= 1
                        prefix = prefix[::-1]
                        prefix_node = self.dictionary.path_node(prefix)
                        self.right_extend(prefix, prefix_node, (i, anchor), 0, (i, anchor))
                    else:
                        limit = 0
                        column_iter = anchor - 1
                        while column_iter >= 0 and self.board[i][column_iter] is None and column_iter not in row_anchors:
                            limit += 1
                            column_iter -= 1
                        self.left_part("", self.dictionary.root_node, limit, (i, anchor), 0)
            # Search all fifteen columns for moves
            
            for i in range(15):
                row_anchors = self.get_anchors(i, 1)
                for anchor in row_anchors:
                    if anchor != 0 and self.board_transp[i][anchor-1] is not None:
                        prefix = ""
                        column_iter = anchor-1
                        while column_iter >= 0 and self.board_transp[i][column_iter] is not None:
                            prefix += self.board_transp[i][column_iter]
                            column_iter -= 1
                        prefix = prefix[::-1]
                        prefix_node = self.dictionary.path_node(prefix)
                        self.right_extend(prefix, prefix_node, (i, anchor), 1, (i, anchor))
                    else:
                        limit = 0
                        column_iter = anchor - 1
                        while column_iter >= 0 and self.board_transp[i][column_iter] is None and column_iter not in row_anchors:
                            limit += 1
                            column_iter -= 1
                        self.left_part("", self.dictionary.root_node, limit, (i, anchor), 1)
            
        

    def left_part(self, partial_word, node, limit, anchor_location, transp):
        self.right_extend(partial_word, node, anchor_location, transp, anchor_location)

        if limit == 0:
            return     
        else:
            for edge in node.edges:
                if edge in self.rack:
                    self.rack.remove(edge)
                    new_node = node.edges[edge]
                    new_partial_word = partial_word + edge
                    self.left_part(new_partial_word, new_node, limit-1, anchor_location, transp)
                    self.rack.append(edge)
    
    def right_extend(self, partial_word, node, square, transp, base):
        if transp:
            board = self.board_transp
            cross_checks = self.cross_checks_transp
        else:
            board = self.board
            cross_checks = self.cross_checks

        row = square[0]
        if square[1] > 14:
            return
        if node is None:
            return
        if board[square[0]][square[1]] is None:
            if node.terminal and square != base:
                prev_square = (square[0], square[1]-1)
                move = self.generate_move(partial_word, prev_square, transp)
                score = self.get_points(move, (not transp))
                if score > self.best_score:
                    self.best_move = move
                    self.best_score = score
                    self.best_word = partial_word
                if len(partial_word) > self.longest_length:
                    self.longest_length = len(partial_word)
                    self.longest_score = score
                    self.longest_move = move
                    self.longest_word = partial_word
            for edge in node.edges:
                if edge in self.rack and edge in cross_checks[square[0]][square[1]]:
                    self.rack.remove(edge)
                    new_node = node.edges[edge]
                    new_partial_word = partial_word + edge
                    next_square = (square[0], square[1]+1)
                    self.right_extend(new_partial_word, new_node, next_square, transp, base)
                    self.rack.append(edge)
        else:
            l = board[square[0]][square[1]]
            if l in node.edges:
                new_node = node.edges[l]
                next_square = (square[0], square[1]+1)
                new_partial_word = partial_word + l
                self.right_extend(new_partial_word, new_node, next_square, transp, base)
            

    def generate_move(self, word, last_square, transp):
        '''
        Generates a placement of tiles for a word ending at a given square
        Assumes the move is possible and legal
        Note than if transposed is true, the placement returned will have transposed coordinates
        NOT true coordinates
        '''
        placement = dict()
        if transp:
            board = self.board_transp
        else:
            board = self.board
        row = last_square[0]
        column_iter = last_square[1]
        for i in range(len(word)):
            if board[row][column_iter] is None:
                if not transp:
                    placement[row,column_iter] = word[len(word)-1-i]
                else:
                    placement[column_iter, row] = word[len(word)-1-i]
            column_iter -= 1
        return placement

    def get_best_move(self):
        return (self.best_word, self.best_score, self.best_move)
    
    def get_longest_move(self):
        return (self.longest_word, self.longest_score, self.longest_move)

    def blank_solve(self):
        raise NotImplementedError
