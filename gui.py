import tkinter

root = tkinter.Tk()

class SudokuSolver:

	def __init__(self):
		self.canvas = tkinter.Canvas(root, width=450, height=400)
		self.coordinates = []

	#Helper functions
	def find_closest_tile_x(self, rawval):		
		if rawval <= 45 or rawval >= 405:
			return -1

		for i in range(len(self.coordinates)):
			if i == 0:
				if rawval > 45 and rawval <= 65:
					return self.coordinates[i][0]				
			elif i == len(self.coordinates)-1:
				if rawval < 405 and rawval >= 385:
					return self.coordinates[i][0]					
			elif self.coordinates[i-1][0] <= rawval and self.coordinates[i][0] >= rawval:
				leftdiff = rawval - self.coordinates[i-1][0]
				rightdiff = self.coordinates[i][0] - rawval
				if leftdiff <= rightdiff:
					return self.coordinates[i-1][0]					
				else:
					return self.coordinates[i][0]					

	#TODO
	#def find_closest_tile_y(self, x, rawval):


	#Callbacks
	def tile_on_click(self, event, tile, canvas):
		canvas.itemconfig("current", text="1")

	def canvas_on_click(self, event):
		# TODO: round the event coordinate to find the nearest tile, and retrieve the tile via its coordinate, then modify the tile.
		
		mousex = self.canvas.canvasx(event.x)
		mousey = self.canvas.canvasy(event.y)
		x, y = self.find_closest_tile_x(mousex), -1			
		
		print(x, y)


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

		self.canvas.bind("<Button-1>", self.canvas_on_click)
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