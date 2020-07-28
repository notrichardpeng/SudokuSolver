
board = [[-1 for i in range(9)] for j in range(9)]
tile_x = []
tile_y = []

valid_numbers = [[[False for k in range(9)] for j in range(9)] for i in range(9)]

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

def update_valid(x, y, num):
	for i in range(x-1, -1, -1): valid_numbers[i][y][num] = True 
	for i in range(x+1, 9): valid_numbers[i][y][num] = True 
	for i in range(y-1, -1, -1): valid_numbers[x][i][num] = True 
	for i in range(y+1, 9): valid_numbers[x][i][num] = True 