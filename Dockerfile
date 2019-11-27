FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip install .
CMD ["image-warp", "--help"]