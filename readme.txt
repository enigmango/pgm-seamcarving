#####################################
# Tyler Wengerd						#
# tlw56@zips.uakron.edu				#
# Project 3 - Seam Carving			#
# Algorithms						#
# University of Akron				#
# Spring 2014						#
# README for seamCarv.py			#
#####################################

# # Program meta-details # #

This program is written in Python v2.7.6.
I'm using 2.7.6 because of a senior project device that only works with 2.7.6.

REQUIREMENTS:	1. NumPy (http://www.numpy.org/)
				This programs uses the NumPy library to handle 2d arrays, so NumPy *must* be installed on the running computer
				SciPy is not needed
			
				2.	Python v 2.7.6 or greater - see note about v3 below.
				Python 3.X may not work with this program due to the print commands used on lines 188 and 197. I haven't tried, so it may work.
				If the print statements don't work, you may comment them out.
				All they do is display the completion percentage on the command line.

# # Basic program operation # #

To run this program, you must have python and numPy installed.
You should be able to run the script by doing the following:
	1. Open a command prompt
	2. Browse to the directory containing the python script
	3. Type seamCarv.py {parameters}
	4. The new PGM file will be saved as (oldfilename)_processed.pgm

If the above does not work in Linux/Mac, try typing "python ./seamCarv.py {parameters}" at the command line instead.


# # Notes/Limitations # #

NOTE -1: The PGM file for the 68, 211 test case on the evaluation sheet is named .._211_68.pgm and appears to have 211 vertical seams and 68 horizontal seams removed. A test case of this program running seamCarv.py twoBalls.pgm 211 68 returns an identical result.

NOTE 0: This program takes some time on large PGM files. Analysis shows this is mainly due to having to go through the full 2d array (thanks dynamic programming) and the abs() function.

NOTE 1: The new (processed) file will be saved in the same directory as the original PGM file, which may not be in the same directory as the python script.

NOTE 2: The filename can contain path characters, and thus allows any file path to be used (e.g. the full command can be "seamCarv.py ..\..\pictures\myPGMFiles\cosmo.pgm 10 20"

NOTE 3: When the program selects the minimum pixel energy, part of this operation involves the min() function. 
	On ties, min() selects the item with the lowest index. 
	This may result in slightly different seams selected than programs in different languages, or even in python with a different min energy selection method.

NOTE 4: I watched *so much* Seinfeld while writing this program

# # Specific program operation # # 

This program accepts various parameters as specified in the project requirements, detailed below with notes:

seamCarv.py fname.pgm v h	// Saves a file fname_processed.pgm to the same directory as fname.pgm. See notes above for filename information. 
	Notes - v = vertical seams to be removed
			h = horizontal seams to be removed
			This program can take a long time when processing large PGM files. A percentage of completion is shown on the command line for your convenience and peace of mind.

-Tyler