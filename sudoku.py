#!usr/bin/env python
#================================================================
# Sudoku Puzzle Solver 
# Author: Arunprasath Shankar
# axs918@case.edu
#================================================================

import sys
import time
import sudosolver
def main():
	""" sudoku main program.
	"""
	argList = sys.argv[1:]
	if len(argList) == 0:
		message("*** You must supply names of atleast one sudoku puzzle file.\n")
	else:
		for arg in argList:
			solveFile(arg)

def message(*L):
	""" Write a message to sys.stderr.
	"""
	sys.stderr.write("*** %s\n" % " ".join(L))

def fatal(*L):
	""" Write a message and terminate.
	"""
	message(*L)
	sys.exit(1)

def solveFile(fileName):
	""" Try to solve one puzzle.
	"""
	try:
		inFile = open(fileName)
		rawPuzzle = inFile.read()
	except IOError, detail:
			message("*** Can't open file '%s' for reading. %s\n" % (fileName,detail))
			return
	try:
		solver = sudosolver.SudokuSolver(rawPuzzle,solutionFound)
	except ValueError,detail:
		message("Invalid puzzle:%s" % detail)
		return
	separator = "=" * 9 
	print ("\n%s %s %s" % (separator,fileName,separator))
	solver.write(sys.stdout)
	startClock = time.clock()
	solver.solve()
	endClock = time.clock()
	print "\nNumber of solutions found:",solver.nSolutions
	print "Elapsed cpu time: %8f seconds." % (endClock - startClock)

def solutionFound(solver):
	""" Report a successful solution to the puzzle.
	"""
	print "\n--- Solution #%d:" % solver.nSolutions
	solver.write(sys.stdout)

#========================================================================================
# Epilogue
#----------------------------------------------------------------------------------------

if __name__ == "__main__":
	main()








