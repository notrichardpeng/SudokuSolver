import tkinter

root = tkinter.Tk()


def create_sudoku_board():

	global root
	canvas = tkinter.Canvas(root, width=450, height=400)

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
			canvas.create_text(x, y, text="0")
			
	canvas.pack()
	


def main():	
	root.geometry('500x500')
	root.title('Sudoku Solver')
	create_sudoku_board()
	root.mainloop()

if __name__ == '__main__':
	main()