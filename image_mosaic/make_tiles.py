#!/usr/bin/env python
import os
import sys
import textwrap
import numpy
from PIL import Image, ImageChops
from optparse import OptionParser
import math
import multiprocessing as mp
from multiprocessing import Pool
import cv2

my_global = None

def tile_ij_at(zoom, x, y, length, center, tilesize = 256):
  left = center[0] - length/2
  upper = center[1] + length/2
  dx = x - left
  dy = upper - y
  n = 2**zoom
  pix = tilesize * n
  lpp = length/float(pix)
  ii = dx/(lpp * tilesize)
  jj = dy/(lpp * tilesize)
  i = int(math.floor(ii))
  if (i < 0):
    i = 0
  elif (i > (n - 1)):
    i = n - 1

  j = int(math.floor(jj))
  if (j < 0):
    j = 0
  elif (j > (n - 1)):
    j = n - 1
  return (i,j)

def make_tiles(zoom, img, dirname, options):
  
  ibox = options.ibox
  tilesize = options.tilesize
  length = options.length
  box = options.bbox
  n = 2**zoom
  fpix = n * tilesize
  
  #print ibox
  #print box
  pix = tilesize * n
  length_per_pix = length/float(pix)
  dum = length_per_pix*tilesize
  #print length
  #print pix
  #print length_per_pix
  #print dum
  min_i, min_j = tile_ij_at(zoom, ibox[0], ibox[1], length, options.center)
  max_i, max_j = tile_ij_at(zoom, ibox[2], ibox[3], length, options.center)
  for i in range(min_i, max_i + 1):
    for j in range(min_j, max_j + 1):
      #tile_path = os.path.join(dirname,"%d-%d.png",i,j)
      if (options.tile):
        tdirname = os.path.join(dirname,str(zoom))
        if not os.path.exists(tdirname):
          os.makedirs(tdirname)
        tile_path = os.path.join(tdirname,"%d_%d.png" % (i,j))
        if (os.path.exists(tile_path)) and options.compose:
          tile = Image.open(tile_path)
        else:
          tile = Image.new('RGBA', (tilesize, tilesize), (0,0,0,0))
      if options.merge:
        merge_path = os.path.join(dirname,"%d.png" % zoom)
        if options.merge_path:
          merge_path = options.merge_path
          base, ext = os.path.splitext(merge_path)
          if (ext == ''):
            if not os.path.exists(merge_path):
              os.makedirs(merge_path)
            merge_path = os.path.join(merge_path, "%d.png" % zoom)
        if (os.path.exists(merge_path)):
          merge = Image.open(merge_path)
        else:
          merge = Image.new('RGBA', (fpix, fpix), (0,0,0,0))

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
        roi_in_merge = (int(i*tilesize) + int(cb[0]*tilesize),int(j*tilesize) + int(cb[1]*tilesize),int(i*tilesize) + int(cb[2]*tilesize),int(j*tilesize) + int(cb[3]*tilesize))
        #print "crop", roi_in_image
        rsize = (roi_in_tile[2] - roi_in_tile[0], roi_in_tile[3] - roi_in_tile[1])
        #print "resize", rsize
        #print "paste", roi_in_tile
        try:
          part = img.crop(roi_in_image)
          part = part.resize(rsize)
          if options.tile:
            tile.paste(part, roi_in_tile, mask=part.split()[3])
          if options.merge:
            merge.paste(part, roi_in_merge, mask=part.split()[3])
        except:
          print("failed to generate %s" % tile_path)
        #print "tile", cbox, "world:", ppbox, roi_in_tile 
        #print "image", cbox, "img", ibox, roi_in_image
      #else:
        #print "roi is outside of the image"
      if options.tile:
        tile.save(tile_path)
      if options.merge:
        merge.save(merge_path)

def make_params(zoom, img, dirname, options):

  ibox = options.ibox
  tilesize = options.tilesize
  length = options.length
  box = options.bbox
  n = 2**zoom
  fpix = n * tilesize
  
  pix = tilesize * n
  length_per_pix = length/float(pix)
  dum = length_per_pix*tilesize
  #print length
  #print pix
  #print length_per_pix
  #print dum
  min_i, min_j = tile_ij_at(zoom, ibox[0], ibox[1], length, options.center)
  max_i, max_j = tile_ij_at(zoom, ibox[2], ibox[3], length, options.center)
  params = []
  for i in range(min_i, max_i + 1):
    for j in range(min_j, max_j + 1):
      #param = {'img': img}
      param = {}
      #param['img'] = img
      #tile_path = os.path.join(dirname,"%d-%d.png",i,j)
      if (options.tile):
        tdirname = os.path.join(dirname,str(zoom))
        if not os.path.exists(tdirname):
          os.makedirs(tdirname)
        tile_path = os.path.join(tdirname,"%d_%d.png" % (i,j))
        param['tile_path'] = tile_path
        param['tilesize'] = tilesize
#        if (os.path.exists(tile_path)) and options.compose:
#          tile = Image.open(tile_path)
#        else:
#          tile = Image.new('RGBA', (tilesize, tilesize), (0,0,0,0))

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
        roi_in_merge = (int(i*tilesize) + int(cb[0]*tilesize),int(j*tilesize) + int(cb[1]*tilesize),int(i*tilesize) + int(cb[2]*tilesize),int(j*tilesize) + int(cb[3]*tilesize))
        #print "crop", roi_in_image
        rsize = (roi_in_tile[2] - roi_in_tile[0], roi_in_tile[3] - roi_in_tile[1])
        #print "resize", rsize
        #print "paste", roi_in_tile
        param['roi_in_src'] = roi_in_image
        param['resize'] = rsize
        try:
          if options.tile:
            param['roi_in_tile'] = roi_in_tile
        except:
          print("failed to generate %s" % tile_path)
      else:
        print("roi is outside of the image")
      params.append(param)

  return params

def save_tile(path):
  global my_dict
  #print("saving %s" % path)
  my_dict[path].save(path)

def make_tile(param):
  global g_tilesize
  global my_global
  img = my_global
  tilesize = g_tilesize
  roi_in_src = param['roi_in_src']
  part = img.crop(roi_in_src)
  rsize = param['resize']
  try:
    part = part.resize(rsize)
  except:
    print(param)
    return
  tile_path = param['tile_path']
  roi_in_tile = param['roi_in_tile']
  if (tile_path in my_dict.keys()):
    tile = my_dict[tile_path]
  elif (os.path.exists(tile_path)):
    tile = Image.open(tile_path)
  else:
    tile = Image.new('RGBA', (tilesize, tilesize), (0,0,0,0))
  tile.paste(part, roi_in_tile, mask=part.split()[3])
  #tile.save(tile_path)
  oimg_bgr = cv2.cvtColor(numpy.array(tile), cv2.COLOR_RGBA2BGRA)
  cv2.imwrite(tile_path, oimg_bgr)
  #return (tile_path, tile)

def box_r(ibox, box):
  bx = box[0]
  by = box[3]
  w = box[2] - box[0]
  h = box[1] - box[3]
 
  l = [(ibox[0] - bx)/w, 1 - (ibox[1] - by)/h, (ibox[2] - bx)/w, 1 - (ibox[3] - by)/h]
  return l

def distance(p1, p2):
  return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def warp(dic, options):
  edges = dic['edges']
  lu = edges[0]
  ru = edges[1]
  rb = edges[2]
  xs = [edge[0] for edge in edges]
  ys = [edge[1] for edge in edges]
  left = min(xs)
  right = max(xs)
  upper = max(ys)
  bottom = min(ys)
  bounds = [left, upper, right, bottom]
  dic['bounds'] = bounds
  w_um = distance(lu, ru)
  h_um = distance(ru, rb)
  img1 = cv2.imread(dic['path'], cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
  height1 = img1.shape[0]
  width1 = img1.shape[1]

  p_um = width1/w_um
  b_w = right - left
  b_h = upper - bottom
  new_geometry = [math.ceil(b_w * p_um), math.ceil(b_h * p_um)]
  corners_on_new_image = []
  for corner in edges:
    dx = corner[0] - left
    dy = upper - corner[1]
    pixs = [int(dx/b_w*new_geometry[0]), int(dy/b_h*new_geometry[1])]
    corners_on_new_image.append(pixs)
  width2 = new_geometry[0]
  height2 = new_geometry[1]
  img2 = numpy.zeros((height2, width2, 3), numpy.uint8)
  src = numpy.array([[0,0],[width1,0],[width1,height1],[0,height1]], dtype = numpy.float32)
  dst = numpy.array(corners_on_new_image, dtype=numpy.float32)
  h = cv2.getPerspectiveTransform(src,dst)
  flags = cv2.INTER_LINEAR
  if options.interpolation_method == 'nearest':
    flags = cv2.INTER_NEAREST
  elif options.interpolation_method == 'area':
    flags = cv2.INTER_AREA
  elif options.interpolation_method == 'cubic':
    flags = cv2.INTER_CUBIC
  elif options.interpolation_method == 'lanczos4':
    flags = cv2.INTER_LANCZOS4

  img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  img1_gray = cv2.warpPerspective(img1_gray, h, (width2, height2), flags=flags)
  img1_gray = cv2.add(img1_gray, 1)
  (thresh, mask) = cv2.threshold(img1_gray, 1, 255, cv2.THRESH_BINARY_INV)

  img3 = cv2.warpPerspective(img1, h, (width2, height2), flags=flags)
  cv2.add(img2, img3, img3, mask)
  #cv2.imwrite(output_path, img3)
  return Image.fromarray(cv2.cvtColor(img3, cv2.COLOR_BGRA2RGBA))

#@profile
def main():
  usage = textwrap.dedent('''\
 %prog <image_path> <upper_and_bottom_edges|four_corners> [(<image_path> <upper_and_bottom_edges|four_corners>) ...] length center([x,y]) 

SYNOPSIS AND USAGE
  %prog <image_path> <upper_and_bottom_edges|four_corners> [(<image_path> <upper_and_bottom_edges|four_corners>) ...] length center([x,y]) 

DESCRIPTION
  Project images to VS space and export squared sub-area of VS space as mosaic.
  The mosaic consists of tiles of image with 256x256 pixels. 
   Locations to project the original images
  are set by x or y coordinate of upper and bottom edges (x coordinate of left edge, 
  y coordinate of upper edge, x coordinate of right edge, and y coordinate of bottom edges) 
  or by x and y coordinate of 4 corners (x and y coordinates of left upper, right upper, 
  right bottom, and left bottom corners). 
  The squared sub-area on VS space is
  specified by center and width. The number of tiles depends on zoom levels. At zoom
  level 0 the squared sub-area is exported as a tile. Resolution of the tile is
  256/width (pixel/micron). With increment of zoom level the number of exporting tiles
  is multiplied by 2x2. This program generates a series of tiles for zoom level from min (default 0) to max (default 2). The zoom level min and max are changed by arguments -i and -z, respectively. When the zoom level is specified by the argument -a, this program gerates a series of tiles at the zoom level.  The tiles are compatible with
  Leaflet.js (a Javascript library for interactive maps). The tiles are exported as
  {zoom level}/{x}_{y}.png where x and y correspond to n-th coordinate of tile in horizontal
  and vertical direction. At zoom level 2, 16 tiles are exported as 2/0_0.png, 2/1_0.png,
  2/2_0.png, ..., and 2/3_3.png with resolution 1024/width (pixel/micron). 

  This program replaces a color (default black) with transparent when the arguments -t is specified. 
  The color is specified with the argument -c. When the arguments --overlay is specified, This program 
  overlay a tile over the existing tile.

  This program merge tiles into an image when the arguments --merge is specified. The output path can
  be specified with the argument --merged-path. With the argument --no-tile you will obtain only merged image.

EXAMPLE
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] 18100 [-294.0,-943.0]
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] data/dog.jpg [-934.4,549.3,875.6,-737.9] 18100 [-294.0,-943.0]
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] 18100 [-294.0,-943.0] -z 3 -o maps/cat -t
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] 18100 [-294.0,-943.0] -a 4 -o maps/cat -t -c 255 255 255
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] 18100 [-290.0,-950.0] -a 4 -o maps/cat -t -c 255 255 255 --overlay
  > %prog data/cat.jpg [-9344.0,5493.0,8756.0,-7379.0] 18100 [-294.0,-943.0] -a 4 -o maps/cat_merged.png -t -c 255 255 255 --merge --no-tile

SEE ALSO
  https://github.com/misasa/image_mosaic
  https://github.com/misasa/image_mosaic/blob/master/image_mosaic/make_tiles.py

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014-2020 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  August 11, 2015: Add documentation
''')

  parser = OptionParser(usage)
  parser.add_option("--no-tile", action="store_false", dest="tile",
              help="without tile", metavar="WITHOUT_TILE", default=True)
  parser.add_option("-l", "--tilesize", type="int", dest="tilesize",
              help="tile size", metavar="TILESIZE", default=256)
  parser.add_option("-t", "--transparent", action="store_true", dest="transparent",
              help="transparent", metavar="TRANSPARENT", default=False)
  parser.add_option("-c", "--transparent-color", type="int", nargs=3, dest="transparent_color",
              help="transparent color", metavar="TRANSPARENT_COLOR", default=(0,0,0))
  parser.add_option("-p","--compose", action="store_true", dest="compose",
              help="compose", metavar="COMPOSE", default=False)
  parser.add_option("--overlay", action="store_true", dest="compose",
              help="overlay", metavar="OVERLAY", default=False)
  parser.add_option("--interpolation-method", type="choice", default ='linear', choices = ['linear', 'nearest'], dest="interpolation_method",
              help="interpolation method: 'linear' or 'nearest' [default: %default]", metavar="INTERPOLATION_METHOD")
#  parser.add_option("-m", "--merge", action="store_true", dest="merge",
#              help="merge", metavar="MERGE", default=False)
  parser.add_option("-i", "--min-zoom-level", type="int", dest="min_zoom_level",
              help="minimum zoom level", metavar="MINIMUM_ZOOM_LEVEL", default=0)
  parser.add_option("-z", "--max-zoom-level", type="int", dest="max_zoom_level",
              help="max zoom level", metavar="MAXIMUM_ZOOM_LEVEL", default=2)
  parser.add_option("-a", "--zoom-level", type="int", dest="zoom_level",
              help="zoom level", metavar="ZOOM_LVEL")
  parser.add_option("-o", "--output-dir", type="string", dest="output_dir",
              help="output directory", metavar="OUTPUT_DIR")
#  parser.add_option("--merge-path", type="string", dest="merge_path",
#              help="merged file path", metavar="MERGE_PATH")
  parser.add_option("-d", "--debug", action="store_true", dest="debug",  
              help="debug", metavar="DEBUG", default=False)
  parser.add_option("--multi", type="int", dest="multi",
              help="multiprocessing (default: %default)", metavar="MULTIPROCESSING", default=os.cpu_count())
  (options, args) = parser.parse_args()

  if len(args) < 4:
    parser.error("incorrect number of arguments")

  center = eval(args.pop(-1))
  length = float(args.pop(-1))

  images = []
  while len(args) > 0:
    image_path = args.pop(0)
    if os.path.exists(image_path) == False:
      parser.error("%s does not exist" % image_path)
    edge_or_corner = eval(args.pop(0))
    if (type(edge_or_corner[0]) is list):
      images.append({'path': image_path, 'edges': edge_or_corner})
    else:
      images.append({'path': image_path, 'bounds': edge_or_corner})

  options.length = length
  options.center = center
  options.bbox = (center[0] - length/2,center[1] + length/2,center[0] + length/2,center[1] - length/2)
  
  dirname = "./"
  if options.output_dir != None:
    dirname = options.output_dir

  if not os.path.exists(dirname):
    os.makedirs(dirname)

  global my_dict
  my_dict = {}  
  for dic in images:
    if ('edges' in dic.keys()):
      img_org = warp(dic, options)
    else:
      img_org = Image.open(dic['path'])

    rgbimg = img_org.convert('RGB')
    image = rgbimg
    if options.debug:
      print(options)
    if options.transparent:
      src_color = options.transparent_color
      r,g,b = rgbimg.split()
      _r = r.point(lambda _: 1 if _ == src_color[0] else 0, mode="1")
      _g = g.point(lambda _: 1 if _ == src_color[1] else 0, mode="1")
      _b = b.point(lambda _: 1 if _ == src_color[2] else 0, mode="1")

      mask = ImageChops.logical_and(_r,_g)
      mask = ImageChops.logical_and(mask, _b)
      mask_inv = ImageChops.invert(mask)
      rgbtimg = Image.new("RGBA", img_org.size, (0,0,0,0))
      rgbtimg.paste(rgbimg, mask=mask_inv)
      image = rgbtimg

    bounds = dic['bounds']
    options.ibox = bounds
    if options.zoom_level:
      #make_tiles(options.zoom_level, image, dirname, options)
      params = make_params(options.zoom_level, image, dirname, options)
    else:
      params = []
      for zoom in range(options.min_zoom_level, (options.max_zoom_level + 1)):
        #make_tiles(zoom, image, dirname, options)
        params.extend(make_params(zoom, image, dirname, options))
    global g_tilesize
    g_tilesize = 256
    global my_global
    my_global = image
    p = Pool(options.multi)
    tiles = p.map(make_tile, params)
    for tile in tiles:
      if tile is not None:
        my_dict[tile[0]] = tile[1]
    p.close()
#  for path in my_dict.keys():
#    my_dict[path].save(path)
  p = Pool(options.multi)
  p.map(save_tile, my_dict.keys())
  p.close()
  
if __name__ == '__main__':
  main()
