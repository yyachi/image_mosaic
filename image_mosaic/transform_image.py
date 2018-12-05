#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
import yaml
import cv2
from optparse import OptionParser
#sys.path.append(os.path.join(os.path.dirname(__file__),'../lib'))
from image_mosaic.opencv_util import *

def main():
  usage = textwrap.dedent('''\
 %prog [options] imagefile

SYNOPSIS AND USAGE
  %prog [options] imagefile

DESCRIPTION
  This command is subset of warp_image. The area to be exported
  is set by width and height of the original image.

EXAMPLE
  > %prog --scale 0.6 --center [100,50] --angle=-50.0 imagefile

SEE ALSO
  warp_image
  https://github.com/misasa/image_mosaic

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  August 11, 2015: Add documentation
''')
  parser = OptionParser(usage)
  parser.add_option("-o", "--output-file", type="string", dest="output_path",
            help="output file", metavar="OUTPUT_FILE")
  parser.add_option("-a", "--angle", type="float", default =0.0, dest="angle",
            help="0 <= angle < 360 [default: %default]", metavar="ANGLE")   
  parser.add_option("-s", "--scale", type="float", default =1.0, dest="scale",
            help="0 < scale <= 1.0 [default: %default]", metavar="SCALE") 
  parser.add_option("-c", "--center", type="string", dest="center",
            help="center of rotation", metavar="CENTER")
  parser.add_option("-m", "--matrix", type='string', dest="matrix",
            help="affine matrix: [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]")              
  parser.add_option("-f", "--output-format", type="choice", default ='text', choices = ['text', 'yaml'], dest="output_format",
            help="output format: 'text' or 'yaml' [default: %default]", metavar="OUTPUT_FORMAT")

  (options, args) = parser.parse_args()

  if len(args) != 1:
       parser.error("incorrect number of arguments")

  image_path = args[0]
  root, ext = os.path.splitext(image_path)
  default_ofile_name = os.path.basename(root) + '_transformed' + ext
  curdir = os.getcwd()
  default_ofile_path = os.path.join(curdir, default_ofile_name)

  output_path = default_ofile_path

  if options.output_path != None:
    output_path = options.output_path


  img = cv2.imread(image_path)
  height = img.shape[0]
  width = img.shape[1]

  if options.matrix != None:
    h = str2array(options.matrix)
    img2 = cv2.warpPerspective(img, h, (width, height))
  else:
    scale = options.scale
    angle = options.angle
    center = numpy.array([0.0, 0.0], dtype=numpy.float32)
    if options.center != None:
      center = str2array(options.center)
    h = cv2.getRotationMatrix2D(tuple(center), angle, scale)
    img2 = cv2.warpAffine(img, h, (width, height))

  # cv2.imshow('image', img2)
  # cv2.waitKey(0)

  cv2.imwrite(output_path, img2)


if __name__ == '__main__':
  main()
