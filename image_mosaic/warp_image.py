#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
import yaml
import cv2
from optparse import OptionParser
from image_mosaic.opencv_util import *

def main():
  usage = textwrap.dedent('''\
 %prog [options] imagefile

SYNOPSIS AND USAGE
  %prog [options] imagefile

DESCRIPTION
  Transform an image using Affine matrix affine_ij2ij and export image.
  Affine matrix can be specified by (1) 3x3 matrix, (2) center of rotation
  in original image, rotation angle, and magnification as similar to
  haffine_from_params, and (3) coordinates where the 4 corners of the original
  image are projected. The area to be exported can be specified by width and
  height via arguments. Without width and height specified, those of the
  original image would be applied. This program also imposes the original image
  on wall image. In this case, the area to be exported is set by width and height
  of the wall image.

EXAMPLE
  > %prog --scale 0.6 --center [100,50] --angle=-50.0 imagefile

SEE ALSO
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
  parser.add_option("-b", "--background-image", type="string", dest="bg_image",
    help="background image file", metavar="BG_IMAGE") 
  parser.add_option("-g", "--geometry", type="string", dest="geometry",
    help="geometry of output [default: same as input image]", metavar="GEOMETRY")
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
  parser.add_option("-n", "--corners", type='string', dest="corner_points",
    help="corner points on destination [upper_left,upper_right,lower_right,lower_left]: [[55,675],[277,677],[281,826],[52,826]]")                 
  parser.add_option("-f", "--output-format", type="choice", default ='text', choices = ['text', 'yaml'], dest="output_format",
    help="output format: 'text' or 'yaml' [default: %default]", metavar="OUTPUT_FORMAT")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.error("incorrect number of arguments")

  image_path = args[0]
  root, ext = os.path.splitext(image_path)
  default_ofile_name = os.path.basename(root) + '_warped' + ext
  curdir = os.getcwd()
  default_ofile_path = os.path.join(curdir, default_ofile_name)

  output_path = default_ofile_path

  if options.output_path != None:
    output_path = options.output_path

  if os.path.exists(image_path) == False:
    parser.error("%s does not exist" % image_path)
  else:
    img = cv2.imread(image_path)
    height = img.shape[0]
    width = img.shape[1]


  if options.matrix != None:
    h = str2array(options.matrix)
  elif options.corner_points != None:
    dst = str2array(options.corner_points)
    src = numpy.array([[0,0],[width,0],[width,height],[0,height]], dtype = numpy.float32)
    h = cv2.getPerspectiveTransform(src,dst)    
  else:
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
    h = numpy.append(h, numpy.array([0.0,0.0,1.0])).reshape(3,3)


  if options.bg_image == None:
    output_geometry = (width, height)
    if options.geometry != None:
      output_geometry = tuple(list(str2array(options.geometry)))
    img2 = cv2.warpPerspective(img, h, output_geometry) 
  else: 
    if os.path.exists(options.bg_image) == False:
      parser.error("%s does not exist" % options.bg_image)
    else:
      bg_img = cv2.imread(options.bg_image)
      bg_height = bg_img.shape[0]
      bg_width = bg_img.shape[1]
      output_geometry = (bg_width, bg_height)

      img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      img_gray = cv2.warpPerspective(img_gray, h, output_geometry)
      img_gray = cv2.add(img_gray, 1)
      (thresh, mask) = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY_INV)
      img2 = cv2.warpPerspective(img, h, output_geometry)
      cv2.add(bg_img, img2, img2, mask)
  cv2.imwrite(output_path, img2)

if __name__ == '__main__':
  main()  
