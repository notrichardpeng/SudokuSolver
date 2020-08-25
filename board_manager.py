import time
import random

class Boardtile:
	def __init__(self, tkid, val):
		self.tkid = tkid
		self.val = val

board = [[None for i in range(9)] for j in range(9)]

#--------------------Sudoku Solving---------------------------------

tries = 0
solve_active = False

def reset_tries(triestext):
	global tries
	tries = 0
	triestext['text'] = "Tries: 0"

def solve_sudoku(canvas, triestext):
	if not solve_active: return False

	global tries
	empty = find_empty_spot()
	if not empty: return True

	i, j = empty[0], empty[1]
	for n in range(1, 10):					
		canvas.itemconfig(board[i][j].tkid, text=str(n), fill="green4")
		board[i][j].val = str(n)

		time.sleep(0.01)		

		if(valid_numbers[i][j][n-1] == 0):
			tries += 1
			triestext['text'] = "Tries: " + str(tries)
			update_valid(i, j, n-1, 1)	
			if solve_sudoku(canvas, triestext):
				return True				
			update_valid(i, j, n-1, -1)

		canvas.itemconfig(board[i][j].tkid, text=" ", fill="green")
					
	board[i][j].val = " "

	return False

def find_empty_spot():
	for i in range(9):
		for j in range(9):
			if board[i][j].val == " ":
				return [i, j]
	return None

def not_unique_solution(count):
	empty = find_empty_spot()
	if not empty: 
		count[0] += 1
		if count[0] > 1: return True
		return False

	i, j = empty[0], empty[1]	
	
	for n in range(1,10):							
		if(valid_numbers[i][j][n-1] == 0):			
			board[i][j].val = str(n)

			update_valid(i, j, n-1, 1)	
			if not_unique_solution(count):
				update_valid(i, j, n-1, -1)
				board[i][j].val = " "
				return True			

			update_valid(i, j, n-1, -1)				
	
	board[i][j].val = " "
	return False	

#------------------------------Generate Board-------------------------------------------------------

def generate_solved_board():
	empty = find_empty_spot()
	if not empty: return True

	i, j = empty[0], empty[1]
	r = list(range(1, 10))
	random.shuffle(r)

	for n in r:							
		if(valid_numbers[i][j][n-1] == 0):			
			board[i][j].val = str(n)

			update_valid(i, j, n-1, 1)	
			if generate_solved_board():
				return True				
			update_valid(i, j, n-1, -1)
	
	board[i][j].val = " "
	return False	

def remove_solved_numbers():
	num_clues = random.randint(30, 37)
	num_remove = 81 - num_clues
	print(num_remove)
	while num_remove > 0:	
		i, j = random.randint(0, 8), random.randint(0, 8)
		if board[i][j].val == " ": continue

		temp = board[i][j].val
		update_valid(i, j, int(temp)-1, -1)
		board[i][j].val = " "

		count = [0]
		if not_unique_solution(count):
			board[i][j].val = temp
			update_valid(i, j, int(temp)-1, 1)
		else:	
			num_remove -= 1

def fill_in_visual_for_board(canvas):
	for i in range(9):
		for j in range(9):
			canvas.itemconfig(board[i][j].tkid, text=board[i][j].val, fill="blue")

#-------------------------Locating tile according to mouse position---------------------------------

tile_x = []
tile_y = []

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

#----------------------Valid Numbers----------------------------------

valid_numbers = [[[0 for k in range(9)] for j in range(9)] for i in range(9)]

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


