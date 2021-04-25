#!/usr/bin/python3

#we import sys and getopt library for the command-line arguments of the program
import sys, getopt, os

# initialize a limited colors and alphabets that we will use to represent the vertex
color = ["Red", "Yellow", "Green", "Orange", "Blue", "Violet", "Purple"]

# symmetric edge finder function
# This function will find all the  symmetric edges in our program such as (i, j) and (j, i) is the same representation of edges
# Graph coloring is commonly used on unweighted graphs only but I also tried to support weighted graphs as well
def symmetricEdge(e):
	info = []
	x = 0
	for i in range(len(e)):
		for j in range(len(e)):
			if e[i][j] >= 1:
				info.append([j, i])
				try:
					info.remove([i, j])
				except:
					pass
	return info

# Vertex adjacency finder function
# This function will find all the adjacent vertex to all of the vertices
def setVertex(e, V):
	setvertex = {}
	sel_vertex = 0
	while sel_vertex < V:
		adjacent = []
		for j in range(len(e)):
			if e[j][0] == sel_vertex:
				adjacent.append(e[j][1])
			elif e[j][1] == sel_vertex:
				adjacent.append(e[j][0])
		# JSON structure {vertex : [index_color, [adjacent_vertices]]}	
		setvertex[str(sel_vertex)] = [0, adjacent]
		sel_vertex +=1
	return setvertex

# Graph Coloring function
# This function will give colors to each vertex and implements the rules of no two adjacent vertices may have the same color 
def graphColoring(G, V):
	symmetricpoints = symmetricEdge(G)
	vertex = setVertex(symmetricpoints, V)
	for i in range(0, len(vertex)):
		for j in range(0, len(vertex)):
			# check if all edges in the current vertex are connected and have the same color
			if i in vertex[str(j)][1] and vertex[str(i)][0] == vertex[str(j)][0]:
				# then increment the indicator
				vertex[str(j)][0] += 1 
	return vertex

# txt file to Matrix function
# It reads and converts the txt file to Matrix. 
# I use this to understand my script the inputs by converting it to a readable computer language
def txttoMatrix(file):
	matrix = []
	txt = open(file, 'rt')
	val = txt.readlines()
	txt.close()
	for i in range(len(val)):
		row = []
		digit = ""
		for j in range(len(val[i])):
			digit += str(val[i][j])
			if val[i][j] == " " or val[i][j] == "\n" or j == len(val[i])-1:
				row.append(int(digit))
				digit = ""
		matrix.append(row)
	return matrix


# Program's Matrix to txt file
# Output the program's Matrix / adjacency matrix to txt file
# Designing what type of output should I want in the txt file
def matrixtoTxt(filename, arr, V):
	graphcolored = graphColoring(arr, V)
	outputstr = "Vertex Colors\n--------------------------\n"
	txt = open(filename, 'w')
	# organize list
	for i in color:
		setcolor = []
		for j in graphcolored:
			if i == color[graphcolored[str(j)][0]]:
				setcolor.append(int(j))
		if len(setcolor):
			outputstr += i +" = "+ str(setcolor) +"\n"
	txt.write(outputstr)
	txt.close()
	
# command line arguments
argv = sys.argv[1:]
try:
	opts, args = getopt.getopt(argv, "i:o:h")
	inputfile = ""
	for opt, arg in opts:
		if opt == '-h':
			print("\nHelp Command:\n\tcolor.py -i <inputfile> -o <outputfile>")
			sys.exit()
		elif opt in ('-i', "--input"):
			# check if the undirected graph is symmetric or have a problem reading
			try:
				inputfile = txttoMatrix(arg)
			except:
				print("\nError Detected:\nThere is a problem in the input.txt file while reading!\nPlease remove spaces in the input, the matrix must be\nsymmetric and also remove newline to avoid errors.")
				sys.exit()
		elif opt in ('-o', "--output"):
			matrixtoTxt(arg, inputfile, len(inputfile))
			print("\nSuccess: Your "+arg+" has been already save in "+os.path.dirname(os.path.realpath(__file__)))
except getopt.error as err:
	print(str(err))


