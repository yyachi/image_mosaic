import numpy
import math
import cv2

def image_pixel_to_coord(point, width, height):
  image_center = [float(width/2), float(height/2)]
  d = [float(point[0]) - image_center[0], image_center[1] - float(point[1])]
  if width > height:
    pp = map((lambda x: float(x)/width * 100), d)
  else:
    pp = map((lambda x: float(x)/height * 100), d)
  return pp

def get_affine_matrix(tsrc, tdst):
  src = numpy.array(tsrc, dtype=numpy.float32)
  dst = numpy.array(tdst, dtype=numpy.float32)
  num_points,n = src.shape
  if num_points == 3:
    h = cv2.getAffineTransform(src,dst)
    h = numpy.append(h, numpy.array([0.0,0.0,1.0])).reshape(3,3)
  else:
    h = cv2.getPerspectiveTransform(src,dst)
  return h

def transform_points(points, affine):
  src = numpy.array(points, dtype=numpy.float32)
  dst = cv2.perspectiveTransform(numpy.array([src]), affine)[0]
  return dst

def affine_to_str(affine):
  l = affine_to_list(affine)
  l_str = []
  for row in l:
    l_str.append(','.join(['%.3e' % x for x in row]))
  return "[" + ';'.join(l_str) + "]"

def affine_to_list(affine):
  l = []
  for row in range(affine.shape[0]):
    c = []
    for col in range(affine.shape[1]):
      c.append(affine[row, col])
    l.append(c)
  l.append([0,0,1])
  return l

def is_answer_yes(prompt = "answer yes/no", default = True, answer_yes = False):
  if answer_yes:
    print prompt
    return True
  else:
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

def list_to_affine(list):
  return numpy.array(list, dtype=numpy.float32)

def array2cvmat2D(array):
  # m,n = array.shape 
  # mat = cv.CreateMat(m, n, cv.CV_32FC1)
  # for i in range(m):
  #   for j in range(n):
  #       mat[i,j] = array[i,j]
  # return mat
  return array
        
def str2array(string):
  return numpy.array(eval(string), dtype=numpy.float32)

def array2str(array):
  tmp = []
  for row in array:
    tmp.append("[" + ",".join([str(f) for f in list(row)]) + "]")

  return "[" + ",".join(tmp) + "]"

def getRotationOffsetMatrix2D(offset, angle, scale):
  theata = math.radians(angle)
  alpha = scale * math.cos(theata)
  beta = scale * math.sin(theata)
  h = cv2.getRotationMatrix2D((0,0), angle, scale)
  h[0,2] = offset[0]
  h[1,2] = offset[1]

  # mapping = array2cvmat2D(numpy.array([[alpha, beta],[-beta, alpha]]))
  # shift_v = array2cvmat2D(numpy.array([[offset[0]], [offset[1]]]))

  # src = numpy.array([[0,0],[100,0],[100,100]], dtype=numpy.float32)
  # src_p = cv.CreateMat(len(src),1,cv.CV_32FC2)
  # dst_p = cv.CreateMat(len(src),1,cv.CV_32FC2)
  # for i in range(len(src)):
  #   point = src[i]
  #   src_p[i,0] = point
  # cv.Transform(src_p,dst_p,mapping,shift_v)

  # dst = []
  # for row in range(dst_p.rows):
  #   tpoint = dst_p[row,0]
  #   dst.append(list(tpoint))
  # dst = numpy.array(dst, dtype=numpy.float32)
  # h = cv2.getAffineTransform(src,dst)
  return h
