#!/usr/bin/env python
import sys
import yaml
from numpy import *
import cv2
import textwrap
from optparse import OptionParser
#sys.path.append(os.path.join(os.path.dirname(__file__),'../lib'))
from opencv_util import *

#from PCV.geometry import homography

def get_anchor_on_stage():
	# sys.stderr.write("input stage coordinates of each anchor points.\n")
	sys.stderr.write("#\tsrc x\tsrc y\tdst x\tdst y\n")
	while True:
		anchors = []
		src = []
		dst = []
		for idx in range(3):
			while True:
				sys.stderr.write(str(idx+1) + "\t")
				input = raw_input()
				vals = input.replace('\t', ' ').replace(',',' ').replace('\s+',' ').split()				
				if len(vals) < 4: continue
				if vals[0] == '#': continue
				src.append([float(vals[-4:][0]), float(vals[-4:][1])])
				dst.append([float(vals[-4:][2]), float(vals[-4:][3])])
				
				anchors.append([float(vals[-2:][0]), float(vals[-2:][1])])
				break

		#fp = array([[p[0] for p in src], [p[1] for p in src], [1.0 for p in src] ])
		#tp = array([[p[0] for p in dst], [p[1] for p in dst], [1.0 for p in dst] ])
		#src = str2array(array2str(src))
		#anchors = str2array(array2str(anchors))
		return array2str(src), array2str(anchors)


def main():
	usage = textwrap.dedent('''\
 %prog from_points to_points
  # Hint
  # %prog
  #		src-x src-y dst-x st-y 
  1		100	50 -50 100
  2		100	0 0 100
  3		0 0 0 0
  [[0.0,-1.0,0.0],[1.0,0.0,0.0],[0.0,0.0,1.0]]

SYNOPSIS AND USAGE
  %prog [options] from_points to_points

DESCRIPTION

EXAMPLE

SEE ALSO
  http://dream.misasa.okayama-u.ac.jp

IMPLEMENTATION
  Orochi, version 9
  Copyright (C) 2014 Okayama University
  License GPLv3+: GNU GPL version 3 or later

HISTORY
  August 11, 2015: Add documentation
''')
	parser = OptionParser(usage)
	parser.add_option("-f", "--output-format", type="choice", default ='text', choices = ['text', 'yaml'], dest="output_format",
	 				  help="output format: 'text' or 'yaml' [default: %default]", metavar="OUTPUT_FORMAT")

	(options, args) = parser.parse_args()

	# if len(args) != 2:
	#      parser.error("incorrect number of arguments")

	src, dst = get_anchor_on_stage()

	src = str2array(src)
	dst = str2array(dst)


	num_points,n = src.shape

	if num_points < 3:
		parser.error("requires at least 3 points")

	if src.shape != dst.shape:
		raise RuntimeError('number of points do not match')

	h = cv2.getAffineTransform(src,dst)
	h = numpy.append(h, numpy.array([0.0,0.0,1.0])).reshape(3,3)
	if options.output_format == 'text':
		print array2str(h)
	elif options.output_format == 'yaml':
		print yaml.dump(h.tolist(), encoding='utf8', allow_unicode=True)

if __name__ == '__main__':
	main()


# parser = OptionParser("usage: %prog [options] image")
# (options, args) = parser.parse_args()

#fp = array([[-50.0,50.0,50.0,-50.0],[37.5,37.5,-37.5,-37.5],[1,1,1,1]])
#tp = array([[4375.0,3235.0,3235.0,4375.0],[-6456.5,-6456.5,-5601.5,-5601.5],[1,1,1,1]])
# src, dst = get_anchor_on_stage()
# fp = array([[p[0] for p in src], [p[1] for p in src], [1.0 for p in src] ])
# tp = array([[p[0] for p in dst], [p[1] for p in dst], [1.0 for p in dst] ])

# h = homography.Haffine_from_points(fp,tp)

# print yaml.dump(h.tolist(), encoding='utf8', allow_unicode=True)



