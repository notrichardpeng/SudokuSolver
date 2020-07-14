
import tkinter

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=450, height=400)	
tile_coordinates = []

edit_number = " "
current_active_number = None

#Helper functions-----------------------------------------------------------------------------------------

def find_closest_tile_x(rawval):		
	if rawval <= 45 or rawval >= 405:
		return -1

	for i in range(len(tile_coordinates)):
		if i == 0:
			if rawval <= tile_coordinates[i][0]:
				return tile_coordinates[i][0]				
		elif tile_coordinates[i-1][0] <= rawval and tile_coordinates[i][0] >= rawval:
			leftdiff = rawval - tile_coordinates[i-1][0]
			rightdiff = tile_coordinates[i][0] - rawval
			if leftdiff <= rightdiff:
				return tile_coordinates[i-1][0]					
			else:
				return tile_coordinates[i][0]

	i -= 1
	if rawval >= tile_coordinates[i][0]:
		return tile_coordinates[i][0]
	return -1					

def find_closest_tile_y(x, rawval):
	if rawval <= 10 or rawval >= 370:
		return -1

	start = -1
	for i in range(len(tile_coordinates)):
		if tile_coordinates[i][0] == x:
			start = i
			break
		
	i = start
	while i < len(tile_coordinates) and tile_coordinates[i][0] == x:
		if i == 0 or tile_coordinates[i-1][0] != x:
			if rawval <= tile_coordinates[i][1]:
				return tile_coordinates[i][1]			
		elif tile_coordinates[i-1][1] <= rawval and tile_coordinates[i][1] >= rawval:
			leftdiff = rawval - tile_coordinates[i-1][1]
			rightdiff = tile_coordinates[i][1] - rawval
			if leftdiff <= rightdiff:
				return tile_coordinates[i-1][1]					
			else:
				return tile_coordinates[i][1]	
		i += 1
	i -= 1		
	if rawval >= tile_coordinates[i][1]:
		return tile_coordinates[i][1]

	return -1

#Callbacks-------------------------------------------------------------------------------------------

def canvas_on_click(event):					
	if edit_number == " ":
		return
	
	mousex = canvas.canvasx(event.x)
	mousey = canvas.canvasy(event.y)
	x = find_closest_tile_x(mousex) 
	y = find_closest_tile_y(x, mousey)					
	if x >= 0 and y >= 0: canvas.itemconfig(canvas.find_closest(x, y), text=edit_number)	


def edit_number_button(num, b):
	global edit_number, current_active_number	
	edit_number = num

	if current_active_number == b:
		current_active_number.config(relief=tkinter.RAISED)
		current_active_number = None
		edit_number = " "
		return

	if current_active_number: current_active_number.config(relief=tkinter.RAISED)
	b.config(relief=tkinter.SUNKEN)	
	current_active_number = b

def clear_board():
	global canvas, current_active_number, edit_number
	tiles = canvas.find_withtag("tile")
	for i in tiles:
		canvas.itemconfig(i, text=" ")

	if current_active_number != None:
		current_active_number.config(relief=tkinter.RAISED)
		edit_number = " "
		current_active_number = None

#Visual----------------------------------------------------------------------------------------------

def create_sudoku_board():	
	global board
	board = [[None for j in range(9)] for _ in range(9)]
	spacing = 40
	start_y = 10
	start_x = 45
	board_size = 360

	for i in range(10):
		y = i*spacing+start_y
		if i % 3 == 0: canvas.create_line(start_x, y, start_x+board_size, y, width=3)
		else: canvas.create_line(start_x, y, start_x+board_size, y)
	for i in range(10):
		x = i*spacing+start_x
		if i % 3 == 0: canvas.create_line(x, start_y, x, start_y+board_size, width=3)
		else: canvas.create_line(x, start_y, x, start_y+board_size)
		for i in range(9):
			for j in range(9):
				x = i*spacing+(spacing/2)+start_x
				y = j*spacing+(spacing/2)+start_y

				tile = canvas.create_text(x, y, text=" ", tags=("tile", "tile"+str(i)+str(j)))
				c = canvas.coords(tile)
				tile_coordinates.append(c)
			

	canvas.bind("<Button-1>", canvas_on_click)
	canvas.pack()		

def create_number_buttons():	
	numbers = tkinter.Frame(root, bd=0)
	numbers.pack()

	text = tkinter.Label(numbers, text="Edit")
	text.pack(side=tkinter.LEFT, padx=5)

	for i in range(1, 10):
		button = tkinter.Button(numbers, text=str(i))
		button.config(command=lambda i=i,button=button: edit_number_button(str(i), button))
		button.pack(side=tkinter.LEFT, padx=5)		

	delete = tkinter.Button(numbers, text="remove")
	delete.config(command=lambda i=i,button=delete: edit_number_button("", button))
	delete.pack(side=tkinter.LEFT, padx=5)
	deleteAll = tkinter.Button(numbers, text="clear")
	deleteAll.config(command=clear_board)
	deleteAll.pack(side=tkinter.LEFT, padx=5)

def create_utility_buttons():
	buttons = tkinter.Frame(root, bd=0)
	buttons.pack(pady=5)
	generate = tkinter.Button(buttons, text="Generate Random")
	solve = tkinter.Button(buttons, text="Solve")
	generate.pack(side=tkinter.LEFT, padx=5)
	solve.pack(side=tkinter.LEFT, padx=5)

#----------------------------------------------------------------------------------------------------

def main():	
	root.geometry('500x500')
	root.title('Sudoku Solver')	
	create_sudoku_board()
	create_number_buttons()
	create_utility_buttons()
	root.mainloop()

if __name__ == '__main__':
	main()