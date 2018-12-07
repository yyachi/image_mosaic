import cv2
from image_mosaic.opencv_util import *

class Stage:
  def __init__(self):    
    #self.image_path = image_path
    #self.original_image = cv2.imread(image_path)
    pass

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

  def set_stage_geometry_from_affine(self, affine, verbose = False):
    height, width, channels = self.original_image.shape

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
      print("set_stage_geometry_from_affine")
      print("image_rect_on_stage:", image_rect_on_stage)
      print("stage x: %f <-> %f" % (self.min_stage_x, self.max_stage_x))
      print("stage y: %f <-> %f" % (self.min_stage_y, self.max_stage_y))

  def set_output_size_from_aspect(self, verbose = False):
    height, width, channels = self.original_image.shape

    output_width_height_based_width = [width, int(float(width) / self.stage_aspect)]
    output_width_height_based_height = [int(self.stage_aspect * height), height]
    if self.image_aspect > self.stage_aspect:
      output_image_width_height = output_width_height_based_width
    else:
      output_image_width_height = output_width_height_based_height

    output_image_width = output_image_width_height[0]
    output_image_height = output_image_width_height[1]
    if verbose:
      print("stage_aspect x image_height:", stage_aspect * height)
      print("image_width / stage_aspect:", float(width) / stage_aspect)
      print("based on width:", output_width_height_based_width)
      print("based on height:", output_width_height_based_height)

    self.output_size = tuple(output_image_width_height)
    self.output_pixels_per_um = float(output_image_width_height[0]) / self.stage_width

  def set_image(self, image_path, affine, verbose = False):
    self.image_path = image_path
    self.original_image = cv2.imread(image_path)

    height, width, channels = self.original_image.shape
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
      print("image_rect_on_stage:", image_rect_on_stage)
      print("stage x: %f <-> %f" % (self.min_stage_x, self.max_stage_x))
      print("stage y: %f <-> %f" % (self.min_stage_y, self.max_stage_y))
      print("stage_width:", self.stage_width)
      print("stage_height:", self.stage_height)
      print("stage_aspect:", self.stage_aspect)
      print("image_aspect:", self.image_aspect)
      print("original pixels_per_um: %.3f" % (self.original_pixels_per_um))
      print("output image: %dx%d (%.3f)" % (self.output_size[0], self.output_size[1], float(self.output_size[0])/self.output_size[1]))
      print("output pixels_per_um: %.3f" % (self.output_pixels_per_um))
    output_width, output_height = self.output_size

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
      print("output_rect:", output_rect)
      print("output_rect_on_stage:", output_rect_on_stage)
      print("output_center_on_stage:", self.output_center_on_stage)

    image_rect_on_output = transform_points(image_rect_on_stage, affine_stage2output)
    affine_image2output = get_affine_matrix(image_rect[0:3], image_rect_on_output[0:3])
    self.affine_stage2output = affine_stage2output
    self.affine_output2stage = affine_output2stage
    self.affine_image2output = affine_image2output
    self.original_center = [(float(self.original_image.shape[0])/2, float(self.original_image.shape[1])/2)]
    self.original_center_on_output = transform_points(self.original_center, affine_image2output)[0]
    original_center_on_stage = transform_points([self.original_center_on_output], affine_output2stage)[0]
    self.output_image = cv2.warpPerspective(self.original_image, affine_image2output, (output_width, output_height))

    if verbose:
      print("original_center_on_output:", self.original_center_on_output)
      print("original_center_on_stage:", original_center_on_stage)
      print("image_rect:", image_rect)
      print("image_rect_on_stage:", image_rect_on_stage)
      print("image_rect_on_output:", image_rect_on_output)
      pos = [(int(t[0]), int(t[1])) for t in image_rect_on_output]
      cv2.polylines( self.output_image, numpy.int32([numpy.array(pos)]), True, (0,255,0), 10, 8)

  def draw_scale_bar(self):
    length_on_stage = 10**(round(math.log10(self.stage_width)) - 1)
    color = (255, 255, 255)
    offset = (100,100)

    points_on_stage = [(0,0),(length_on_stage, 0)]
    points_on_output = transform_points(points_on_stage, self.affine_stage2output)
    length_on_output = abs(points_on_output[1][0] - points_on_output[0][0])

    start = (offset[0], self.output_image.shape[1] - offset[1])
    cv2.rectangle(self.output_image, start, (start[0] + int(length_on_output), start[1] + int(length_on_output/50)), color, -1)
    cv2.resize(self.output_image, self.view_size)

  def resize_image(self, pixels_per_um, verbose = False):
    self.output_pixels_per_um = pixels_per_um
    resize = tuple([int(math.ceil(float(self.stage_width) * pixels_per_um)), int(math.ceil(float(self.stage_height) * pixels_per_um))])
    rshape = list(self.output_image.shape)
    rshape[0] = resize[0]
    rshape[1] = resize[1]
    #self.resized_image = cv.CreateImage(resize, self.original_image.depth, self.original_image.channels)
    #cv.Resize(self.output_image, self.resized_image)
    self.resized_image = cv2.resize(self.output_image, resize)
    if verbose:
      print("resize_image")
      print("original pixels_per_um: %.3f" % (self.original_pixels_per_um))
      print("output image: %dx%d (%.3f)" % (self.output_size[0], self.output_size[1], float(self.output_size[0])/self.output_size[1]))
      print("output pixels_per_um: %.3f" % (self.output_pixels_per_um))
