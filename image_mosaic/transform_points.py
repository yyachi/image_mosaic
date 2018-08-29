#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
import yaml
import cv2
import math
from optparse import OptionParser
#sys.path.append(os.path.join(os.path.dirname(__file__),'../lib'))
from opencv_util import *

def main():
	usage = textwrap.dedent('''\
 %prog [options] points
  # Hint
  # > %prog --scale 0.6 --center [100,50] --angle=-50.0 [[0,0],[100,100]]
  # > %prog --matrix=[[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]] [[0,0],[100,100]]

SYNOPSIS AND USAGE
  %prog [options] points

DESCRIPTION

EXAMPLE

SEE ALSO
  http://dream.misasa.okayama-u.ac.jp

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  August 11, 2015: Add documentation
''')

	parser = OptionParser(usage)
	parser.add_option("-a", "--angle", type="float", default =0.0, dest="angle",
	 				  help="0 <= angle < 360 [default: %default]", metavar="ANGLE")		
	parser.add_option("-s", "--scale", type="float", default =1.0, dest="scale",
	 				  help="0 < scale <= 1.0 [default: %default]", metavar="SCALE")	
	parser.add_option("-c", "--center", type="string", dest="center",
	 				  help="center of rotation", metavar="CENTER")
	parser.add_option("-t", "--offset", type="string", dest="offset",
	 				  help="offset vector", metavar="SHIFT")	
	parser.add_option("-m", "--matrix", type='string', dest="matrix",
					  help="affine matrix: [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]") 				  		
	parser.add_option("-f", "--output-format", type="choice", default ='text', choices = ['text', 'yaml'], dest="output_format",
	 				  help="output format: 'text' or 'yaml' [default: %default]", metavar="OUTPUT_FORMAT")

	(options, args) = parser.parse_args()

	if len(args) != 1:
	     parser.error("incorrect number of arguments")

	src = str2array(args[0])

	if options.matrix != None:
		h = str2array(options.matrix)
		a = numpy.array([src])
		dst = cv2.perspectiveTransform(a, h)
		dst = dst[0]
	else:
		a = numpy.array([src])
		scale = options.scale
		angle = options.angle
		center = numpy.array([0.0, 0.0], dtype=numpy.float32)
		if options.offset != None:
			offset = str2array(options.offset)
			h = getRotationOffsetMatrix2D(tuple(offset), angle, scale)
		else:
			if options.center != None:
				center = str2array(options.center)
			h = cv2.getRotationMatrix2D(tuple(center), angle, scale)

		dst = cv2.transform(a, h)
		dst = dst[0]


	if options.output_format == 'text':
		print array2str(dst)
	elif options.output_format == 'yaml':
		print yaml.dump(dst.tolist(), encoding='utf8', allow_unicode=True)


if __name__ == '__main__':
	main()
