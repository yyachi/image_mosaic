# ImageMosaic

Manipulate images utilizing power of Python.

This is called by [gem package -- vstool](http://devel.misasa.okayama-u.ac.jp/gitlab/gems/vstool/tree/master) and [gem package -- opencvtool](http://devel.misasa.okayama-u.ac.jp/gitlab/gems/opencvtool/tree/master).


# Dependency

## [pip](https://pip.pypa.io/en/latest/installing.html "download and DOS> python get-pip.py")

## [PyYAML](http://pyyaml.org/wiki/PyYAML "download and launch installer")

## [numpy](http://sourceforge.net/projects/numpy/files/NumPy/ "download and launch installer")

## [opencv](http://opencv.org/downloads.html "download and DOS> copy C:\opencv\build\python\2.7\x86\cv2.pyd C:\Python27\Lib\site-packages")


# Installation

Install it as Administrator as:

    ADMIN.CMD> pip install git+https://github.com/misasa/image_mosaic.git

Successful installation is confirmed by:

    CMD> blend-image --help

# Commands

Commands are summarized as:

| command             | description                                                               | note |
| ------------------- | ------------------------------------------------------------------------- | ---- |
| affine_from_points  | No description available                                                  |      |
| blend-image         | Blend two images using alpha blend techniques                             |      |
| crop_image          | No description available                                                  |      |
| h_from_points       | No description available                                                  |      |
| haffine_from_params | No description available                                                  |      |
| haffine_from_points | No description available                                                  |      |
| image-get-affine    | Calculate affine_ij2vs, affine_xy2vs, and anchors_xy                      |      |
| image-warp-clicks   | Transform imagefile by matching three coordinates                         |      |
| image-warp          | Transform imagefile based on Affine matrix stored in imageometry file.    |      |
| image_in_image      | No description available                                                  |      |
| make_tiles          | No description available                                                  |      |
| transform_image     | No description available                                                  |      |
| transform_points    | No description available                                                  |      |
| warp_image          | Transform an image based on parameters of angle, magnification, and shift |      |


# Usage

See online document with option `--help`.
