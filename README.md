# python package -- image_mosaic

A series of image utilities.  Use this ImageMosaic package to crop, rotate, or
enlarge bitmap images.  This package was developed as [python package
-- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/pythonpackage/opencvtool)
until 2018-08.

See [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool) that refers to this package.
See [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool) that refers to this package.
See [Rails project -- medusa](https://github.com/misasa/medusa) that refers to this package.
See [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem) that refers to this package.
See also `spots-warp` in [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage).

# Dependency

## [OpenCV 2.4](https://opencv.org/releases.html)

Download OpenCV 2.4 for MS Windows, uncompress the archive, and copy a Python library file `CV2.pyd` to local Python directory such for `C:\Python27\Lib\site-packages`.

    $ cd ~/Downlaods/
    $ wget https://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.13/opencv-2.4.13.6-vc14.exe/download
    CMD> cd %USERPROFILE%\Downloads\
    CMD> copy opencv\build\python\2.7\x64\cv2.pyd C:\Python27\Lib\site-packages\

# Installation

Install it as Administrator as:

    ADMIN.CMD> pip install git+https://github.com/misasa/image_mosaic.git

or as:

    $ cd ~/Downloads/
    $ wget https://github.com/misasa/image_mosaic/archive/master.zip
    ADMIN.CMD> cd %USERPROFILE%\Downloads\
    ADMIN.CMD> pip list
    ADMIN.CMD> pip uninstall opencvtool
    ADMIN.CMD> pip install master.zip

Successful installation is confirmed by:

    CMD> image-warp --help

# Commands

Commands are summarized as:

| command             | description                                                                            | note |
| ------------------- | -------------------------------------------------------------------------------------- | ---- |
| affine_from_points  | Calculates an affine transform from three pairs of the corresponding points.           |      |
| blend-image         | Blend two images using alpha blend techniques                                          |      |
| crop_image          | No description available                                                               |      |
| h_from_points       | No description available                                                               |      |
| haffine_from_params | No description available                                                               |      |
| haffine_from_points | No description available                                                               |      |
| image-get-affine    | Calculate affine_ij2vs, affine_xy2vs, and anchors_xy from anchors in imageometry file. |      |
| image-warp-clicks   | Transform imagefile by matching three coordinates                                      |      |
| image-warp          | Create an image file after rotation, magnification, and distortion based on Affine matrix in imageometry file.      |      |
| image_in_image      | No description available                                                               |      |
| make_tiles          | No description available                                                               |      |
| transform_image     | No description available                                                               |      |
| transform_points    | No description available                                                               |      |
| warp_image          | Impose an image file with rotated and magnified to an wallpaper image. Specify the wallpaper image and the transformation parameters as arguments.                         |      |

# Usage

See online document with option `--help`.
