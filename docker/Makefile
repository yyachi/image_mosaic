UID?="${UID}"

build:
	cd .. && docker build -t image_mosaic -f docker/Dockerfile .

test: build
	cd .. && docker run -it -v ${PWD}/..:/image_mosaic -w /image_mosaic --rm -u $(UID) image_mosaic:latest nosetests -s -v
