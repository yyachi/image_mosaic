# python package -- image_mosaic

A series of image utilities.  Use this ImageMosaic package to crop, rotate, or
enlarge bitmap images.  This package was developed as python package
-- opencvtool until 2018-08.

See [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool) that refers to this package.
See [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool) that refers to this package.
See [rails project -- medusa](https://github.com/misasa/medusa) that refers to this package.
See [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem) that refers to this package.
See also `spots-warp` in [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage).

# Dependency

## [OpenCV 3](https://opencv.org/releases.html)

# Installation

## Windows

Download OpenCV for MS Windows, uncompress the archive, and copy a Python library file `CV2.pyd` to local Python directory such for `C:\Python27\Lib\site-packages`.

    $ cd ~/Downlaods/
    $ wget https://sourceforge.net/projects/opencvlibrary/files/opencv-win/3.4.3/opencv-3.4.3-vc14_vc15.exe/download
    CMD> cd %USERPROFILE%\Downloads\
    CMD> copy opencv\build\python\2.7\x64\cv2.pyd C:\Python27\Lib\site-packages\
    
Install this package as Administrator as:

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

## macOS
Download and install the [Anaconda (a distribution of Python for data science).](https://www.anaconda.com/)

    $ cd ~/Downloads/
    $ wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-MacOSX-x86_64.pkg
    $ open Anaconda3-5.3.0-MacOSX-x86_64.pkg
    $ source ~/.bash_profile
    $ which python
    /Users/dream/anaconda3/bin/python
    $ python -V
    Python 3.7.0
    
Install OpenCV into Anaconda.

    $ conda install -c conda-forge opencv
    $ conda list | grep opencv
    opencv                    3.4.1           py36_blas_openblash553dce0_201    conda-forge

Install scipy into Anaconda.

    $ conda install pyyaml numpy pillow

Install this package.

    $ git clone https://github.com/misasa/image_mosaic.git
    $ cd image_mosaic
    $ python setup.py install
    $ conda list | grep image-mosaic
    image-mosaic              0.1.5                     <pip>

# Commands

Commands to project an image to VS space are shown below.

| command                        | description                                                                                                                                                                                                                                                | referer                                                                   |
| ----------------------------   | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----                                                                   |
| `image-get-affine`             | Return `affine_xy2vs` (also `affine_ij2vs` and anchors_xy) estimated from anchors and anchors_ij in imageometry file.    This command is subset of `image-warp`, without image manipulation.  ||
| `image-warp-clicks` | Offer similar functionality to `image-warp`.  User can create imageometry file with clicking image and typing stage coordinates.  This command cannot accept --range and --density options unlike `image-warp`.                                                                                                                                                                                                         ||
| `image-warp`                   | Project an image into VS space based on Affine matrix `affine_xy2vs` stored in imageometry file and export sub-area of the VS space as image file.                                                             ||
| `make_tiles`        | Project image to VS space and export squared sub-area of VS space as mosaic.  The mosaic consists of tiles of image with 256x256 pixels.   Note that the edges of the original image must be parallel to axis of VS space because this program does not support projection with rotation. Location to project the original image is set by x or y coordinate of four edges (x coordinate of left and right edges and y coordinate of upper and bottom edges). The squared sub-area on VS space is specified by center and width. The number of tiles depends on `zoom levels`.  At `zoom level` 0 the squared sub-area is exported as a tile.  Resolution of the tile is 256/`width` (pixel/micron). With increment of zoom level the number of exporting tiles is multiplied by 2x2.   This program generates a series of tiles for zoom level from 0 to `max`. The zoom level `max` is specified by arguments.  The tiles are compatible with [Leaflet.js](https://leafletjs.com/) (a Javascript library for interactive maps). The tiles are exported as {zoom level}/{x}_{y}.png where x and y correspond to n-th coordinate of tile in horizontal and vertical direction.  At zoom level 2,  16 tiles are exported as 2/0_0.png, 2/1_0.png, 2/2_0.png, ..., and 2/3_3.png with resolution 1024/`width` (pixel/micron).  | [rails project -- medusa](https://github.com/misasa/medusa)                                                                                                                                                                                                                                                                                 |

Commands to estimate Affine matrix are shown below.

| command               | description                                                                                                                                                                                | referer                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------   | --------------------------------------------------------------------------------------                                                                                                     | ----                                                                                                                                                                                                                                                                                                                                                                         |
| `h_from_points`       | Return Affine matrix calculated from four pairs of coordinates.  Coordinates should be fed by arguments.                                                                                     | [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage) |
| `haffine_from_points` | Same as `h_from_points` but takes three pairs of coordinates instead of four.                                                                                                           ||                                                                                                                                                                                                                                                                                                                                                 
| `affine_from_points`  | Same as `haffine_from_points` but coordinates should be fed by stdin instead of by arguments.                                                                                              ||
| `haffine_from_params` | Return Affine matrix calculated from center of rotation in original image, rotation angle, and magnification. Parameters should be fed by arguments. |[gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool)                                                                                                                                                                                                                                                         |

Commands to transform an image by Affine transform `affine-ij2ij` are shown below.

| command             | description                                                                                                                                                                          | referer                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------- | --------------------------------------------------------------------------------------                                                                                               | ----                                                                                                                                                                                                                                                                                                                                                                                               |
| `warp_image`        | Transform an image using Affine matrix `affine_ij2ij` and export image.  Affine matrix can be specified by (1) 3x3 matrix, (2) center of rotation in original image, rotation angle, and magnification as similar to `haffine_from_params`, and (3) coordinates where the 4 corners of the original image are projected. The area to be exported can be specified by width and height via arguments. Without width and height specified, those of the original image would be applied. This program also imposes the original image on wall image. In this case, the area to be exported is set by width and height of the wall image. | [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage) |
| `image_in_image`    | Impose an image on wall image after Affine transformation.  Affine matrix `affine_ij2ij` is specified by coordinates where the 4 corners of the original image are projected. This command is subset of `warp_image`. |[rails project -- medusa](https://github.com/misasa/medusa)                                                                                                                                                                                                                                                                                                      |
| `transform_image` (obsolete)  | This command is subset of `warp_image`.  The area to be exported is set by width and height of the original image.                                                                  | |
| `transform_points`  | Return coordinates after Affine transformation. Original coordinates and Affine matrix are specified by arguments.                                                                                                                             | [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage)                        |

Commands to mix images and extract image are shown below.

| command             | description                                                                            | referer                                                                                                                                                                                                                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------- | ----                                                                                                                                                                                                                                                                                                                                        |
| `blend-image`       | Impose image to wall image with alpha blend techniques.  Location to impose the image is set by ij coordinates via arguments.                                        | |
| `crop_image`        | Crop a rectangular region of an image.                                              | [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool),  [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage) |

# Usage

See on-line document with option `--help`.
