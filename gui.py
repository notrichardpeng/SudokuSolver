import tkinter

root = tkinter.Tk()

def tile_on_click(event, tile, canvas):
	canvas.itemconfig("current", text="1")

def canvas_on_click(event):
	#TODO: round the event coordinate to find the nearest tile, and retrieve the tile via its coordinate, then modify the tile.
	canvas = event.widget
	x = canvas.canvasx(event.x)
	y = canvas.canvasy(event.y)
	item = canvas.find_closest(x, y)
	canvas.delete(item)

class SudokuSolver:

	def __init__(self):
		self.canvas = tkinter.Canvas(root, width=450, height=400)
		self.coordinates = []

	def create_sudoku_board(self):

		global root
		board = [[None for j in range(9)] for _ in range(9)]

		spacing = 40
		start_y = 10
		start_x = 45
		board_size = 360

		for i in range(10):
			y = i*spacing+start_y
			if i % 3 == 0: self.canvas.create_line(start_x, y, start_x+board_size, y, width=3)
			else: self.canvas.create_line(start_x, y, start_x+board_size, y)
		for i in range(10):
			x = i*spacing+start_x
			if i % 3 == 0: self.canvas.create_line(x, start_y, x, start_y+board_size, width=3)
			else: self.canvas.create_line(x, start_y, x, start_y+board_size)

		for i in range(9):
			for j in range(9):
				x = i*spacing+(spacing/2)+start_x
				y = j*spacing+(spacing/2)+start_y
				tile = self.canvas.create_text(x, y, text="0")
				c = self.canvas.coords(tile)
				self.coordinates.append(c)

		self.canvas.bind("<Button-1>", canvas_on_click)
		self.canvas.pack()
		print(self.coordinates)

def main():	
	root.geometry('500x500')
	root.title('Sudoku Solver')
	sudoku_solver = SudokuSolver()
	sudoku_solver.create_sudoku_board()
	root.mainloop()

if __name__ == '__main__':
	main()