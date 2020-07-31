#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
 %prog from_points to_points

SYNOPSIS AND USAGE
  %prog [options] from_points to_points

DESCRIPTION
Return Affine matrix calculated from four
pairs of coordinates. Coordinates should be
fed by arguments.


EXAMPLE
  > %prog [[100,50],[100,0],[0,0],[0,50]] [[-50,100],[0,100],[0,0],[-50,0]]

SEE ALSO
  https://github.com/misasa/image_mosaic
  https://github.com/misasa/image_mosaic/blob/master/image_mosaic/H_from_points.py

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014-2020 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  August 11, 2015: Add documentation
''')
  parser = OptionParser(usage)
  parser.add_option("-f", "--output-format", type="choice", default ='text', choices = ['text', 'yaml'], dest="output_format",
    help="output format: 'text' or 'yaml' [default: %default]", metavar="OUTPUT_FORMAT")

  (options, args) = parser.parse_args()
  if len(args) != 2:
       parser.error("incorrect number of arguments")

  src = str2array(args[0])
  dst = str2array(args[1])

  num_points,n = src.shape

  if num_points < 4:
    parser.error("requires at least 4 points")

  if src.shape != dst.shape:
    raise RuntimeError('number of points do not match')

  h = cv2.getPerspectiveTransform(src,dst)

  if options.output_format == 'text':
    print(array2str(h))
  elif options.output_format == 'yaml':
    print(yaml.dump(h.tolist(), encoding='utf8', allow_unicode=True).decode())

if __name__ == '__main__':
  main()
