
import tkinter
import threading
import board_manager as BM
from tkinter import messagebox

canvas = None
root = None
edit_number = " "
current_active_number = None
is_solving = False

#Helper functions-----------------------------------------------------------------------------------------

def reset_active_number():
	global current_active_number, edit_number	
	if current_active_number:
		current_active_number.config(relief=tkinter.RAISED)
		current_active_number = None
	edit_number = " "

#Callbacks-------------------------------------------------------------------------------------------

def canvas_on_click(event):			
	global is_solving
	if edit_number == " " or is_solving:
		return		
	
	mousex = canvas.canvasx(event.x)
	mousey = canvas.canvasy(event.y)
	r = BM.find_closest_tile_y(mousey)	
	c = BM.find_closest_tile_x(mousex) 

	if r < 0 or c < 0: return
	
	clicked = BM.board[r][c].tkid	
	if edit_number != '' and canvas.itemcget(clicked, 'text') != ' ': return

	if canvas.itemcget(clicked, 'text') != "X": 		
		if edit_number == "":
			t = canvas.itemcget(clicked, 'text')
			if t == ' ': return

			check = int(t)-1
			BM.update_valid(r, c, check, -1)	
			for i in range(9):
				for j in range(9):			
					if BM.valid_numbers[i][j][check]==0 and canvas.itemcget(BM.board[i][j].tkid, 'text') == 'X':
						canvas.itemconfig(BM.board[i][j].tkid, text=' ')
			canvas.itemconfig(clicked, text=" ", fill="blue")	
			BM.board[r][c].val = " "
		else:
			check = int(edit_number)-1
			BM.update_valid(r, c, check, 1)
			for i in range(9):
				for j in range(9):			
					if BM.valid_numbers[i][j][check]>0 and canvas.itemcget(BM.board[i][j].tkid, 'text') == ' ':
						canvas.itemconfig(BM.board[i][j].tkid, text='X', fill="red")	
			canvas.itemconfig(clicked, text=edit_number, fill="blue")	
			BM.board[r][c].val = edit_number

def edit_number_button(num, b):
	global edit_number, current_active_number, canvas, is_solving
	if is_solving: return

	edit_number = num
	
	clear_x()
	if current_active_number == b:
		reset_active_number()		
		return

	if num != '':
		check = int(num)-1
		for i in range(9):
			for j in range(9):			
				if BM.valid_numbers[i][j][check]>0 and canvas.itemcget(BM.board[i][j].tkid, 'text') == ' ':
					canvas.itemconfig(BM.board[i][j].tkid, text='X', fill="red")

	if current_active_number: current_active_number.config(relief=tkinter.RAISED)
	b.config(relief=tkinter.SUNKEN)	
	current_active_number = b

def clear_board():
	global canvas, current_active_number, edit_number, is_solving
	if is_solving: return	

	tiles = canvas.find_withtag("tile")
	for i in tiles:
		canvas.itemconfig(i, text=" ")

	for i in range(9):
		for j in range(9):
			BM.board[i][j].val = " "

	if current_active_number != None:
		reset_active_number()
		clear_x()	
	BM.reset_valid()

def generate_random():
	global is_solving
	if is_solving: return

	reset_active_number()
	clear_x()

def solve_sudoku():
	global is_solving, canvas
	if is_solving: return

	reset_active_number()
	clear_x()
	is_solving = True	
	if BM.solve_sudoku(canvas):
		messagebox.showinfo("Result", "The given sudoku has been solved!")
	else: messagebox.showinfo("Result", "The given sudoku is unsolvable.")
	is_solving = False

#Visual----------------------------------------------------------------------------------------------

def create_sudoku_board():	
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
		cx, cy = 0, 0
		for j in range(9):
			x = i*spacing+(spacing/2)+start_x
			y = j*spacing+(spacing/2)+start_y

			tile = canvas.create_text(x, y, text=" ", tags=("tile", "tile"+str(i)+str(j)))
			c = canvas.coords(tile)				
			cx, cy = c[0], c[1]
			if len(BM.tile_y) < 9: BM.tile_y.append(cy)			
			BM.board[j][i] = BM.Boardtile(tile, " ") # Board[j][i] because coordinate system different for Tkinter	
		BM.tile_x.append(cx)		

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
	generate = tkinter.Button(buttons, text="Generate Random", command=generate_random)
	solve = tkinter.Button(buttons, text="Solve", command=lambda: threading.Thread(target=solve_sudoku).start())
	generate.pack(side=tkinter.LEFT, padx=5)
	solve.pack(side=tkinter.LEFT, padx=5)

def clear_x():
	global canvas
	for i in range(9):
		for j in range(9):
			if canvas.itemcget(BM.board[i][j].tkid, 'text') == 'X':
				canvas.itemconfig(BM.board[i][j].tkid, text=" ")

#----------------------------------------------------------------------------------------------------

def main():	
	global root, canvas, edit_number, current_active_number
	root = tkinter.Tk()
	canvas = tkinter.Canvas(root, width=450, height=400)	

	edit_number = " "
	current_active_number = None


	root.geometry('500x500')
	root.title('Sudoku Solver')	
	create_sudoku_board()
	create_number_buttons()
	create_utility_buttons()	
	root.mainloop()	

if __name__ == '__main__':
	main()