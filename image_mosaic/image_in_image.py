#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
import yaml
import scipy
import cv2
from optparse import OptionParser
#from opencv_util import *

def main():
  usage = textwrap.dedent('''\
 %prog image1 image2 corner_of_image1_on_image2([upper_left,upper_right,lower_right,lower_left])

SYNOPSIS AND USAGE
  %prog image1 image2 corner_of_image1_on_image2([upper_left,upper_right,lower_right,lower_left])

DESCRIPTION
  Impose an image on wall image after Affine transformation. Affine matrix affine_ij2ij
  is specified by coordinates where the 4 corners of the original image are projected. 
  This command is subset of warp_image.

EXAMPLE
  > %prog data/cat.jpg data/billboad_for_rent.jpg [[40,264],[605,264],[605,540],[36,538]]
  > %prog data/cat.jpg data/billboad_for_rent.jpg [[55,675],[277,677],[281,826],[52,826]]

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

  (options, args) = parser.parse_args()

  if len(args) != 3:
    parser.error("incorrect number of arguments")

  image_path1 = args[0]
  image_path2 = args[1]
# corner_points = str2array(args[2])
        corner_points = numpy.array(eval(args[2]), dtype=numpy.float32)

  root1, ext1 = os.path.splitext(image_path1)
  root2, ext2 = os.path.splitext(image_path2)

  default_ofile_name = os.path.basename(root1) + '_on_' + os.path.basename(root2) + ext1
  curdir = os.getcwd()
  default_ofile_path = os.path.join(curdir, default_ofile_name)

  output_path = default_ofile_path

  if options.output_path != None:
    output_path = options.output_path

  
  tp = numpy.array([[p[1] for p in corner_points], [p[0] for p in corner_points], [1.0 for p in corner_points] ])

  if os.path.exists(image_path1) == False:
    parser.error("%s does not exist" % image_path1)
  else:     
    img1 = cv2.imread(image_path1)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    height1 = img1.shape[0]
    width1 = img1.shape[1]


  if os.path.exists(image_path2) == False:
    parser.error("%s does not exist" % image_path2)
  else:     
    img2 = cv2.imread(image_path2)
    height2 = img2.shape[0]
    width2 = img2.shape[1]

  src = numpy.array([[0,0],[width1,0],[width1,height1],[0,height1]], dtype = numpy.float32)
  dst = corner_points
  h = cv2.getPerspectiveTransform(src,dst)

  img1_gray = cv2.warpPerspective(img1_gray, h, (width2, height2))
  img1_gray = cv2.add(img1_gray, 1)
  (thresh, mask) = cv2.threshold(img1_gray, 1, 255, cv2.THRESH_BINARY_INV)

  img3 = cv2.warpPerspective(img1, h, (width2, height2))
  cv2.add(img2, img3, img3, mask)

  cv2.imwrite(output_path, img3)
  # cv2.imshow('image', img3)
  # cv2.waitKey(0)  

if __name__ == '__main__':
  main()
