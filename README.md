# python package -- image_mosaic

A series of image utilities.  Use this ImageMosaic package to crop, rotate, or
enlarge bitmap images.  This package was developed as [python package
-- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/pythonpackage/opencvtool)
until 2018-08.

See [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool) that refers to this package.
See [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool) that refers to this package.
See [rails project -- medusa](https://github.com/misasa/medusa) that refers to this package.
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

Commands to project an image to VS space are shown below.

| command                        | description                                                                                                                                                                                                                                                | note                                                                   |
| ----------------------------   | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----                                                                   |
| `image-get-affine`             | Return `affine_xy2vs` (also `affine_ij2vs` and anchors_xy) estimated from anchors and anchors_ij in imageometry file.  This command also reads anchors_ij via GUI and anchors via stdin.  This command is subset of `image-warp`, without image manipulation.  | Incompatible with OpenCV3.|
| `image-warp-clicks` | Offer similar functionarity to `image-warp`.  User can create imageometry file with clicking image and typing stage corrdinates.  This command cannot accept --range and --density options unlike `image-warp`.                                                                                                                                                                                                         | Incompatible with OpenCV3.|
| `image-warp`                   | Project an image into VS space based on Affine matrix `affine_xy2vs` stored in imageometry file and export sub-area of the VS space as image file.                                                             | Incompatible with OpenCV3.|
| `make_tiles`        | Project an image into VS space and export a squared sub-area of the VS space as tile images (256x256 pixel images) which can be used with the [Leaflet.js](https://leafletjs.com/) (a Javascript library for interactive maps).  Note that the edges of the source image must be parallel to the VS coordinate axis because this program does not support projection with rotation. Location to project the source image is set by x or y coordinate of four edges (x coordinate of left and right edges and y coordinate of upper and bottom edges) of the source image on the VS space. The squared sub-area is specified by the coordinate of the center of the area and the `width` of the area on the VS space. The number of tile images and resolution of each tile image depend on zoom levels. At the zoom level 0 the squared sub-area is exported as a 256x256 pixel image. Thus the number and resolution of map tile is 1 tile and 256/`width`, respectively. With increasing zoom levels the width of exported image is multiplied by 2 (a 512x512 pixel image at zoom level 1, a 1024x1024 pixel image at zoom level 2. For to make tile images, the exporting image for each zoom level is divided into 256x256 pixel images. Thus the number of tile images and the resolution of each tile image are 4 tiles and 512/`width` at zoom level 1, 16 tiles and 1024/`width` at zoom level 2. This program generates tile images from zoom level 0 to zoom level `max`. The zoom level `max` is specified by arguments. The tile images for each zoom level are exported in a directory with the following file path: {zoom level}/{x}_{y}.png. For example at zoom level 2, the 16 tiles are exported as 2/0_0.png, 2/1_0.png, 2/2_0.png, ..., and 2/3_3.png.| Used in [rails project -- medusa](https://github.com/misasa/medusa)                                                                                                                                                                                                                                                                                 |

Commands to calculate a transform matrix are shown below.

| command               | description                                                                                                                                                                                | note                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------   | --------------------------------------------------------------------------------------                                                                                                     | ----                                                                                                                                                                                                                                                                                                                                                                         |
| `h_from_points`       | Return Affine matrix calculated from four pairs of coordinates.  Coordinates should be fed by arguments.                                                                                     | Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage). |
| `haffine_from_points` | Same as `h_from_points` but takes three pairs of coordinates instead of four.                                                                                                           ||                                                                                                                                                                                                                                                                                                                                                 
| `affine_from_points`  | Same as `haffine_from_points` but coordinates should be fed by stdin instead of by arguments.                                                                                              ||
| `haffine_from_params` | Return Affine matrix calculated from center of rotation in original image, rotation angle, and magnification. Parameters should be fed by arguments. |Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool).                                                                                                                                                                                                                                                         |

Commands to apply geometrical transform to an image or points are shown below.

| command             | description                                                                                                                                                                          | note                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------- | --------------------------------------------------------------------------------------                                                                                               | ----                                                                                                                                                                                                                                                                                                                                                                                               |
| `warp_image`        | Transform an image using Affine matrix `affine_ij2ij` and export image.  Affine matrix can be specified by (1) 3x3 matrix, (2) center of rotation in original image, rotation angle, and magnification as similar to `haffine_from_params`, and (3) coordinates where the 4 corners of the source image are transformed. The area to be exported can be specified by width and height via arguments. Without width and height specified, those of the original image would be applied. This program also imposes the transformed image on wall image. In this case, the area to be exported is set by width and height of the wall image. | Incompatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage) |
| `image_in_image`    | Impose an image on wall image after Affine transformation.  Affine matrix `affine_ij2ij` is specified by coordinates where the 4 corners of the source image are transformed. This command is subset of `warp_image`. |Used in [rails project -- medusa](https://github.com/misasa/medusa).                                                                                                                                                                                                                                                                                                      |
| `transform_image` (obsolete)  | This command is subset of `warp_image`.  The area to be exported is set by width and height  of the source image.                                                                  | |
| `transform_points`  | Return coordinates after Affine transformation.  Original coordinates and Affine matrix are specified by arguments.                                                                                                                             | Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage)                        |

Other commands are shown below.

| command             | description                                                                            | note                                                                                                                                                                                                                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------- | ----                                                                                                                                                                                                                                                                                                                                        |
| `blend-image`       | Impose an image to wall image with alpha blend techniques.  Location to impose the image is set by ij corrdinates via arguments.                                        | |
| `crop_image`        | Crop a rectangular region of an image.                                              | [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool),  [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage) |

# Usage

See online document with option `--help`.
