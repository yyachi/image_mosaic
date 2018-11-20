#!/usr/bin/env python
import os
import sys
from cv2 import cv
#import threading
import time
import math
import yaml
from optparse import OptionParser


class ViewWindow:
	def __init__(self, image_path, title):
		self.image_path = image_path
		self.original_image = cv.LoadImage(image_path)
		self.window_name = title

	def open_window(self):
		cv.NamedWindow(self.window_name)

	def set_stage_geometry(self, x_range, y_range):
		self.min_stage_x = x_range[0]
		self.max_stage_x = x_range[1]
		self.min_stage_y = y_range[0]
		self.max_stage_y = y_range[1]

		stage_width = self.max_stage_x - self.min_stage_x
		stage_height = self.max_stage_y - self.min_stage_y
		stage_aspect = float(stage_width) / stage_height
		self.stage_width = stage_width
		self.stage_height = stage_height
		self.stage_aspect = stage_aspect

#		if pixels_per_um != None:
#			self.output_pixels_per_um = pixels_per_um
#			self.output_size = tuple([int(math.ceil(float(stage_width) * pixels_per_um)), int(math.ceil(float(stage_height) * pixels_per_um))])

	def set_stage_geometry_from_affine(self, affine, verbose = False):
		width = self.original_image.width
		height = self.original_image.height

		image_rect = [(0,0),(width,0),(width,height),(0,height)]
		image_rect_on_stage = transform_points(image_rect, affine)

		max_xy = list(image_rect_on_stage[0])
		min_xy = list(image_rect_on_stage[0])
		for stage in image_rect_on_stage:
			for i in range(len(max_xy)):
				if stage[i] > max_xy[i]:
					max_xy[i] = stage[i]
				if stage[i] < min_xy[i]:
					min_xy[i] = stage[i]

		self.max_stage_x = max_xy[0]
		self.max_stage_y = max_xy[1]
		self.min_stage_x = min_xy[0]
		self.min_stage_y = min_xy[1]

		stage_width = self.max_stage_x - self.min_stage_x
		stage_height = self.max_stage_y - self.min_stage_y
		stage_aspect = float(stage_width) / stage_height
		self.stage_width = stage_width
		self.stage_height = stage_height
		self.stage_aspect = stage_aspect

		if verbose:
			print "set_stage_geometry_from_affine"
			print "image_rect_on_stage:", image_rect_on_stage
			print "stage x: %f <-> %f" % (self.min_stage_x, self.max_stage_x)
			print "stage y: %f <-> %f" % (self.min_stage_y, self.max_stage_y)

	def set_output_size_from_aspect(self, verbose = False):
		width = self.original_image.width
		height = self.original_image.height

		output_width_height_based_width = [width, int(float(width) / self.stage_aspect)]
		output_width_height_based_height = [int(self.stage_aspect * height), height]
		if self.image_aspect > self.stage_aspect:
			output_image_width_height = output_width_height_based_width
		else:
			output_image_width_height = output_width_height_based_height

		output_image_width = output_image_width_height[0]
		output_image_height = output_image_width_height[1]
		if verbose:
			print "stage_aspect x image_height:", stage_aspect * height
			print "image_width / stage_aspect:", float(width) / stage_aspect
			print "based on width:", output_width_height_based_width
			print "based on height:", output_width_height_based_height

		self.output_size = tuple(output_image_width_height)
		self.output_pixels_per_um = float(output_image_width_height[0]) / self.stage_width


	def resize_image(self, pixels_per_um, verbose = False):
		self.output_pixels_per_um = pixels_per_um
		resize = tuple([int(math.ceil(float(self.stage_width) * pixels_per_um)), int(math.ceil(float(self.stage_height) * pixels_per_um))])

		self.resized_image = cv.CreateImage(resize, self.original_image.depth, self.original_image.channels)
		cv.Resize(self.output_image, self.resized_image)

		if verbose:
			print "resize_image"
			print "original pixels_per_um: %.3f" % (self.original_pixels_per_um)
			print "output image: %dx%d (%.3f)" % (self.output_size[0], self.output_size[1], float(self.output_size[0])/self.output_size[1])
			print "output pixels_per_um: %.3f" % (self.output_pixels_per_um)


	def warp_image(self, affine, view_geometry, verbose = False):
		width = self.original_image.width
		height = self.original_image.height
		image_aspect = float(width) / height
		self.image_aspect = image_aspect

		image_rect = [(0,0),(width,0),(width,height),(0,height)]
		image_rect_on_stage = transform_points(image_rect, affine)
		if abs(image_rect_on_stage[0][0] - image_rect_on_stage[1][0]) > 0:
			self.original_pixels_per_um = float(width) / abs(image_rect_on_stage[0][0] - image_rect_on_stage[1][0])
		else:
			self.original_pixels_per_um = float(height) / abs(image_rect_on_stage[0][1] - image_rect_on_stage[1][1])


		if hasattr(self, 'max_stage_x') != True and hasattr(self, 'max_stage_y') != True and hasattr(self, 'min_stage_x') != True and hasattr(self, 'min_stage_y') != True:
			self.set_stage_geometry_from_affine(affine, verbose)


		if hasattr(self, 'output_size') != True:
			self.set_output_size_from_aspect()


		if verbose:
			print "image_rect_on_stage:", image_rect_on_stage
			print "stage x: %f <-> %f" % (self.min_stage_x, self.max_stage_x)
			print "stage y: %f <-> %f" % (self.min_stage_y, self.max_stage_y)
			print "stage_width:", self.stage_width
			print "stage_height:", self.stage_height
			print "stage_aspect:", self.stage_aspect
			print "image_aspect:", self.image_aspect
			print "original pixels_per_um: %.3f" % (self.original_pixels_per_um)
			print "output image: %dx%d (%.3f)" % (self.output_size[0], self.output_size[1], float(self.output_size[0])/self.output_size[1])
			print "output pixels_per_um: %.3f" % (self.output_pixels_per_um)
			print self.output_size


		output_rect = [(0,0),(self.output_size[0],0),(self.output_size[0],self.output_size[1]),(0,self.output_size[1])]
		output_rect_on_stage = [(self.min_stage_x, self.max_stage_y),(self.max_stage_x, self.max_stage_y),(self.max_stage_x, self.min_stage_y),(self.min_stage_x, self.min_stage_y)]
		self.output_rect = output_rect
		self.output_rect_on_stage = output_rect_on_stage
		affine_stage2output = get_affine_matrix(output_rect_on_stage[0:3], output_rect[0:3])
		affine_output2stage = get_affine_matrix(output_rect[0:3], output_rect_on_stage[0:3])

		self.output_left_upper = [(0,0)]
		self.output_left_upper_on_stage = transform_points(self.output_left_upper, affine_output2stage)
		self.output_center = [(float(self.output_size[0])/2, float(self.output_size[1])/2)]
		self.output_center_on_stage = transform_points(self.output_center, affine_output2stage)[0]

		if verbose:
			print "output_rect:", output_rect
			print "output_rect_on_stage:", output_rect_on_stage
			print "output_center_on_stage:", self.output_center_on_stage

		image_rect_on_output = transform_points(image_rect_on_stage, affine_stage2output)
		affine_image2output = get_affine_matrix(image_rect[0:3], image_rect_on_output[0:3])
		self.affine_stage2output = affine_stage2output
		self.affine_output2stage = affine_output2stage
		self.affine_image2output = affine_image2output
		self.original_center = [(float(self.original_image.width)/2, float(self.original_image.height)/2)]
		self.original_center_on_output = transform_points(self.original_center, affine_image2output)[0]
		original_center_on_stage = transform_points([self.original_center_on_output], affine_output2stage)[0]
		self.output_image = cv.CreateImage(self.output_size, self.original_image.depth, self.original_image.channels)
		cv.SetImageROI(self.output_image, (0, 0, self.original_image.width, self.original_image.height))
		cv.Add(self.output_image, self.original_image,  self.output_image)
		cv.ResetImageROI(self.output_image)
		cv.WarpAffine(self.output_image, self.output_image, affine_image2output)

		if verbose:
			print "original_center_on_output:", self.original_center_on_output
			print "original_center_on_stage:", original_center_on_stage
			print "image_rect:", image_rect
			print "image_rect_on_stage:", image_rect_on_stage
			print "image_rect_on_output:", image_rect_on_output
			pos = [(int(t[0]), int(t[1])) for t in image_rect_on_output]
			cv.PolyLine( self.output_image, [pos], True, (0,255,0), 10, 8)

		r_w = float(view_geometry[0]) / self.output_image.width
		r_h = float(view_geometry[1]) / self.output_image.height
		r_view = r_w
		if r_w > r_h:
			r_view = r_h
		self.view_size = (int(self.output_image.width * r_view), int(self.output_image.height * r_view))
		self.temp = cv.CreateImage(self.view_size, self.original_image.depth, self.original_image.channels)
		cv.Resize(self.output_image, self.temp)

	def rectangle(self, pt1, pt2, color, thickness=1, lineType=8, shift=0):
		cv.Rectangle(self.output_image, pt1, pt2, color, thickness, lineType, shift)

	def rectangle_on_stage(self, pt1, pt2, color, thickness=1, lineType=8, shift=0):
		points_on_stage = [pt1, pt2]
		points_on_output = transform_points(points_on_stage, self.affine_stage2output)
		print points_on_output
		pos = [(int(t[0]), int(t[1])) for t in points_on_output]
		cv.Rectangle(self.output_image, pos[0], pos[1], color, thickness, lineType, shift)

	def draw_point_on_stage(self, pt1, color, thickness=1, size=10):
		point_on_stage = pt1
		point_on_output = transform_points([point_on_stage], self.affine_stage2output)[0]
		self.draw_point(tuple([int(round(x)) for x in point_on_output]), color, thickness, size)

	def draw_point(self, pt, color, thickness=10, size=10):
		radius = int(size * 1.0)
		l = int(size * 2.0)
		cv.Circle(self.output_image, pt, radius, color, thickness)
		cv.Line(self.output_image, (pt[0] - l, pt[1]), (pt[0] + l, pt[1]), color, thickness)
		cv.Line(self.output_image, (pt[0], pt[1] - l), (pt[0], pt[1] + l), color, thickness)
		self.temp = cv.CreateImage(self.view_size, self.original_image.depth, self.original_image.channels)
		cv.Resize(self.output_image, self.temp)



	def warp_image_and_place(self, affine, center, width, height, view_geometry):
		image_rect = [(0,0),(self.original_image.width,0),(self.original_image.width,self.original_image.height),(0,self.original_image.height)]
		image_rect_on_stage = transform_points(image_rect, affine)
		view_rect = [(0,0),(width,0),(width,height),(0,height)]
		view_rect_on_stage = [(center[0] - width / 2, center[1] + height / 2),(center[0] + width / 2, center[1] + height / 2),(center[0] + width / 2, center[1] - height / 2),(center[0] - width / 2, center[1] - height / 2)]
		affine_stage2view = get_affine_matrix(view_rect_on_stage[0:3], view_rect[0:3])
		image_rect_on_view = transform_points(image_rect_on_stage, affine_stage2view)
		affine_image2view = get_affine_matrix(image_rect[0:3], image_rect_on_view[0:3])

		self.view_image = cv.CreateImage((width, height), self.original_image.depth, self.original_image.channels)

		self.image_rect = image_rect
		self.image_rect_on_stage = image_rect_on_stage
		self.view_rect = view_rect
		self.view_rect_on_stage = view_rect_on_stage
		self.image_rect_on_view = image_rect_on_view

		cv.SetImageROI(self.view_image, (0, 0, self.original_image.width, self.original_image.height))
		cv.Add(self.view_image, self.original_image,  self.view_image)
		cv.ResetImageROI(self.view_image)
		cv.WarpAffine(self.view_image, self.view_image, affine_image2view)

		r_w = float(view_geometry[0]) / self.view_image.width
		r_h = float(view_geometry[1]) / self.view_image.height
		r_view = r_w
		if r_w > r_h:
			r_view = r_h
		self.view_size = (int(self.view_image.width * r_view), int(self.view_image.height * r_view))
		self.temp = cv.CreateImage(self.view_size, self.original_image.depth, self.original_image.channels)
		cv.Resize(self.view_image, self.temp)

	def draw_scale_bar(self):
		length_on_stage = 10**(round(math.log10(self.stage_width)) - 1)
		color = (255, 255, 255)
		offset = (100,100)

		points_on_stage = [(0,0),(length_on_stage, 0)]
		points_on_output = transform_points(points_on_stage, self.affine_stage2output)
		length_on_output = abs(points_on_output[1][0] - points_on_output[0][0])

		start = (offset[0], self.output_image.height - offset[1])
		cv.Rectangle(self.output_image, start, (start[0] + int(length_on_output), start[1] + int(length_on_output/50)), color, -1)
		self.temp = cv.CreateImage(self.view_size, self.original_image.depth, self.original_image.channels)
		cv.Resize(self.output_image, self.temp)

	def resize_and_save(self, filepath, pixels_per_um):
		self.save_size = (int(self.view_image.width * pixels_per_um), int(self.view_image.height * pixels_per_um))
		save_image = cv.CreateImage(self.save_size, self.view_image.depth, self.view_image.channels)
		cv.Resize(self.view_image, save_image)
		cv.SaveImage(filepath, save_image)
	def save_output(self, filepath):
		cv.SaveImage(filepath, self.output_image)

	def save_resized(self, filepath):
		cv.SaveImage(filepath, self.resized_image)


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
#		cv.NamedWindow(self.window_name)
#		self.interactive_mode
		self.active_point_index = None
		self.points = []
		self.drawing = False

	def open_window(self):
		cv.NamedWindow(self.window_name)

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

def get_default_view_width_height(affine, width, height):
	image_rect = [(0,0),(width,0),(width,height),(0,height)]
	image_rect_on_stage = transform_points(image_rect, affine)

	max_stage = [0,0]
	max_xy = [0,0]
	min_xy = [0,0]
	for stage in image_rect_on_stage:
		for i in range(len(max_stage)):
			if abs(stage[i]) > max_stage[i]:
				max_stage[i] = abs(stage[i])
			if stage[i] > max_xy[i]:
				max_xy[i] = stage[i]
			else:
				min_xy[i] = stage[i]
	print "max_xy:", max_xy
	print "min_xy:", min_xy
	stage_width = max_xy[0] - min_xy[0]
	stage_height = max_xy[1] - min_xy[1]
	stage_aspect = float(stage_width) / stage_height
	image_aspect = float(width) / height

	print "stage_width:", stage_width
	print "stage_height:", stage_height
	print "stage_aspect:", stage_aspect
	print "image_aspect:", image_aspect

	print "stage_aspect x image_height:", stage_aspect * height
	print "image_width / stage_aspect:", float(width) / stage_aspect

	output_width_height_based_width = [width, int(float(width) / stage_aspect)]
	output_width_height_based_height = [int(stage_aspect * height), height]
	print "based on width:", output_width_height_based_width
	print "based on height:", output_width_height_based_height

	if image_aspect > stage_aspect:
		output_image_width_height = output_width_height_based_width
	else:
		output_image_width_height = output_width_height_based_height

	pixels_per_um = float(output_image_width_height[0]) / stage_width
	print "output image: %dx%d (%.3f)" % (output_image_width_height[0], output_image_width_height[1], float(output_image_width_height[0])/output_image_width_height[1])
	print "pixels_per_um: %.3f" % (pixels_per_um)
	return [int(math.ceil(x)) * 2 for x in max_stage]

def image_pixel_to_coord(point, width, height):
	image_center = [float(width/2), float(height/2)]
	d = [float(point[0]) - image_center[0], image_center[1] - float(point[1])]
	pp = map((lambda x: float(x)/width * 100), d)
	return pp

def list_to_affine(list):
	mapping = cv.CreateMat(2, 3, cv.CV_32FC1)
	for row in range(mapping.rows):
		for col in range(mapping.cols):
			t = list[row]
			mapping[row, col] = t[col]
#			print "[%d,%d]: %f" % (row, col, mapping[row, col])
	return mapping

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

def get_anchor_on_image(win):
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

def get_anchor_on_stage(win):
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


def main():
	#argvs = sys.argv
	#argc = len(argvs)
	#if (argc != 2):
	#    print 'Usage: # python %s filename' % argvs[0]
	#    quit()

	# parser = OptionParser("usage: %prog [options] image")
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
  `--range'.  Without the option, minimum area that just covers the
  transformed image is exported.

EXAMPLE
  CMD> dir
  image.jpg  image.geo
  CMD> image-warp image.jpg -r -50 50 -38.45 38.45 -d 10.24
  ... |image_.jpg| and |image_.geo| were created
  CMD> dir
  image.jpg  image.geo  image_.jpg  image_.geo

SEE ALSO
  vs_attach_image.m
  image-get-affine (renamed from vs-calc-affine.py)
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


	win = ImageWindow(image_path,[500,500])
	original_width = win.original_image.width
	original_height = win.original_image.height
	original_aspect = float(original_width) / original_height
	#print "original image: %dx%d (%.3f)" % (original_width, original_height, original_aspect)

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
		interactive = True
		win.open_window()
		if interactive:
			anchors_on_image = get_anchor_on_image(win)
			anchors_on_stage = get_anchor_on_stage(win)
		#else:
		# for debug
		#	anchors_on_image = [[5678, 778], [3900, 4800], [1194, 474]]
		#	anchors_on_stage = [[4283.148, 2357.953], [2020.386, -3105.960], [-1790.444, 2593.054]]
		#	anchors_on_image = [[0, 0], [640, 960], [1280, 0]]
		#	anchors_on_stage = [[-76.0,-11715.0], [-676.0,-10815.0], [-1276.0,-11715.0]]

		win.set_anchors(anchors_on_image)
	#	win.active_point_index = 0
		win.draw_points(win.temp)
	#	center = [float(original_width)/2, float(original_height)/2]
	#	win.draw_point(win.temp, tuple([int(round(x * win.r_view)) for x in center]), (0,255,0))
		anchors_on_image_coord = [image_pixel_to_coord(p, original_width, original_height) for p in anchors_on_image]

		print "#\tx(pix)\ty(pix)\tx(um)\ty(um)"
		for idx in range(len(anchors_on_image)):
			print "%d\t%.3f\t%.3f\t%.3f\t%.3f" % (idx+1,anchors_on_image_coord[idx][0], anchors_on_image_coord[idx][1],anchors_on_stage[idx][0],anchors_on_stage[idx][1])

		affine_image2stage = get_affine_matrix(anchors_on_image, anchors_on_stage)
		affine_for_output = get_affine_matrix(anchors_on_image_coord, anchors_on_stage)

		f = open(default_yfile_path, 'w')
		yaml.dump(affine_to_list(affine_for_output), f, encoding='utf8', allow_unicode=True)
		print "%s %dx%d pix was calibrated. It's affine matrix to stage was %s." % (os.path.basename(image_path), original_width, original_height, affine_to_str(affine_for_output))
		cv.ShowImage(win.window_name, win.temp)

	win_view = ViewWindow(image_path, default_ofile_name)
	if x_range != None and y_range != None:
	#	win_view.set_stage_geometry(x_range = x_range, y_range = y_range, pixels_per_um = pixels_per_um)
		win_view.set_stage_geometry(x_range = x_range, y_range = y_range)
	win_view.warp_image(affine_image2stage, [500, 500], False)

	#for anchor_on_stage in anchors_on_stage:
	#	win_view.draw_point_on_stage(tuple(anchor_on_stage),(255,0,0),10,100)

	#win_view.draw_point_on_stage((530.6,-5.652),(0,255,0),10,100)
	#win_view.draw_point_on_stage((0,0),(255,255,255),10,100)
	#center = [float(win_view.output_image.width)/2, float(win_view.output_image.height)/2]
	#win_view.draw_point(tuple([int(round(x)) for x in center]),(0,0,255),10,100)
	if options.with_scale:
		win_view.draw_scale_bar()

	#f = open(default_yfile_name, 'w')
	#yaml.dump(affine_to_list(affine_for_output), f, encoding='utf8', allow_unicode=True)

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

	#output_rect = [(0,0),(win_view,0),(original_width,original_height),(0,original_height)]
	#image_rect_coord = [image_pixel_to_coord(p, original_width, original_height) for p in image_rect]


	#affine_image2stage = get_affine_matrix(anchors_on_image, anchors_on_stage)
	#affine_for_output = get_affine_matrix(anchors_on_image_coord, anchors_on_stage)

	#default_view = get_default_view_width_height(affine_image2stage, original_width, original_height )

	#win_view = ViewWindow(image_path, default_ofile_name)
	#center = [0, 0]
	#win_view.warp_image(affine_image2stage, center, default_view[0], default_view[1], [500,500])
	#win_view.draw_scale_bar(10**(round(math.log10(default_view[0])) - 1))

	#default_pixels_per_um = float(original_width) / default_view[0]
	#r_h = float(original_height) / default_view[1]

	#if default_pixels_per_um > r_h:
	#	default_pixels_per_um = r_h
	#win_view.resize_and_save(default_ofile_name, default_pixels_per_um)

	#print "%s %dx%d pix was calibrated and saved as %s." % (os.path.basename(image_path), original_width, original_height, default_ofile_path)
	#print "width: %d um" % (win_view.view_image.width)
	#print "height: %d um" % (win_view.view_image.height)
	#print "center: (%.3f, %.3f) um" % (center[0], center[1])
	#print "left upper: (%.3f, %.3f) um" % (win_view.view_rect_on_stage[0][0], win_view.view_rect_on_stage[0][1])
	#print "resolution: %.3f pix/um" % (default_pixels_per_um)
	#print "width: %d pix" % (win_view.save_size[0])
	#print "height: %d pix" % (win_view.save_size[1])
	#print "affine matrix: %s" % affine_to_str(affine_for_output)

	if options.flag_window:
		print "activate %s window and type escape to terminate." % (win_view.window_name)
		win_view.open_window()

		while True:

			cv.ShowImage(win.window_name, win.temp)
			cv.ShowImage(win_view.window_name, win_view.temp)
			if cv.WaitKey(15) == 27: break
	#raw_input()

if __name__ == '__main__':
	main()
