from setuptools import setup, find_packages
import sys, os

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

version = '0.1.9'

setup(name='image_mosaic',
      version=version,
      description="Python package for manipulating image",
      long_description=readme,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='cv',
      author='Yusuke Yachi',
      author_email='yyachi@misasa.okayama-u.ac.jp',
      url='http://github.com/misasa/image_mosaic',
      license=license,
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            "PyYAML",
            "numpy",
            "Pillow",
            "opencv-python",
          # -*- Extra requirements: -*-
      ],
      entry_points={
            "console_scripts" : [
                  "crop_image = image_mosaic.crop_image:main",
                  "H_from_points = image_mosaic.H_from_points:main",
                  "Haffine_from_params = image_mosaic.Haffine_from_params:main",
                  "Haffine_from_points = image_mosaic.Haffine_from_points:main",
                  "image_in_image = image_mosaic.image_in_image:main",
                  "make_tiles = image_mosaic.make_tiles:main",
                  "transform_image = image_mosaic.transform_image:main",
                  "transform_points = image_mosaic.transform_points:main",
                  "warp_image = image_mosaic.warp_image:main",
                  "affine_from_points = image_mosaic.affine_from_points:main",
                  "image-warp-clicks = image_mosaic.image_warp_click:main",                  
                  "image-warp = image_mosaic.image_warp:main",
                  "blend-image = image_mosaic.blend_image:main",
                  "image-get-affine = image_mosaic.image_get_affine:main"              
            ]
            },
      )
