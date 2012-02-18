"""sudosolver.py: Sudoku puzzle solver
"""
SUBMAT_L = 3
MAT_L = SUBMAT_L ** 2
BOARD_L = MAT_L ** 2
EMPTY = 0
# - - - - - class SudokuSolver - - - - - 
class SudokuSolver:
	""" Represents one sudoku puzzle.
	"""
	def __init__(self,givenPuzzle,solutionObserver = None,changeObserver = None):
		"""Constructor for SudokuSolver."""
		self.givenPuzzle		=		 givenPuzzle
		self.solutionObserver   =        solutionObserver
		self.changeObserver     =        changeObserver
		self.nStateChanges      =        0
		self.nSolutions         =        0
		self.__board            =        self.__readPuzzle()
		self.__given            =        self.__board[:]

	def __readPuzzle(self):
		""" Translate the puzzle from external to internal form."""
		charList = [c for c in list(self.givenPuzzle) if not c.isspace()]
		if len(charList) != BOARD_L:
			raise ValueError, ("Puzzle has %d nonblank charcters; it should have exactly %d characters" % (len(charList),BOARD_L))
		result = [self.__readChar(c) for c in charList]
		return result

	def __readChar(self,c):
		""" Translate one input character. """
		if c == '.':
			return 0
		elif '1' <= c <= '9':
			return int(c)
		else:
			raise ValueError,("Invalid sudoku character: '%s'" % c)
		
	def get(self,r,c):
		""" Get the cell at row r and column c. """
		if not(0 <= r < MAT_L):
			raise KeyError,("SudokuSolver.get(): Bad row index, %d." % r)
		if not(0 <= c < MAT_L):
			raise KeyError,("SudokuSolver.get(): Bad column index, %d." % c)
		x = self.__rowColToX(r,c)
		return self.__board[x]

	def __rowColToX(self,r,c):
		return (r*MAT_L) + c

	def write(self,outFile):
		for rowx in range(MAT_L):
			if ((rowx > 0) and ((rowx % SUBMAT_L) == 0)):
				print >>outFile
			self.writeRow(outFile,rowx)

	def writeRow(self,outFile,rowx):
		"""Display one row in plain text."""
		for colx in range(MAT_L):
			cell = self.get(rowx,colx)
			if cell == 0: c = '.'
			else: c = chr(ord('0')+cell)
			if ((colx > 0) and ((colx % SUBMAT_L) == 0)):
				print >>outFile," ",
			print >>outFile,c,
		print >>outFile

# - - - SudokuSolver.Solve - - - 
	def solve(self):
		""" Find all solutions to the puzzle.
		"""
		self.__reSolve(0)

	def __reSolve(self,x):
		""" Recursively solve the puzzle.
		"""
		if x >= BOARD_L:
			self.__solution()
			return
		if self.__given[x] != EMPTY:
			self.__reSolve(x+1)
			return
		possibles = self.__findPossibles(x)
		for trial in possibles:
			self.__set(x,trial)
			self.__reSolve(x+1)
			
		self.__set(x,EMPTY)

	def __solution(self):
		""" A solution has been found.
		"""
		self.nSolutions += 1
		if self.solutionObserver is not None:
			self.solutionObserver(self)
	def __findPossibles(self,x):
		""" What digits are legal position x on the board?
		"""
		rowElim = self.__usedInRow(x)
		colElim = self.__usedInColumn(x)
		subElim = self.__usedInSubmat(x)
		elim = [rowElim[x] | colElim[x] | subElim[x] for x in range(MAT_L)]
		result = [i+1 for i in range(0,MAT_L) if elim[i] == 0]
		return result

	def __usedInRow(self,x):
		"""What digits are used elsewhere in the row containing x?
		"""
		rx,cx = self.__xToRowCol(x)
		result = [0] * MAT_L
		for col in range(MAT_L):
			if col != cx:
				cell = self.get(rx,col)
				if cell != EMPTY:
					result[cell - 1] = 1
		return result

	def __usedInColumn(self,x):
		""" What digits are used elsewhere in the column containing x ?
		"""
		rx,cx = self.__xToRowCol(x)
		result = [0] * MAT_L
		for row in range(MAT_L):
			if row != rx:
				cell = self.get(row,cx)
				if cell != EMPTY:
					result[cell - 1] = 1
		return result

	def __usedInSubmat(self,x):
		"""What digits are used in the submatrix containing x ?
		"""
		result = [0] * MAT_L
		rx,cx = self.__xToRowCol(x)
		rSub = (rx/3) * 3
		cSub = (cx/3) * 3
		for rowx in range(rSub,rSub+SUBMAT_L):
			for colx in range(cSub,cSub+SUBMAT_L):
				if((rowx != rx) or (colx != cx)):
					cell = self.get(rowx,colx)
					if cell != EMPTY:
						result[cell -1] = 1
		return result

	def __set(self,x,value):
		""" Set or clear one cell of the board.
		"""
		self.__board[x] = value
		self.nStateChanges += 1
		if self.changeObserver is not None:
			row,col = self.__xToRowCol(x)
			self.changeObserver(self,row,col,value)

	def __xToRowCol(self,x):
		""" Translate board index into rows and columns.
		"""
		return divmod(x,9)


		

