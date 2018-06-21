# Date: 3/21/2016
#in cmd: py -3 tester1p.py sfaust3_p1.py
#	OR   python tester1p.py sfaust3_p1.py

#energies = color gradient for each pixel
#cheapest path (from topto bottom, moving like a pawn)
#remove path
#(portable pixmap format (p3 ver) and imagemagick tool?)
#try to use ONLY recursion!

#column count
def width(grid):
	return len(grid[0])
#-------------------------------------------------------------------------------
#row count
def height(grid):
	return len(grid)
	
################################################################################
def energy_at(grid, r, c):
	#given a grid of RGB triplets
	#check if border node
	leftR = 0
	leftG = 0
	leftB = 0
	rightR = 0
	rightG = 0
	rightB = 0
	upR = 0
	upG = 0
	upB = 0
	downR = 0
	downG = 0
	downB = 0

	#do we check up, down, or both?
	if r==0:
		#check down while up wraps around
		upR = grid[height(grid)-1][c][0]
		upG = grid[height(grid)-1][c][1]
		upB = grid[height(grid)-1][c][2]
		downR = grid[r+1][c][0]
		downG = grid[r+1][c][1]
		downB = grid[r+1][c][2]
	else:
		if r==(height(grid)-1):
			#check up while down wraps around
			upR = grid[r-1][c][0]
			upG = grid[r-1][c][1]
			upB = grid[r-1][c][2]
			downR = grid[0][c][0]
			downG = grid[0][c][1]
			downB = grid[0][c][2]
		else:
			#check both
			upR = grid[r-1][c][0]
			upG = grid[r-1][c][1]
			upB = grid[r-1][c][2]
			downR = grid[r+1][c][0]
			downG = grid[r+1][c][1]
			downB = grid[r+1][c][2]
			
			
			
			
	#do we check left, right, or both?
	if c==0:
		#check right while left wraps around
		rightR = grid[r][c+1][0]
		rightG = grid[r][c+1][1]
		rightB = grid[r][c+1][2]
		leftR = grid[r][width(grid)-1][0]
		leftG = grid[r][width(grid)-1][1]
		leftB = grid[r][width(grid)-1][2]
	else:
		if c==(width(grid)-1):
			#check left while right wraps around
			rightR = grid[r][0][0]
			rightG = grid[r][0][1]
			rightB = grid[r][0][2]
			leftR = grid[r][c-1][0]
			leftG = grid[r][c-1][1]
			leftB = grid[r][c-1][2]
		else:
			#check both
			rightR = grid[r][c+1][0]
			rightG = grid[r][c+1][1]
			rightB = grid[r][c+1][2]
			leftR = grid[r][c-1][0]
			leftG = grid[r][c-1][1]
			leftB = grid[r][c-1][2]
	
	#now we calculte the energy
	rx = (rightR - leftR)**2
	gx = (rightG - leftG)**2
	bx = (rightB - leftB)**2
	ry = (upR - downR)**2
	gy = (upG - downG)**2
	by = (upB - downB)**2
	
	return (rx+gx+bx+ry+gy+by)
#-------------------------------------------------------------------------------			
#returns a grid of the energies at each point
def energy(grid):
	return energy_helper(grid, width(grid), height(grid), 0, 0, [[]])
#recursion!!
def energy_helper(grid, w, h, curR, curC, egrid):
	if curR>=h:
		return egrid
	if curC>=w:
		return energy_helper(grid, w, h, (curR+1), 0, egrid)
	if curR==(height(egrid)):
		egrid.append([])
	egrid[curR].append(energy_at(grid, curR, curC))
	return energy_helper(grid, w, h, curR, (curC+1), egrid)
	
################################################################################
def find_vertical_path(grid):
	egrid = energy(grid)
	#grabs the index(es) of the minimum value in the first row
	minis = minimum(egrid[0], egrid[0][0], [], 0, width(egrid))
	paths = []
	for p in minis:
		#paths is a list of tuples (path, pathcost)
		paths.append(vert_path_helper(egrid, width(grid), height(grid), (0, p), [(0, p)], 0))
	least = paths[0][1]
	least_index = 0
	indexCount = 0
	#now we find and return the path of least path cost
	for k in paths:
		if indexCount==0:
			indexCount+=1
		else:
			if k[1]<least:
				least = k[1]
				least_index=indexCount
				indexCount+=1
	return paths[least_index][0]

#recursively finds the path
def vert_path_helper(egrid, w, h, curP, path, pathcost):
	if curP[0]>=(h-1):
		#end the recursion
		return (path, pathcost)	
	#next_point_index is the column index of the minimum adjacent point
	next_point_index = 0;
	#check whether to add down-left and/or down-right to the path
	#curP[0] is the row, curP[1] is the column
	if curP[1]==0:
		#compare down and down-right
		next_point_index = minimum(egrid[(curP[0]+1)], egrid[(curP[0]+1)][curP[1]], [curP[1]], curP[1], (curP[1]+2))[0]
	else:
		if curP[1]==(w-1):
			#compare down and down-left
			next_point_index = minimum(egrid[(curP[0]+1)], egrid[(curP[0]+1)][curP[1]-1], [curP[1]-1], (curP[1]-1), (curP[1]+1))[0]
		else:
			#compare down, down-right, and down-left
			next_point_index = minimum(egrid[(curP[0]+1)], egrid[(curP[0]+1)][curP[1]-1], [curP[1]-1], (curP[1]-1), (curP[1]+2))[0]
	#get the next (minimum) point
	next_point = ((curP[0]+1), next_point_index)
	path.append(next_point)
	return vert_path_helper(egrid, w, h, next_point, path, (pathcost+(egrid[(curP[0]+1)][next_point_index])))
	
#-------------------------------------------------------------------------------
#returns the index of the minimum value in a list (or a list if there are mult)
def minimum(lis, mini, mini_indexes, i, stop):
	if i>=stop:
		return mini_indexes
	if lis[i]<mini:
		mini = lis[i]
		mini_indexes = [i]
	else:
		if lis[i]==mini:
			mini_indexes.append(i)
	return minimum(lis, mini, mini_indexes, (i+1), stop)
#-------------------------------------------------------------------------------	
def find_horizontal_path(grid):
	egrid = energy(grid)
	col = column_list(egrid, 0, 0, [])
	#grabs the index(es) of the minimum value in the first row
	minis = minimum(col, egrid[0][0], [], 0, height(egrid))
	paths = []
	for p in minis:
		#paths is a list of tuples (path, pathcost)
		paths.append(hori_path_helper(egrid, width(grid), height(grid), (p, 0), [(p, 0)], 0))
	least = paths[0][1]
	least_index = 0
	indexCount = 0
	#now we find and return the path of least path cost
	for k in paths:
		if indexCount==0:
			indexCount+=1
		else:
			if k[1]<least:
				least = k[1]
				least_index=indexCount
				indexCount+=1
	return paths[least_index][0]

#recursively finds the path
def hori_path_helper(egrid, w, h, curP, path, pathcost):
	if curP[1]>=(w-1):
		#end the recursion
		return (path, pathcost)		
	#next_point_index is the column index of the minimum adjacent point
	next_point_index = 0;
	col = column_list(egrid, (curP[1]+1), 0, [])
	#check whether to add right-up and/or right-down to the path
	#curP[0] is the row, curP[1] is the column
	if curP[0]==0:
		#compare right and down
		next_point_index = minimum(col, egrid[curP[0]][(curP[1]+1)], [curP[0]], curP[0], (curP[0]+2))[0]
	else:
		if curP[0]==(h-1):
			#compare right and up
			next_point_index = minimum(col, egrid[(curP[0]-1)][(curP[1]+1)], [(curP[0]-1)], (curP[0]-1), (curP[0]+1))[0]
		else:
			#compare right, up, and down
			next_point_index = minimum(col, egrid[(curP[0]-1)][(curP[1]+1)], [(curP[0]-1)], (curP[0]-1), (curP[0]+2))[0]
	#get the next (minimum) point
	next_point = (next_point_index, (curP[1]+1))
	path.append(next_point)
	return hori_path_helper(egrid, w, h, next_point, path, (pathcost+(egrid[next_point_index][(curP[1]+1)])))
	
#-------------------------------------------------------------------------------
def column_list(grid, c, curR, lis):
	if curR==height(grid):
		return lis
	lis.append(grid[curR][c])
	return column_list(grid, c, (curR+1), lis)
#-------------------------------------------------------------------------------
def remove_vertical_path(grid, path):
	return rem_vert_helper(grid, path, 0)
	
def rem_vert_helper(grid, path, index):
	if index>=len(path):
		return grid
	#in this case, we don'tworry about countering the grid's shrinkage
	del grid[path[index][0]][path[index][1]]
	return rem_vert_helper(grid, path, (index+1))
	
#-------------------------------------------------------------------------------
def remove_horizontal_path(grid, path):
	#since deleting columns messes with the grid's shape, 
		#we transpose it, turning columns into rows temporarily
	return rem_hori_helper(transpose(grid), path, 0)
	
def rem_hori_helper(grid, path, index):
	if index>=len(path):
		return transpose_back(grid)
	del grid[path[index][1]][path[index][0]]
	return rem_hori_helper(grid, path, (index+1))

#transposes the grid
def transpose(grid):
	newgrid = []
	for i in range(0, width(grid)):
		newgrid.append([])
	for p in grid:
		for k in range(0, width(grid)):
			newgrid[k].append(p[k])
	return newgrid
#restores the grid back to its initial ordering
def transpose_back(grid):
	newgrid = []
	for i in range(0, width(grid)):
		newgrid.append([])
	for p in grid:
		for k in range(0, width(grid)):
			newgrid[k].append(p[k])
	return newgrid
################################################################################
#returns a 
def ppm_to_grid(filename):
	#reading from the file
	someFile = open(filename, 'r')
	storeNum = someFile.read()
	someFile.close()
	#initializing values to be used in making the grid
	sp = storeNum.split()
	width = int(sp[1])
	c = 0
	r = 0
	grid = []
	for i in range(4, len(sp), 3):
		if c==0:	#if we are on a new row...
			grid.append([])
		#adding the new tuple
		grid[r].append((int(sp[i]),int(sp[i+1]),int(sp[i+2])))
		#checking if we need to move on to the next row
		c += 1
		if c==width:
			c = 0
			r += 1
	return grid

def grid_to_ppm(grid, filename):
	someFile = open(filename, 'w')
	someFile.write("P3\n"+str(width(grid))+"\n"+str(height(grid))+"\n255\n")
	for s in grid:
		for sp in s:
			someFile.write(str(sp[0])+"\n")
			someFile.write(str(sp[1])+"\n")
			someFile.write(str(sp[2])+"\n")
	someFile.close()
	
	
	
	
	
	
	
	
	
	
	
