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

Commands to support imageometry file are summarized as:

| command             | description                                                                            | note |
| ------------------- | -------------------------------------------------------------------------------------- | ---- |
| image-get-affine    |Calculates affine_xy2vs (also affine_ij2vs and anchors_xy) from anchors and anchors_ij in imageometry file. Accepts anchors_ij via GUI and anchors via stdin. | Not Compatible with OpenCV3. interactive-command|
| image-warp-clicks   | Transform imagefile by matching three coordinates. Accepts anchors_ij via GUI and anchors via stdin.                                      | Not compatible with OpenCV3. Supports affine_ij2xy. interactive-command.    |
| image-warp          | Project image file into VS space based on Affine matrix stored in imageometry file and export sub-area of the VS space as image file. Accepts user interaction via command-line arguments.    |Not compatible with OpenCV3. Supports affine_ij2xy. interactive-command.     |

Commands to calculate a perspective transform from four pairs of the corresponding points are summarized as:

| command             | description                                                                            | note |
| ------------------- | -------------------------------------------------------------------------------------- | ---- |
| h_from_points       |The four pairs of the correspondig points are specified as command-line arguments.|Compatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage).|

Commands to calculate an affine transform from three pairs of the corresponding points are summarized as:

| command             | description                                                                            | note |
| ------------------- | -------------------------------------------------------------------------------------- | ---- |
| haffine_from_points |The three pairs of the corrensponding points are specified as command-line arguments.|Compatible with OpenCV3.|
| affine_from_points  |The three pairs of the corrensponding points are input via stdin.        |Compatible with OpenCV3.  interactive-command|


Commands to calculate an affine matrix of 2D rotation from parameters are summarized as:

| command             | description                                                                            | note |
| ------------------- | -------------------------------------------------------------------------------------- | ---- |
| haffine_from_params | Parameters are the center of the rotation in the source image, rotation angle and Isotropic scale factor. Accepts parameters via command-line arguments.|Compatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool).|

Commands to apply affine transform to an image or points are summarized as:

| command             | description                                                                            | note |
| ------------------- | -------------------------------------------------------------------------------------- | ---- |
| transform_image     | Applies an affine transformation to an image.                                                               |Compatible with OpenCV3. Supports affine_ij2ij.     |
| transform_points    | Applies an affine transformation to points.                                                            |Compatible with OpenCV3. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage)|
| image_in_image      | Overlay an image file in a base image with an affine transformation. The affine transform is calculated from corners of the overlay image on the base image specified via command-line arguments.|Compatible with OpenCV3. Used in [rails project -- medusa](https://github.com/misasa/medusa).|
| warp_image          | Impose an image file with rotated and magnified to an wallpaper image. Specify the wallpaper image and the transformation parameters as arguments.                           |Compatible with OpenCV3. Supports affine_ij2ij. Used in [gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool), [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage)|

Other commands are summarized as:

| command             | description                                                                            | note |
| ------------------- | -------------------------------------------------------------------------------------- | ---- |
| blend-image         | Blend two images using alpha blend techniques                                          | user-interactive-command     |
| crop_image          | Cut out a rectangular region of an image.|[gem package -- opencvtool](https://gitlab.misasa.okayama-u.ac.jp/gems/opencvtool), [gem package -- vstool](https://gitlab.misasa.okayama-u.ac.jp/gems/vstool),  [rake project -- mosaic-sem](https://gitlab.misasa.okayama-u.ac.jp/DREAM/mosaic-sem), [gem package -- multi_stage](https://gitlab.misasa.okayama-u.ac.jp/gems/multi_stage)|
| make_tiles          | Create map tiles to use with Leaflet.js.                   |[rails project -- medusa](https://github.com/misasa/medusa)|


# Usage

See online document with option `--help`.
