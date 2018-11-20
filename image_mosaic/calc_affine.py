#!/usr/bin/env python
from optparse import OptionParser
import os
import sys
from cv2 import cv
#import threading
import time
import math
import yaml

class ImageWindow:
	def __init__(self, image_path, view_geometry = [500, 500]):
		self.image_path = image_path
		self.original_image = cv.LoadImage(image_path)
		r_w = float(view_geometry[0]) / self.original_image.width
		r_h = float(view_geometry[1]) / self.original_image.height
		self.r_view = r_w
		if r_w > r_h:
			self.r_view = r_h
		self.image = cv.CreateImage((int(self.original_image.width * self.r_view), int(self.original_image.height * self.r_view)), cv.IPL_DEPTH_8U, 3)
		cv.Resize(self.original_image, self.image)
		self.temp = cv.CloneImage(self.image)
		self.window_name = os.path.basename(image_path)
		cv.NamedWindow(self.window_name)
#		self.interactive_mode
		self.active_point_index = None
		self.points = []
		self.drawing = False

	def interactive_mode(self):
		cv.SetMouseCallback(self.window_name,self.specify_anchors)

	def normal_mode(self):
		cv.SetMouseCallback(self.window_name,self.normal)


	def anchors(self):
		array = []
		for point in self.points:
			anchor = (round(point[0] / self.r_view), round(point[1] / self.r_view))
			array.append(anchor)
		return array

	def set_anchors(self, anchors):
		points = []
		for anchor in anchors:
			#anchor_on_view = (round(anchor[0] * self.r_view), anchor[1] * self.r_view )
			anchor_on_view = tuple([int(round(x * self.r_view)) for x in anchor])
			points.append(anchor_on_view)
		self.points = points

	def normal(self, event, x, y, flags, param):
		pt = (x, y)

	def specify_anchors(self, event, x, y, flags, param):
		pt = (x, y)
#		print event
#		print pt
		if event == cv.CV_EVENT_LBUTTONDOWN:
#			print ":left_button_down"
			self.drawing = True
			self.temp = cv.CloneImage(self.image)
			self.draw_points(self.temp)
			self.draw_point(self.temp, pt, (255,0,0))

		elif event == cv.CV_EVENT_MOUSEMOVE:
#			print ":move"
			self.temp = cv.CloneImage(self.image)
			self.draw_points(self.temp)

			if self.drawing:
				self.draw_point(self.temp, pt, (0,255,0))
			else:
				self.draw_cross(self.temp, pt)

		elif event == cv.CV_EVENT_LBUTTONUP:
#			print "left_button_up"
			self.points.append(pt)
			self.temp = cv.CloneImage(self.image)
			self.draw_points(self.temp)
			self.drawing = False

#			print self.points
	def draw_points(self, image):
		for i in range(len(self.points)):
			point = self.points[i]
			if self.active_point_index == i:
#				print "active", i
				self.draw_point(image, point, (0, 0, 255))
			else:
#				print "normal", i
				self.draw_point(image, point, (255, 0, 0))
			#print point


	def draw_point(self, image, pt, color):
		thickness = 1
		size = 10
		radius = int(size * 1.0)
		l = int(size * 2.0)
		cv.Circle(image, pt, radius, color)
		cv.Line(image, (pt[0] - l, pt[1]), (pt[0] + l, pt[1]), color)
		cv.Line(image, (pt[0], pt[1] - l), (pt[0], pt[1] + l), color)


	def draw_cross(self, image, pt):
#		print "cross lines drawing..."
		cv.Line(image, (0, pt[1]), (self.original_image.width - 1, pt[1]), (255,255,255))
		cv.Line(image, (pt[0], 0), (pt[0], self.original_image.height - 1), (255,255,255))

def image_pixel_to_coord(point, width, height):
	image_center = [float(width/2), float(height/2)]
	d = [float(point[0]) - image_center[0], image_center[1] - float(point[1])]
	if width > height:
		pp = map((lambda x: float(x)/width * 100), d)
	else:
		pp = map((lambda x: float(x)/height * 100), d)
	return pp


def get_anchor_on_image():
	print "input image coordinates of 3 anchor points."
	print "#\tx(pix)\ty(pix)"
	while True:
		anchors_on_image = []
		for idx in range(3):
			while True:
				input = raw_input(str(idx+1) + "\t")
				vals = input.replace('\t', ' ').replace(',',' ').replace('\s+',' ').split()
				if len(vals) < 2: continue
				anchors_on_image.append((float(vals[-2:][0]), float(vals[-2:][1])))
				break

		return anchors_on_image

def get_anchor_on_image_from_window(win):
	print "click image and specify 3 anchor points."
	print "#\tx(pix)\ty(pix)"
	count = 0
	win.interactive_mode()
	#cv.SetMouseCallback(win.window_name,win.specify_anchors)

	while True:
		cv.ShowImage(win.window_name, win.temp)
		if len(win.points) != count:
			anchor = win.anchors()[-1]
			anchor_coord = image_pixel_to_coord(anchor, original_width, original_height)
			#print count + 1, anchor[0], anchor[1]
			print "%d\t%.3f\t%.3f" % (count+1,anchor_coord[0],anchor_coord[1])
			count += 1
		if count == 3:
			win.normal_mode()
			break
		if cv.WaitKey(15) == 27: break
	return win.anchors()

def get_anchor_on_stage():
	print "input stage coordinates of each anchor points."
	print "#\tx(um)\ty(um)"
	while True:
		anchors_on_stage = []
		for idx in range(3):
			while True:
				input = raw_input(str(idx+1) + "\t")
				vals = input.replace('\t', ' ').replace(',',' ').replace('\s+',' ').split()
				if len(vals) < 2: continue
				anchors_on_stage.append((float(vals[-2:][0]), float(vals[-2:][1])))
				break

		return anchors_on_stage

def get_anchor_on_stage_from_window(win):
	print "input stage coordinates of each anchor points."
	print "#\tx(um)\ty(um)"
	while True:
		anchors_on_stage = []
		for idx in range(3):
			while True:
				win.active_point_index = idx
				win.draw_points(win.temp)
				cv.ShowImage(win.window_name, win.temp)
				cv.WaitKey(15)
				input = raw_input(str(idx+1) + "\t")
				vals = input.replace('\t', ' ').replace(',',' ').replace('\s+',' ').split()
				if len(vals) < 2: continue
				anchors_on_stage.append((float(vals[-2:][0]), float(vals[-2:][1])))
				break
		win.active_point_index = None
		win.draw_points(win.temp)
		cv.ShowImage(win.window_name, win.temp)
		cv.WaitKey(15)

		return anchors_on_stage

def get_affine_matrix(tsrc, tdst):
	verbose = False
	mapping = cv.CreateMat(2, 3, cv.CV_32FC1)
	src = []
	dst = []
	for point in tsrc:
		src.append(tuple(point))
	for point in tdst:
		dst.append(tuple(point))
	cv.GetAffineTransform(src, dst, mapping)
	if verbose:
		for row in range(mapping.rows):
			for col in range(mapping.cols):
				print "[%d,%d]: %f" % (row, col, mapping[row, col])
	return mapping

def transform_points(points, affine):
	src = cv.CreateMat(len(points),1,cv.CV_32FC2)
	dst = cv.CreateMat(len(points),1,cv.CV_32FC2)

	for i in range(len(points)):
		point = points[i]
		src[i,0] = point
	cv.Transform(src,dst,affine)
	tpoints = []
	for row in range(dst.rows):
		tpoint = dst[row,0]
		tpoints.append(tpoint)
	return tpoints

def affine_to_str(affine):
	l = affine_to_list(affine)
	l_str = []
	for row in l:
		l_str.append(','.join(['%.3e' % x for x in row]))
	return "[" + ';'.join(l_str) + "]"

def affine_to_list(affine):
	l = []
	for row in range(affine.rows):
		c = []
		for col in range(affine.cols):
			c.append(affine[row, col])
		l.append(c)

	l.append([0,0,1])
	return l

def list_to_affine(list):
	mapping = cv.CreateMat(2, 3, cv.CV_32FC1)
	for row in range(mapping.rows):
		for col in range(mapping.cols):
			t = list[row]
			mapping[row, col] = t[col]
#			print "[%d,%d]: %f" % (row, col, mapping[row, col])
	return mapping

def is_answer_yes(prompt = "answer yes/no", default = True):
	input = raw_input(prompt).lower()

	if len(input) == 0:
		return default
	elif input[0] == "y":
		return True
	elif input[0] == "n":
		return False
	else:
		return default

def points_to_list(points):
	l = [[],[],[]]
	for point in points:
		l[0].append(point[0])
		l[1].append(point[1])
		l[2].append(1)
	return l

def list_to_points(l):
	points = []
	for index in range(len(l[0])):
		point = ( l[0][index], l[1][index] )
		points.append(point)
	return points

def main():
        parser = OptionParser("""usage: %prog [options] image

SYNOPSIS AND USAGE
  python %prog [options] imagefile.jpg

DESCRIPTION
  Calculate affine_ij2vs, affine_xy2vs, and anchors_xy, from anchors
  and anchors_ij in imageometry file that comes with imagefile.jpg.
  For example, when imageilfe.jpg is `raman.jpg', this will look for
  imageometry file `raman.geo'.  Very likly you have to invoke this
  program from CMD prompt on MS Windows.

EXAMPLE
  CMD> dir
  raman.jpg  raman.geo
  CMD> type raman.geo
  anchors:
  - [X1 X2 X3]
  - [Y1 Y2 Y3]
  - [1  1  1 ]
  anchors_ij:
  - [x1 x2 x3]
  - [y1 y2 y3]
  - [1  1  1 ]
  CMD> python C:/Users/ims/xtreeml/imgtools/bin/vs-calc-affine.py raman.jpg
  ... <affine_xy2vs> and <affine_ij2vs> inserted in |raman.geo|

SEE ALSO
  blend-image
  image-warp
  http://dream.misasa.okayama-u.ac.jp

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  May 24, 2015: TK adds documentation
""")
	parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="make lots of noise")
	parser.add_option("-w", "--window",
	                 action="store_true", dest="flag_window", default=False,
	                 help="interate with a window")

	(options, args) = parser.parse_args()
	if len(args) != 1:
	    parser.error("incorrect number of arguments")

	image_path = args[0]

	original_image = cv.LoadImage(image_path)
	original_width = original_image.width
	original_height = original_image.height
	original_aspect = float(original_width) / original_height


	root, ext = os.path.splitext(image_path)
	default_ofile_name = os.path.basename(root) + '_' + ext #  _VS
	default_yfile_name = os.path.basename(root) + '.geo'    # .yaml
	warped_yfile_name = os.path.basename(root) + '_.geo'    # _warped.yaml


	curdir = os.getcwd()
	default_ofile_path = os.path.join(curdir, default_ofile_name)
	default_yfile_path = os.path.join(curdir, default_yfile_name)
	warped_yfile_path = os.path.join(curdir, warped_yfile_name)

	config = None

	if options.flag_window:
		win = ImageWindow(image_path,[500,500])

	if os.path.isfile(default_yfile_path):
		print "%s loading..." % default_yfile_path
		yf = open(default_yfile_path).read().decode('utf8')
		config = yaml.load(yf)
		if 'affine_ij2vs' in config:
			affine_input = list_to_affine(config['affine_ij2vs'])
			print "Input affine matrix to stage is %s." % (affine_to_str(affine_input))
			image_rect = [(0,0),(original_width,0),(original_width,original_height),(0,original_height)]
			image_rect_coord = [image_pixel_to_coord(p, original_width, original_height) for p in image_rect]
			image_rect_on_stage = transform_points(image_rect_coord, affine_input)
			affine_image2stage = get_affine_matrix(image_rect, image_rect_on_stage)
			print "%s %dx%d pix was calibrated based on %s. It's affine matrix to stage is %s." % (os.path.basename(image_path), original_width, original_height, os.path.basename(default_yfile_name), affine_to_str(affine_input))

	if config != None and ('anchors_ij' in config) and is_answer_yes("Anchors for image <anchors_ij> found.  Do you use them? (YES/no) "):
		anchors_on_image = list_to_points(config['anchors_ij'])
	else:
		if options.flag_window:
			anchors_on_image = get_anchor_on_image_from_window(win)
		else:
			anchors_on_image = get_anchor_on_image()


	if config != None and ('anchors' in config) and is_answer_yes("Anchors for stage <anchors> found.  Do you use them? (YES/no) "):
		#vals = input.replace('\t', ' ').replace(',',' ').replace('\s+',' ').split()
		anchors_on_stage = list_to_points(config['anchors'])
	else:
		if options.flag_window:
			anchors_on_stage = get_anchor_on_stage_from_window(win)
		else:
			anchors_on_stage = get_anchor_on_stage()


	if options.flag_window:
		# anchors_on_image = get_anchor_on_image_from_window(win)
		# anchors_on_stage = get_anchor_on_stage_from_window(win)
		win.set_anchors(anchors_on_image)
		win.draw_points(win.temp)
	# else:
	# 	anchors_on_image = get_anchor_on_image()
	# 	anchors_on_stage = get_anchor_on_stage()

	anchors_on_image_coord = [image_pixel_to_coord(p, original_width, original_height) for p in anchors_on_image]

	#	center = [float(original_width)/2, float(original_height)/2]
	#	win.draw_point(win.temp, tuple([int(round(x * win.r_view)) for x in center]), (0,255,0))
	print "#\tx(pix)\ty(pix)\tx(um)\ty(um)"
	for idx in range(len(anchors_on_image)):
		print "%d\t%.3f\t%.3f\t%.3f\t%.3f" % (idx+1,anchors_on_image_coord[idx][0], anchors_on_image_coord[idx][1],anchors_on_stage[idx][0],anchors_on_stage[idx][1])

	affine_image2stage = get_affine_matrix(anchors_on_image, anchors_on_stage)
	affine_for_output = get_affine_matrix(anchors_on_image_coord, anchors_on_stage)

	f = open(default_yfile_path, 'w')
	yaml.dump({ 'anchors': points_to_list(anchors_on_stage), 'anchors_xy': points_to_list(anchors_on_image_coord), 'anchors_ij': points_to_list(anchors_on_image), 'affine_xy2vs': affine_to_list(affine_for_output), 'affine_ij2vs': affine_to_list(affine_image2stage) }, f, encoding='utf8', allow_unicode=True)
	print "%s %dx%d pix was calibrated. Its affine matrix to stage was %s." % (os.path.basename(image_path), original_width, original_height, affine_to_str(affine_for_output))


if __name__ == "__main__":
	main()
