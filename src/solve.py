# Solution based on the approach from: https://gist.github.com/evangelos-zafeiratos
import numpy as np

class Solve:

    def __init__(self, board):
        self.board = board

    def find_empty_cell(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if self.board[row][col] == 0:
                    return row, col
        return None

    def proof_number(self, number, row, col):
        for j in range(0, 9):
            if self.board[row][j] == number:
                return False
        for i in range(0, 9):
            if self.board[i][col] == number:
                return False
        block_row_start = 3 * (row // 3)
        block_col_start = 3 * (col // 3)
        block_row_end = block_row_start + 3
        block_col_end = block_col_start + 3
        for i in range(block_row_start, block_row_end):
            for j in range(block_col_start, block_col_end):
                if self.board[i][j] == number:
                    return False
        return True

    def solve_sudoku(self):
        cell = self.find_empty_cell()
        if cell is None:
            return True
        else:
            row, col = cell

        for number in range(1, 10):
            if self.proof_number(number, row, col):
                self.board[row][col] = number
                if self.solve_sudoku():
                    return True
                self.board[row][col] = 0
        return False

    def return_board(self):
        return self.board

    def find_valid_numbers(self, row, col):
        self.all_numbers_list = list()
        for number in range(1, 10):
            found = False

            for j in range(0, 9):
                if self.board[row][j] == number:
                    found = True
                    break

            if found:
                continue
            else:
                for i in range(0, 9):
                    if self.board[i][col] == number:
                        found = True
                        break

            if found:
                continue
            else:
                block_row_start = 3 * (row // 3)
                block_col_start = 3 * (col // 3)
                block_row_end = block_row_start + 3
                block_col_end = block_col_start + 3
                for i in range(block_row_start, block_row_end):
                    for j in range(block_col_start, block_col_end):
                        if self.board[i][j] == number:
                            found = True
                            break

            if not found:
                self.all_numbers_list.append(number)

        return self.all_numbers_list

    def save_valid_numbers(self):
        self.cache = dict()
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    self.cache[(row, col)] = self.find_valid_numbers(row, col)
        return self.cache

    def save_valid_numbers_ordered(self):
        self.cache = self.save_valid_numbers()
        self.cache_priority = dict()
        for row in range(9):
            temp_list_numbers = list()
            numbers_count = dict()
            for col in range(9):
                if (row, col) in self.cache.keys():
                    for number in self.cache[(row, col)]:
                        temp_list_numbers.append(number)
            temp_set_numbers = set(temp_list_numbers)
            for number in temp_set_numbers:
                numbers_count[number] = temp_list_numbers.count(number)

            for col in range(9):
                temp_list_frequencys = list()
                if (row, col) in self.cache.keys():
                    for number in self.cache[(row, col)]:
                        frequency = numbers_count[number]
                        temp_list_frequencys.append(frequency)
                    self.cache_priority[(row, col)] = temp_list_frequencys

        for row in range(9):
            for col in range(9):
                if (row, col) in self.cache.keys():
                    self.cache[row, col] = [i for _, i in sorted(zip(self.cache_priority[(row, col)], self.cache[(row, col)]))]

        return self.cache

    def solve_sudoku_cache(self):
        cell = self.find_empty_cell()
        if cell is None:
            return True
        else:
            row, col = cell
        self.cache = self.save_valid_numbers_ordered()
        for number in self.cache[(row, col)]:
            if self.proof_number(number, row, col):
                self.board[row][col] = number
                if self.solve_sudoku_cache():
                    return True
                self.board[row][col] = 0
        return False