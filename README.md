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
| `image-get-affine`             | Return `affine_xy2vs` (also `affine_ij2vs` and anchors_xy) estimated from anchors and anchors_ij in imageometry file.  This command also reads anchors_ij via GUI and anchors via stdin.  This command is subset of `image-warp`, without image manipulation.  | Incompatible with OpenCV3. Interactive-command.                        |
| `image-warp-clicks` | Offer similar functionarity to `image-warp`.  User can create imageometry file with clicking image and typing stage corrdinate.  This command cannot accept -r and -d options unlike `image-warp`.                                                                                                                                                                                                         | Incompatible with OpenCV3. Supports `affine_xy2vs`. Interactive-command. |
| `image-warp`                   | Project image into VS space based on Affine matrix `affine_xy2vs` stored in imageometry file and export sub-area of the VS space as image file.                                                             | Incompatible with OpenCV3. Interactive-command. |

Commands to calculate a transform matrix are shown below.

| command               | description                                                                                                                                                                                | note                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------   | --------------------------------------------------------------------------------------                                                                                                     | ----                                                                                                                                                                                                                                                                                                                                                                         |
| `h_from_points`       | Return Affine matrix calculated from four pairs of coordinates.  Coordinates should be fed by arguments.                                                                                     | Compatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage). |
| `haffine_from_points` | Same as `h_from_points` but take three pairs of coordinates instead of four.                                                                                                           | Compatible with OpenCV3.                                                                                                                                                                                                                                                                                                                                                     |
| `affine_from_points`  | Same as `haffine_from_points` but coordinates should be fed by stdin instead of by arguments.                                                                                              | Compatible with OpenCV3.  interactive-command                                                                                                                                                                                                                                                                                                                                |
| `haffine_from_params` | Return Affine matrix calculated from center of rotation in source image, rotation angle, and magnification. Parameters should be fed by arguments. | Compatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool).                                                                                                                                                                                                                                                         |

Commands to apply geometrical transform to an image or points are shown below.

| command             | description                                                                                                                                                                          | note                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------- | --------------------------------------------------------------------------------------                                                                                               | ----                                                                                                                                                                                                                                                                                                                                                                                               |
| `warp_image`        | Transform an image using Affine matrix `affine_ij2ij` and export image.  Affine matrix can be also specified by center of ratation, angle of rotation, and magnification as similar to `haffine_from_params`. The area to be exported is specified by width and height via arguments.  Note that the top-left corner of the original image is the origin.  Without width and height specified, those of the original image would be applied. This program also imposes the transformed image on wall image.  In this case, Affine matrix is calculated from coordinates of 4 corners of the original image and coordinates where the 4 corners are projected (specified by arguments).| Incompatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage) |
| `image_in_image`    | Impose an image on wall image after Affine transformation.  Affine matrix is calculated from coordinates of 4 corners of the image and those projected onto the wall image specified by arguments. This command is subset of `warp_image`.| Compatible with OpenCV3. Supports `affine_ij2ij`.  Used in [rails project -- medusa](https://github.com/misasa/medusa).                                                                                                                                                                                                                                                                                                      |
| `transform_image` (obsolete)  | This command is subset of `warp_image`, but the area of exporting image is always same as the source image.                                                                  | Compatible with OpenCV3. Supports `affine_ij2ij`.                                                                                                                                                                                                                                                                                                                                                    |
| `transform_points`  | Return coordinates after Affine transformation using Affine matrix specified by arguments.                                                                                                                             | Compatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage)                        |

Other commands are shown below.

| command             | description                                                                            | note                                                                                                                                                                                                                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------- | ----                                                                                                                                                                                                                                                                                                                                        |
| `blend-image`       | Impose an image to wall image with alpha blend techniques.  Location to impose the image is set by ij corrdinates via arguments.                                        | user-interactive-command                                                                                                                                                                                                                                                                                                                    |
| `crop_image`        | Crop a rectangular region of an image.                                              | [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool),  [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage) |
| `make_tiles`        | Project an image into VS space and make the VS space zoomable with Leaflet.js. This program generates map tiles (256x256 pixels images) in a directory with the following structure: {zoom level}/{x}_{y}.png. For example at zoom level 2, the program projects the source image into the VS space (1024x1024 square image) and split it into 16 map tiles (2/0_0.png, 2/1_0.png, 2/2_0.png, ... 2/3_3.png). The length and the center of the VS space, the position of the source image on the VS space, and the maximum zoom level are specified by arguments.| [rails project -- medusa](https://github.com/misasa/medusa)                                                                                                                                                                                                                                                                                 |


# Usage

See online document with option `--help`.
