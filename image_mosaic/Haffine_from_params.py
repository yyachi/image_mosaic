#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
import yaml
import cv2
from optparse import OptionParser
from image_mosaic.util import *

def main():
  usage = textwrap.dedent('''\
 %prog [options]

SYNOPSIS AND USAGE
  %prog [options]

DESCRIPTION
  Return Affine matrix calculated from center of rotation
  in original image, rotation angle, and magnification.
  Parameters should be fed by arguments.

EXAMPLE
  > %prog --scale 0.6 --center [100,50] --angle=-50.0

SEE ALSO
  https://github.com/misasa/image_mosaic
  https://github.com/misasa/image_mosaic/blob/master/image_mosaic/Haffine_from_params.py

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014-2020 Okayama University
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
  parser.add_option("-f", "--output-format", type="choice", default ='text', choices = ['text', 'yaml'], dest="output_format",
    help="output format: 'text' or 'yaml' [default: %default]", metavar="OUTPUT_FORMAT")

  (options, args) = parser.parse_args()

  scale = options.scale
  angle = options.angle
  center = numpy.array([0.0, 0.0], dtype=numpy.float32)
  if options.center != None:
    center = str2array(options.center)
  h = cv2.getRotationMatrix2D(tuple(center), angle, scale)

  h = numpy.append(h, numpy.array([0.0,0.0,1.0])).reshape(3,3)
  if options.output_format == 'text':
    print(array2str(h))
  elif options.output_format == 'yaml':
    print(yaml.dump(h.tolist(), encoding='utf8', allow_unicode=True).decode())

if __name__ == '__main__':
  main()
