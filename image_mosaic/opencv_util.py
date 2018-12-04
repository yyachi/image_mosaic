import numpy
import math
import cv2

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
