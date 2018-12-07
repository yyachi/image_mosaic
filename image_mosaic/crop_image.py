#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
import yaml
import re
import cv2
from optparse import OptionParser
from image_mosaic.util import *

def main():
  usage = textwrap.dedent('''\
 %prog [options] imagefile

SYNOPSIS AND USAGE
  %prog [options] imagefile

DESCRIPTION
  Crop a rectangular region of an image.
EXAMPLE
  > %prog --geometery 600x400+40+28 data/cat.jpg

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
  parser.add_option("-g", "--geometry", type="string", dest="geometry",
    help="cut out a rectangular region of the image: 1280x640+10+10", metavar="GEOMETRY")

  (options, args) = parser.parse_args()

  if len(args) != 1:
    parser.error("incorrect number of arguments")

  image_path = args[0]

  if not os.path.isfile(image_path):
    parser.error(image_path + " does not exist")

  root, ext = os.path.splitext(image_path)
  default_ofile_name = os.path.basename(root) + '_cropped' + ext
  curdir = os.getcwd()
  default_ofile_path = os.path.join(curdir, default_ofile_name)

  output_path = default_ofile_path

  if options.output_path != None:
    output_path = options.output_path

  img = cv2.imread(image_path)
  height = img.shape[0]
  width = img.shape[1]
  crop_w = width
  crop_h = height
  crop_x = 0
  crop_y = 0
  if options.geometry != None:
    r = re.compile("([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)")
    m = r.search(options.geometry)
    crop_w = int(m.group(1))
    crop_h = int(m.group(2))
    crop_x = int(m.group(3))
    crop_y = int(m.group(4))

  img2 = img[crop_y:(crop_y + crop_h), crop_x:(crop_x + crop_w)]

  cv2.imwrite(output_path, img2)

if __name__ == '__main__':
  main()
