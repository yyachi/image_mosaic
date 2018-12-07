import cv2
from image_mosaic.util import *
import os

class Gui:
  def __init__(self, image_path, view_geometry = [500, 500]):
    self.image_path = image_path
    self.original_image = cv2.imread(image_path)

    r_w = float(view_geometry[0]) / self.original_image.shape[0]
    r_h = float(view_geometry[1]) / self.original_image.shape[1]
    self.r_view = r_w
    if r_w > r_h:
      self.r_view = r_h
    dim = [int(self.original_image.shape[1] * self.r_view), int(self.original_image.shape[0] * self.r_view)]
    self.image = cv2.resize(self.original_image, tuple(dim))
    #self.image = cv.CreateImage((int(self.original_image.width * self.r_view), int(self.original_image.height * self.r_view)), cv.IPL_DEPTH_8U, 3)
    #cv.Resize(self.original_image, self.image)
    self.temp = self.image.copy()
    self.window_name = os.path.basename(image_path)
    cv2.namedWindow(self.window_name)
#   self.interactive_mode
    self.active_point_index = None
    self.points = []
    self.drawing = False

  def interactive_mode(self):
    #cv.SetMouseCallback(self.window_name,self.specify_anchors)
    cv2.setMouseCallback(self.window_name, self.specify_anchors)

  def normal_mode(self):
    cv2.setMouseCallback(self.window_name,self.normal)

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
    if event == cv2.EVENT_LBUTTONDOWN:
      self.drawing = True
      self.temp = self.image.copy()

      self.draw_points(self.temp)
      self.draw_point(self.temp, pt, (255,0,0))

    elif event == cv2.EVENT_MOUSEMOVE:
      self.temp = self.image.copy()
      self.draw_points(self.temp)

      if self.drawing:
        self.draw_point(self.temp, pt, (0,255,0))
      else:
        self.draw_cross(self.temp, pt)

    elif event == cv2.EVENT_LBUTTONUP:
      self.points.append(pt)
      self.temp = self.image.copy()
      self.draw_points(self.temp)
      self.drawing = False

  def draw_points(self, image):
    for i in range(len(self.points)):
      point = self.points[i]
      if self.active_point_index == i:
        self.draw_point(image, point, (0, 0, 255))
      else:
        self.draw_point(image, point, (255, 0, 0))


  def draw_point(self, image, pt, color):
    thickness = 1
    size = 10
    radius = int(size * 1.0)
    l = int(size * 2.0)
    cv2.circle(image, pt, radius, color)
    cv2.line(image, (pt[0] - l, pt[1]), (pt[0] + l, pt[1]), color)
    cv2.line(image, (pt[0], pt[1] - l), (pt[0], pt[1] + l), color)


  def draw_cross(self, image, pt):
    cv2.line(image, (0, pt[1]), (self.original_image.shape[0] - 1, pt[1]), (255,255,255))
    cv2.line(image, (pt[0], 0), (pt[0], self.original_image.shape[1] - 1), (255,255,255))

  def get_anchor_on_image(self):
    print("click image and specify 3 anchor points.")
    print("#\tx(pix)\ty(pix)")
    count = 0
    self.interactive_mode()

    while True:
      cv2.imshow(self.window_name, self.temp)
      if len(self.points) != count:
        anchor = self.anchors()[-1]
        anchor_coord = image_pixel_to_coord(anchor, self.original_image.shape[0], self.original_image.shape[1])
        #print count + 1, anchor[0], anchor[1]
        print("%d\t%.3f\t%.3f" % (count+1,anchor_coord[0],anchor_coord[1]))
        count += 1
      if count == 3:
        self.normal_mode()
        break
      if cv2.waitKey(15) == 27: break
    return self.anchors()

  def get_anchor_on_stage(self):
    print("input stage coordinates of each anchor points.")
    print("#\tx(um)\ty(um)")
    while True:
      anchors_on_stage = []
      for idx in range(3):
        while True:
          self.active_point_index = idx
          self.draw_points(self.temp)
          cv2.imshow(self.window_name, self.temp)
          cv2.waitKey(15)
          input = raw_input(str(idx+1) + "\t")
          vals = input.replace('\t', ' ').replace(',',' ').replace('\s+',' ').split()
          if len(vals) < 2: continue
          anchors_on_stage.append((float(vals[-2:][0]), float(vals[-2:][1])))
          break
      self.active_point_index = None
      self.draw_points(self.temp)
      cv2.imshow(self.window_name, self.temp)
      cv2.waitKey(15)
      return anchors_on_stage