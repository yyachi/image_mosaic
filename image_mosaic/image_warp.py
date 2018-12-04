#!/usr/bin/env python
import os
import sys
import cv2
import time
import math
import yaml
from optparse import OptionParser
from stage import *
from opencv_util import *

def main():
  parser = OptionParser("""usage: %prog [options] imagefile

SYNOPSIS AND USAGE
  python %prog [options] image.jpg

DESCRIPTION
  Create an image file after rotation, magnification, and distortion
  and impose the image into a canvas based on Affine matrix stored in
  imageometry file.

  Note %prog assumes existence of image-info yamlfile for image (=
  imageometry).  When name of an image is `image.jpg', name of the
  imageometry file should be `image.geo'.  Prepare imageometry file in
  advance.  Consider using `vs_attach_image.m', or combination of
  `image-get-affine' and `image-warp-clicks'.

  The image is transformed and imposed to VS space using `image.geo'
  then sub-area of the VS space is exported as `image_.jpg' with
  `image_.geo'.  We refer the image as image-of-VS.  The area of
  image-of-VS to be exported from VS space is specified by option
  `--range'.  Without the option, minimum rectangled-area that surrounds
  the projected image is exported.

EXAMPLE
  CMD> dir
  image.jpg  image.geo
  CMD> image-warp image.jpg -r -50 50 -38.45 38.45 -d 10.24
  ... |image_.jpg| and |image_.geo| were created
  CMD> dir
  image.jpg  image.geo  image_.jpg  image_.geo

SEE ALSO
  vs_attach_image.m
  image-get-affine (renamed from vs-calc-affine)
  image-warp-clicks
  blend-image
  https://github.com/misasa/image_mosaic

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014,2018 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  March 28, 2018: Documentation modified
  May 27, 2015: TK adds documentation
""")
  parser.add_option("-o", "--out", type="string", dest="output_file_path",
            help="name of image-of-VS to be exported", metavar="OUT_PATH")
  parser.add_option("-r", "--range", type="float", nargs=4, dest="stage_range",
            help="area of VS space to be exported as image-of-VS (in micron)", metavar="X_MIN X_MAX Y_MIN Y_MAX")
  parser.add_option("-d", "--density", type="float", dest="pixels_per_um",
            help="resolution of image-of-VS after exported", metavar="PIXEL_PER_MICRON")
  parser.add_option("-s", "--scale", dest="with_scale",
            action="store_true")
  parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose")
  parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose")
  parser.add_option("-w", "--windows",
                    action="store_true", dest="flag_window")

  (options, args) = parser.parse_args()
  x_range = None
  y_range = None
  pixels_per_um = None

  if len(args) != 1:
      parser.error("incorrect number of arguments")

  if options.pixels_per_um != None:
    pixels_per_um = options.pixels_per_um
  else:
    pixels_per_um = 1.0

  if options.stage_range != None:
    x_range = [options.stage_range[0], options.stage_range[1]]
    y_range = [options.stage_range[2], options.stage_range[3]]

  image_path = args[0]
  root, ext = os.path.splitext(image_path)

  default_ofile_name = os.path.basename(root) + '_' + ext
  default_yfile_name = os.path.basename(root) + '.geo'
  warped_yfile_name = os.path.basename(root) + '_.geo'
  target_dir = os.path.dirname(image_path)
  default_ofile_path = os.path.join(target_dir, default_ofile_name)
  default_yfile_path = os.path.join(target_dir, default_yfile_name)
  warped_yfile_path = os.path.join(target_dir, warped_yfile_name)

  if options.output_file_path != None:
    root, ext = os.path.splitext(options.output_file_path)
    target_dir = os.path.dirname(options.output_file_path)

    default_ofile_name = os.path.basename(root) + ext
    warped_yfile_name = os.path.basename(root) + '.geo'
    default_ofile_path = os.path.join(target_dir, default_ofile_name)
    warped_yfile_path = os.path.join(target_dir, warped_yfile_name)


  original_image = cv2.imread(image_path)
  original_height = original_image.shape[0]
  original_width = original_image.shape[1]
  original_aspect = float(original_width) / original_height
#  print "original image: %dx%d (%.3f)" % (original_width, original_height, original_aspect)

  if os.path.isfile(default_yfile_path):
    yf = open(default_yfile_path).read().decode('utf8')
    config = yaml.load(yf)
    if 'affine_xy2vs' in config:
      affine_input = list_to_affine(config['affine_xy2vs'])
      image_rect = [(0,0),(original_width,0),(original_width,original_height),(0,original_height)]
      image_rect_coord = [image_pixel_to_coord(p, original_width, original_height) for p in image_rect]
      image_rect_on_stage = transform_points(image_rect_coord, affine_input)
      affine_image2stage = get_affine_matrix(image_rect, image_rect_on_stage)
      if options.verbose:
        print "Input affine matrix to stage is %s." % (affine_to_str(affine_input))
        print "%s %dx%d pix was calibrated based on %s. It's affine matrix to stage is %s." % (os.path.basename(image_path), original_width, original_height, os.path.basename(default_yfile_name), affine_to_str(affine_input))
    else:
      raise RuntimeError("affine_xy2vs is not found in %s." % default_yfile_path)
  else:
    raise RuntimeError("%s is not found." % default_yfile_path)

  win_view = Stage(image_path, default_ofile_name)
  if x_range != None and y_range != None:
    win_view.set_stage_geometry(x_range = x_range, y_range = y_range)

  win_view.warp_image(affine_image2stage, [500, 500], False)

  if options.with_scale:
    win_view.draw_scale_bar()

  if options.pixels_per_um:
    win_view.resize_image(pixels_per_um,False)
    win_view.save_resized(default_ofile_path)
  else:
    win_view.save_output(default_ofile_path)

  warped_rect_coord = [image_pixel_to_coord(p, win_view.output_size[0], win_view.output_size[1]) for p in win_view.output_rect]
  affine_warped = get_affine_matrix(warped_rect_coord[0:3], win_view.output_rect_on_stage[0:3])

  f = open(warped_yfile_path, 'w')
  yaml.dump({ 'affine_xy2vs': affine_to_list(affine_warped) }, f, encoding='utf8', allow_unicode=True)

  dpi = win_view.output_pixels_per_um * 10000 * 2.54
  if options.verbose:
    print "Calibrated image was saved as %s %dx%d pix. " % (default_ofile_path, win_view.output_image.width, win_view.output_image.height)
    print "Density: %.3f x %.3f dpi" % (dpi, dpi)
    print "Please use the following parameters to place the calibrated image."
    print "Locate:\t(%7.3f, %7.3f) um" % (win_view.output_rect_on_stage[0][0], win_view.output_rect_on_stage[0][1])
    print "Center:\t(%7d, %7d) dot" % (0, 0)
    print "Size:\t(%7.3f, %7.3f) um" % (win_view.stage_width, win_view.stage_height)

  if options.flag_window:
    print "activate %s window and type escape to terminate." % (win_view.window_name)

    while True:
      cv2.imshow(win_view.window_name, win_view.temp)
      if cv2.waitKey(15) == 27: break

if __name__ == '__main__':
  main()