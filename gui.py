import tkinter

def create_sudoku_board(root):
	canvas = tkinter.Canvas(root, height=450)

	spacing = 40
	startY = 10
	startX = 10

	for i in range(9):
		y = i*spacing+startY
		canvas.create_line(10, y, 500, y)
	for i in range(9):
		x = i*spacing+startX
		canvas.create_line(x, 10, x, 500)

	canvas.pack()


def main():
	root = tkinter.Tk()
	root.geometry('500x500')
	root.title('Sudoku Solver')
	create_sudoku_board(root)
	root.mainloop()

if __name__ == '__main__':
	main()