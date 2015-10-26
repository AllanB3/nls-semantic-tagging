#!/bin/sh

echo "Extract alphabetical index"
pdftk 85920425.6-BW-1910.pdf cat 45-482 output 85920425.6-BW-1910-ALPHA-INDEX.pdf
pdftk 85920425.23-RGB-1910.pdf cat 45-482 output 85920425.23-RGB-1910-ALPHA-INDEX.pdf