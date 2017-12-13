#!/usr/bin/env bash

# original image from http://sci.esa.int/hubble/58093-abell-s1063-the-final-frontier/
# 2243 x 2511 jpg image (on the right)

curl http://sci.esa.int/science-e-media/img/ed/heic1615a.jpg -o abells1063.jpg
convert abells1063.jpg abells1063.eps

