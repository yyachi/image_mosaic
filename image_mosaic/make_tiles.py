#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
import yaml
import scipy
from PIL import Image, ImageChops
#import cv2
from optparse import OptionParser
#from opencv_util import *

def make_tiles(zoom, img, dirname, options):
  dirname = os.path.join(dirname,str(zoom))
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  
  ibox = options.ibox
  tilesize = options.tilesize
  length = options.length
  box = options.bbox
  n = 2**zoom
  #print "zoom:%d (%d) tiles" % (zoom, n)
  #print ibox
  #print box
  pix = tilesize * n
  length_per_pix = length/float(pix)
  dum = length_per_pix*tilesize
  #print length
  #print pix
  #print length_per_pix
  #print dum

  for i in range(n):
    for j in range(n):
      #tile_path = os.path.join(dirname,"%d-%d.png",i,j)
      tile_path = os.path.join(dirname,"%d_%d.png" % (i,j))
      tile = Image.new('RGBA', (tilesize, tilesize), (0,0,0,0))
      
      pbox = (tilesize*i, tilesize*j, tilesize*(i+1), tilesize*(j+1))
      zleft = box[0] + dum*i
      zright = zleft + dum
      zupper = box[1] - dum*j
      zlower = zupper - dum
      ppbox = (zleft, zupper, zright, zlower)
      cbox = [0,0,0,0]
      if (ibox[0] >= zleft and ibox[0] <= zright):
        cbox[0] = ibox[0]
      else:
        cbox[0] = zleft
      if (ibox[1] <= zupper and ibox[1] >= zlower):
        cbox[1] = ibox[1]
      else:
        cbox[1] = zupper
      if (ibox[2] >= zleft and ibox[2] <= zright):
        cbox[2] = ibox[2]
      else:
        cbox[2] = zright
      if (ibox[3] <= zupper and ibox[3] >= zlower):
        cbox[3] = ibox[3]
      else:
        cbox[3] = zlower
      cb = box_r(cbox,ppbox)
      tb = box_r(cbox,ibox)
      #print (i,j), "pixs:", pbox, "world:", ppbox
      invalids = [r for r in tb if r < 0 or r > 1]
      if len(invalids) == 0:
        img_width, img_height = img.size
        roi_in_tile = (int(cb[0]*tilesize),int(cb[1]*tilesize),int(cb[2]*tilesize),int(cb[3]*tilesize))
        roi_in_image = (int(tb[0]*img_width),int(tb[1]*img_height),int(tb[2]*img_width),int(tb[3]*img_height))
        #print "crop", roi_in_image
        rsize = (roi_in_tile[2] - roi_in_tile[0], roi_in_tile[3] - roi_in_tile[1])
        #print "resize", rsize
        #print "paste", roi_in_tile
        try:
          part = img.crop(roi_in_image)
          part = part.resize(rsize)
          tile.paste(part, roi_in_tile)
        except:
          print("failed to generate %s" % tile_path)
        #print "tile", cbox, "world:", ppbox, roi_in_tile 
        #print "image", cbox, "img", ibox, roi_in_image
      #else:
        #print "roi is outside of the image"
      tile.save(tile_path)

def box_r(ibox, box):
  bx = box[0]
  by = box[3]
  w = box[2] - box[0]
  h = box[1] - box[3]
 
  l = [(ibox[0] - bx)/w, 1 - (ibox[1] - by)/h, (ibox[2] - bx)/w, 1 - (ibox[3] - by)/h]
  return l

def main():
  #print "hello world"
  usage = textwrap.dedent('''\
 %prog image_path bounds([left,upper,right,bottom]) length center([x,y]) 

SYNOPSIS AND USAGE
  %prog image_path bounds([left,upper,right,bottom]) length center([x,y]) 

DESCRIPTION
  Project image to VS space and export squared sub-area of VS space as mosaic.
  The mosaic consists of tiles of image with 256x256 pixels. Note that the edges
  of the original image must be parallel to axis of VS space because this program
  does not support projection with rotation. Location to project the original image
  is set by x or y coordinate of four edges (x coordinate of left and right edges 
  and y coordinate of upper and bottom edges). The squared sub-area on VS space is
  specified by center and width. The number of tiles depends on zoom levels. At zoom
  level 0 the squared sub-area is exported as a tile. Resolution of the tile is
  256/width (pixel/micron). With increment of zoom level the number of exporting tiles
  is multiplied by 2x2. This program generates a series of tiles for zoom level from 0
  to max. The zoom level max is specified by arguments. The tiles are compatible with
  Leaflet.js (a Javascript library for interactive maps). The tiles are exported as
  {zoom level}/{x}_{y}.png where x and y correspond to n-th coordinate of tile in horizontal
  and vertical direction. At zoom level 2, 16 tiles are exported as 2/0_0.png, 2/1_0.png,
  2/2_0.png, ..., and 2/3_3.png with resolution 1024/width (pixel/micron).

EXAMPLE
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] 18100 [-294.0,-943.0]
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] 18100 [-294.0,-943.0] -z 3 -o maps/cat -t

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
  parser.add_option("-l", "--tilesize", type="int", dest="tilesize",
              help="tile size", metavar="TILESIZE", default=256)
  parser.add_option("-t", "--transparent", action="store_true", dest="transparent",
              help="transparent", metavar="TRANSPARENT", default=False)
  parser.add_option("-z", "--maxzoom", type="int", dest="maxzoom",
              help="max zoom level", metavar="MAXZOOM", default=2)
  parser.add_option("-o", "--output-dir", type="string", dest="output_dir",
              help="output directory", metavar="OUTPUT_DIR")

  (options, args) = parser.parse_args()

  if len(args) != 4:
    parser.error("incorrect number of arguments")
 
  image_path = args[0]
  if os.path.exists(image_path) == False:
    parser.error("%s does not exist" % image_path)

  bounds = eval(args[1])
  length = float(args[2])
  center = eval(args[3])
  options.ibox = bounds
  options.length = length
  options.bbox = (center[0] - length/2,center[1] + length/2,center[0] + length/2,center[1] - length/2)

  dirname = "./"
  if options.output_dir != None:
    dirname = options.output_dir
  if not os.path.exists(dirname):
    os.makedirs(dirname)

  img_org = Image.open(image_path)
  rgbimg = img_org.convert('RGB')
  image = rgbimg
  if options.transparent:
    r,g,b = rgbimg.split()
    _r = r.point(lambda _: 0 if _ == 0 else 1, mode="1")
    _g = g.point(lambda _: 0 if _ == 0 else 1, mode="1")
    _b = b.point(lambda _: 0 if _ == 0 else 1, mode="1")
    mask = ImageChops.logical_and(_r,_g)
    mask = ImageChops.logical_and(mask, _b)
    rgbtimg = Image.new("RGBA", img_org.size, (0,0,0,0))
    rgbtimg.paste(rgbimg, mask=mask)
    image = rgbtimg
    #image.save(dirname+".png")
    #print img_org
    #print image

    for zoom in range(options.maxzoom + 1):
      make_tiles(zoom, image, dirname, options)

if __name__ == '__main__':
  main()
