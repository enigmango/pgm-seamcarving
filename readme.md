# Description

This is an image resizing program written in Python. The original program was written for a seam carving project as part of an algorithms class at the University of Akron. 
It uses the [seam carving](http://en.wikipedia.org/wiki/Seam_carving) algorithm to resize with minimal distortion.

Tested and working with Python 3.4.2 on ArchLinux.

Feel free to use as you please. Pull requests welcome. 

*This is part of an ongoing project to put some of my old school projects on GitHub - the going will be slow, as I have to go through backups and recovered files.*

#Requirements	
* [NumPy](http://www.numpy.org/)
	* This programs uses the NumPy library to handle 2d arrays, so NumPy *must* be installed on the running computer. (SciPy is not needed)

#Operation

`python ./seamCarv.py path/to/file V H`

...Where *V* is the number of vertical seams to remove, and *H* is the number of horizontal seams to remove.

The new PGM file will be saved as (oldfilename)_processed.pgm in the same directory as the original file.

A percentage of completion is shown on the command line for your convenience and peace of mind.

##Example
`./seamcarv.py cosmo.pgm 100 50` on a 1000x1000 image named `cosmo.pgm` will save a 900x950 image named `cosmo_processed.pgm`.


#Notes/Limitations

* This currently only works with black & white PGM files.
* Large PGM files take some time to process. Analysis shows this is mainly due to having to go through the full 2d array (thanks dynamic programming) and the abs() function.
* The filename can contain path characters (e.g. the full command can be "seamCarv.py ..\..\pictures\myPGMFiles\cosmo.pgm 10 20")
*  When the program selects the minimum pixel energy, part of this operation involves the min() function. 
	* On ties, min() selects the item with the lowest index. 
	* This may result in slightly different seams selected than programs in different languages, or even in python with a different min energy selection method.
* I watched *so much* Seinfeld while writing this program
* Two (public domain) images have been included in tis repo, with examples of vertical and horizontal resizing for both.
