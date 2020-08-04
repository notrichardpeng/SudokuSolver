from gui import canvas

class Boardtile:
	def __init__(self, tkid, val):
		self.tkid = tkid
		self.val = val

valid_numbers = [[[0 for k in range(9)] for j in range(9)] for i in range(9)]
board = [[None for i in range(9)] for j in range(9)]
tile_x = []
tile_y = []

def solve_sudoku():
	hasempty = False
	for i in range(9):
		for j in range(9):
			if board[i][j].val == " ":
				hasempty = True
				for n in range(1, 10):
					canvas.itemconfig(board[i][j].tkid, text=str(n), fill="blue")
					board[i][j].val = str(n)
					update_valid(i, j, n-1, 1)

					if valid_numbers[i][j][n-1] == 0 and solve_sudoku():						
						return True
						
					update_valid(i, j, n-1, -1)
					canvas.itemconfig(board[i][j].tkid, text=" ")

				board[i][j].val = " "

	if not hasempty:
		return True
	return False


def find_closest_tile_x(rawval):		
	if rawval <= 45 or rawval >= 405:
		return -1

	for i in range(len(tile_x)):
		if i == 0:
			if rawval <= tile_x[i]:
				return i
		elif tile_x[i-1] <= rawval and tile_x[i] >= rawval:
			leftdiff = rawval - tile_x[i-1]
			rightdiff = tile_x[i] - rawval
			if leftdiff <= rightdiff:
				return i-1
			else:
				return i
	
	if rawval >= tile_x[i]:
		return i
	return -1					

def find_closest_tile_y(rawval):
	if rawval <= 10 or rawval >= 370:
		return -1
		
	for i in range(len(tile_y)):
		if i == 0:
			if rawval <= tile_y[i]:
				return i
		elif tile_y[i-1] <= rawval and tile_y[i] >= rawval:
			leftdiff = rawval - tile_y[i-1]
			rightdiff = tile_y[i] - rawval
			if leftdiff <= rightdiff:
				return i-1
			else:
				return i
	
	if rawval >= tile_y[i]:
		return i
	return -1

def update_valid(x, y, num, val):
	for i in range(x-1, -1, -1): valid_numbers[i][y][num] += val 
	for i in range(x+1, 9): valid_numbers[i][y][num] += val
	for i in range(y-1, -1, -1): valid_numbers[x][i][num] += val 
	for i in range(y+1, 9): valid_numbers[x][i][num] += val 

	startx, starty = 0, 0	
	if x >= 3 and x < 6: startx = 3
	elif x >= 6: startx = 6
	if y >= 3 and y < 6: starty = 3
	elif y >= 6: starty = 6

	for i in range(startx, startx+3):
		for j in range(starty, starty+3):
			valid_numbers[i][j][num] += val


def reset_valid():
	for i in range(9):
		for j in range(9):
			for num in range(9):
				valid_numbers[i][j][num] = 0