#!/usr/bin/env python
import sys
import os
from optparse import OptionParser
import cv2

def main():
  parser = OptionParser("""usage: %prog [options] imagefile0 imagefile1 x y width height alpha beta

SYNOPSIS AND USAGE
  python %prog [options] imagefile0 imagefile1 x y width height alpha beta

DESCRIPTION
  Blend two images using alphablend technique.  You impose imagefile1
  to imagefile0.  Specify where to locate imagefile1 by (x, y) of
  imagefile0 and dimension of imagefile1 by (width, height).  Rotate
  and distort imagefile1 in advance using `image-warp'.  Specify alpha
  and beta by 7th and 8th arguments.

  Typically, beta = 1 - alpha.

EXAMPLE
  $ ls
  mywall.jpg  raman.jpg  raman_.jpg
  $ %prog mywall.jpg raman_.jpg 0 0 1024 788 0.4 0.6

SEE ALSO
  image-warp
  https://github.com/misasa/image_mosaic
  https://github.com/misasa/image_mosaic/blob/master/image_mosaic/blend_image.py

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014-2020 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  May 25, 2015: TK adds documentation
""")
  parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="make lots of noise")
  parser.add_option("-o", "--out", type="string", dest="output_path",
            help="set output file", metavar="OUTPUT_FILE_PATH")


  (options, args) = parser.parse_args()
  if len(args) != 8:
    parser.error("incorrect number of arguments")
  src1_path = args[0]
  src2_path = args[1]

  root_1, ext = os.path.splitext(src1_path)
  root_2, ext = os.path.splitext(src2_path)

  default_ofile_name = os.path.basename(root_2) + '-on-' + os.path.basename(root_1) + ext
  target_dir = os.path.dirname(root_1)
  default_ofile_path = os.path.join(target_dir, default_ofile_name)

  output_path = default_ofile_path
  if options.output_path != None:
    output_path = options.output_path

  x = int(args[2])
  y = int(args[3])
  width = int(args[4])
  height = int(args[5])
  alpha = float(args[6])
  beta = float(args[7])

  #src1 = cv.LoadImage(src1_path, cv.CV_LOAD_IMAGE_UNCHANGED)
  src1 = cv2.imread(src1_path)
  #src2 = cv.LoadImage(src2_path, cv.CV_LOAD_IMAGE_UNCHANGED)
  src2 = cv2.imread(src2_path)
  #cv.SetImageROI(src1, (x, y, width, height))
  #cv.SetImageROI(src2, (0, 0, width, height))
  #cv.AddWeighted(src1, alpha, src2, beta, 0.0, src1)
  #cv.ResetImageROI(src1)
  roi1 = src1[y:y+height, x:x+width]
  roi2 = src2[0:height,0:width]
  dst = cv2.addWeighted(roi1, alpha, roi2, beta, 0.0)
  src1[y:y+height,x:x+width] = dst
  #cv.SaveImage(output_path, src1)
  cv2.imwrite(output_path, src1)

if __name__ == '__main__':
  main()
