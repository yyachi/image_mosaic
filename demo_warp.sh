#!/bin/sh
docker run -it --gpus all --rm -v $PWD:/image_mosaic yyachi/image_mosaic:gpu bash -c "python3 image_mosaic/opencv_cuda.py test/files/20200310-2153.jpg test/files/warped-20200806-1-1efwlrp.png '[[0,0],[5756,55],[5790,8364],[33,8308]]' -p nearest -o maps/warped-20200806-1-1efwlrp.png"
