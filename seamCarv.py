import sys, random, numpy, math # IMPORTANT: numPy must be installed on target computer
numpy.set_printoptions(threshold='nan') # debug - enable display full numpy array in console

'''
Tyler Wengerd
tlw56@zips.uakron.edu
Project 3 - seam carving
Algorithms
University of Akron
Spring 2014
'''

# global variables
filename = ""
numArgs = len(sys.argv) - 1 # get number of arguments passed
seamCoords = []

# Functions

''' parsePGM 
    turns a PGM file into a numpy 2d array
    inputs:        filepath
    outputs:    2d array representing the pgm file
                maxVal of PGM file (integer representing white)
'''
def parsePGM(fn):
    # parsing header
    words = [] # we're looking for four words: P2, width, height, maxval
    activeFile = open(fn, 'r')
    for line in activeFile:
        for word in line.split():
            if word == "#": # this line is a comment - or something's not right
                break # skip this line
            else:
                words.append(word)
    if words[0] != "P2":
        print "Error: Bad header (P2 not found)"
    wPGM = int(words[1]) # width
    hPGM = int(words[2]) # height
    maxGrey = int(words[3]) # max value (white)
    rawData = [int(thing) for thing in words[4:]]
    pgmArray = numpy.array(rawData).reshape(hPGM, wPGM)
    activeFile.close()
    return pgmArray, maxGrey
    
''' calcSeam 
    calculates the lowest energy seam based on the specs given in the project documentation
    this calculates vertical seams. for horizontal seams, the array is transposed beforehand, so this doesn't have to make any differentiation.
    inputs:        2d numpy array
    outputs:    array of coordinates [i,j] of pixels in the seam
'''
def calcSeam(pgmArray):
    rows, columns = pgmArray.shape # numPy shape function returns 2d array size as [height, width]
    energy = numpy.zeros((rows, columns), dtype=int) # this is our cumulative min energy matrix
    maxRow = rows-1
    maxCol = columns-1
    seamCoords[:] = []

    # # # top row cases # # #
    # upper left: use right and lower pixels
    energy[0, 0] = abs(pgmArray[0,0] - pgmArray[0, 1]) + abs(pgmArray[0,0] - pgmArray[1, 0])
    # upper right: use left and lower pixels
    energy[0, -1] = abs(pgmArray[0, -1] - pgmArray[0, -2]) + abs(pgmArray[0, -1] - pgmArray[1, -1])
        # top edge: use left, right, and lower pixels
    i = 0 # top row
    for j in range(1, columns-1): # we don't want final column as that's part of corner
        energy[i, j] = abs(pgmArray[i, j] - pgmArray[i, j-1]) + abs(pgmArray[i, j] - pgmArray[i, j+1]) + abs(pgmArray[i, j] - pgmArray[i+1, j])

    # now we start calculating the rest of the energy and finding min energy seam
    # using mins as a list of choices for min that we get while calculating energy, and choose from afterwards
    for i in range(1, rows):
        for j in range(columns):
              # always an above row
            energy[i, j] =  abs(pgmArray[i, j] - pgmArray[i-1, j])
            mins = [energy[i-1, j]]
            # check below - min not needed here
            if i != maxRow:
                energy[i,j] += abs(pgmArray[i, j] - pgmArray[i+1, j]) # add to energy
            # check for left
            if j != 0:
                energy[i,j] += abs(pgmArray[i, j] - pgmArray[i, j-1]) # add to energy
                mins.append(energy[i-1, j-1]) # add upper left pixel energy to min choices
            # check for right
            if j != maxCol:
                energy[i,j] += abs(pgmArray[i, j] - pgmArray[i, j+1]) # add to energy
                mins.append(energy[i-1, j+1]) # add upper right pixel energy to min choices

            # now M(i,j) = e(i,j)
            # making it M(i,j) = e(i,j) + min(M(i,j)):
            energy[i,j] += min(mins)
            mins[:] = [] # clears mins array - I like to do this because sometimes array values seem to stick around when using loops

    # now we start from end and get pixel coordinates
    j = numpy.argmin(energy[maxRow]) # returns column index of minimum value in last row (leftmost one in case of tie)
    seamCoords.append([maxRow, j]) # first pixel coordinate of seam 
        
    ''' I just tried to figure out what this did a couple days after writing it and it was still hard to decypher, so here's more info:

            prevj is the j-coordinate of the latest pixel in the seam that we know of (last entry in seamCoords)
            since we're moving up the table based only on the i (row) in the for loop, we need to keep track of which column we're in
            once we determine the column, we get the energies of the upper 2 or 3 pixels and find the one with the minimum energy
            there's an array called pixAbove which has the three values of the pixels above_left, above_right, and above the last pixel in seamCoords
            if we're on a boundary we use sys.maxint for the value of the missing pixel
            then we find the minimum energy in pixAbove and add its index-1 (resulting in -1, 0, or +1) to the j of the latest pixel in seamCoords to get the j of the next pixel to add to seamCoord
            the i for the next pixel to add is the i of the loop we're in.
    '''
    for i in reversed(range(maxRow)): # start from second to last row since we just did the last one
        # pixAbove is an array of upper left, upper, and upper right pixel energies relative to the current pixel in the seam
        prevj = seamCoords[-1][1] # gets previous j coordinate
        if prevj == 0: # left column
            pixAbove = [sys.maxint, energy[i, prevj], energy[i, prevj+1]] # options added to seam are [MAX, value(above), value(above_right)]
        elif prevj == maxCol: # right column
            pixAbove = [energy[i, prevj-1], energy[i,prevj], sys.maxint] # options value added to seam are [value(above_left), value(above), MAX]
        else: # in between
            pixAbove = [energy[i, prevj-1], energy[i,prevj], energy[i, prevj+1]] # options value added to seam are [value(above_left), value(above), value(above_right)]

        # make new j relative to previous j, using min indexed value from energy of pixels above
        j = prevj + pixAbove.index(min(pixAbove)) - 1 # pixAbove.index(..) gives 0, 1, or 2 - we add this (-1) to  j to let us know if the best pixel for this row is to the left, right, or neither
        # note - have to offset by one so upper left is 0-1 = prevj - 1; also note that this will favor upper left 
   
            # so we then add that i,j coordinate set to the list of seam pixel coordinates and repeat
        seamCoords.append([i,j]) # add new pixel to the list of seam coords 
        pixAbove[:] = [] # just in case
    # 
    # a haiku:
    # when this for loop ends
    # we'll have our vertical seam
    # now I'm off to bed
    return seamCoords

''' removeSeam 
    deletes a seam from a 2d array
    inputs:        2d array, list of coordinates of pixels to remove
    outputs:    2d array with pixels removed
'''
def removeSeam(inPGM, pixelCoords):
    outPGM = numpy.copy(inPGM)
    seamMask = numpy.ones(len(inPGM.flat), dtype=bool).reshape(inPGM.shape) # boolean matrix the size of the input pgm, we will mark pixels to be deleted as false
    for pixel in pixelCoords: # create boolean mask
        i, j = pixel[0], pixel[1]
        seamMask[i, j] = False # [i,j] = pixel to be removed

    # inPGM[seamMask] removes all entries that have false at that same spot on the inPGM matrix.
    # That flattens the matrix (into 1d) because numpy can't just refigure the matrix dimensions
    # so if we removed a vertical seam we need to reshape the new, flat matrix, saying the height is the same and the width is 1 column less than the old matrix
    # inPGM.shape returns the list [height, width]
    outPGM = inPGM[seamMask].reshape(inPGM.shape[0], inPGM.shape[1]-1) 
    return outPGM

''' makeNewPGM 
    writes a PGM file based on an input 2d array
    inputs:        name of new file, height of PGM, width of PGM, maxvalof PGM, and PGM data in a 2d array
    outputs:    none
'''
def makeNewPGM(fName, hMaker, wMaker, maxval, pgmIn):
    newFile = open(fName, 'w+')
    newFile.write("P2\n")
    newFile.write("# Created by Tyler Wengerd\n")
    newFile.write(str(wMaker) + " " + str(hMaker) + "\n") # pgm spec says width first
    newFile.write(str(maxval) + "\n")
    maxW = 24 # for readability
    counter = 0
    for pixel in pgmIn.flat:
        newFile.write(str(pixel) + "\t")
        counter += 1
        if counter == maxW:
            newFile.write("\n")
            counter = 0
    newFile.close()

#end functions

#parsing input
if numArgs == 3:
    filename = str(sys.argv[1])
    vRemove = int(sys.argv[2]) # number of vertical seams to remove
    hRemove = int(sys.argv[3]) # number of horizontal seams to remove

    newFilename = filename[:-4] + "_processed.pgm" # negative indexing is so good - this removes the .pgm from the end of the filename and we add "_processed.pgm" to it
    currentPGM, white = parsePGM(filename) # get PGM data
    total = vRemove + hRemove # for percentage showing
    for vCount in range(vRemove):
        seamCoordinates = calcSeam(currentPGM) # returns array of coordinates of pixels in seam
        newPGM = removeSeam(currentPGM, seamCoordinates) # new data for PGM
        currentPGM = newPGM
        # The following print command may not work on computers with Python v3.X.
        # It is not essential to the program operation, so feel free to comment it out if the program is not working on a system with python 3.
        print str(int(round((float(vCount)/total)*100, 0))) + "%\r", # display percentage. Apparently in python 3 this bit with the comma might not work.

    currentPGM = numpy.transpose(currentPGM) # for horizonal seam removal we just transpose the PGM matrix, process it as if it were a vertical removal, and transpose it back.
    for hCount in range(hRemove):
        seamCoordinates = calcSeam(currentPGM) # returns array of coordinates of pixels in seam
        newPGM = removeSeam(currentPGM, seamCoordinates) # new data for PGM
        currentPGM = newPGM
        # The following print command may not work on computers with Python v3.X.
        # It is not essential to the program operation, so feel free to comment it out if the program is not working on a system with python 3.
        print str(int(round((float(hCount+1+vRemove)/total)*100, 0))) + "%\r", # same thing - might not work in python 3.
    currentPGM = numpy.transpose(currentPGM) # works even if we didn't do any horizontals because we have now transposed it twice.

    hei, wid = currentPGM.shape[0], currentPGM.shape[1] # we need to pass the size of the new pgm into the ..._processed.pgm file 
    makeNewPGM(newFilename, hei, wid, white, currentPGM) # do it

else:
    print "Error: Need three inputs (filename, numVerticalSeams, numHorizontalSeams)"