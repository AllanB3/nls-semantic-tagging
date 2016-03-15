#!/bin/sh
mkdir segmentation
cp $@ segmentation
cd segmentation

echo "Convert PDF into PPM..."
pdftoppm -f $2 -l $3 -r 400 $1 SPOD
echo "Done"

echo "Convert PPM into TIF..."
for i in *.ppm; do convert "$i" "`basename "$i" .ppm`.tif"; done
echo "Done"

echo "Convert TIF into PNG..."
for i in *.tif; do convert "$i" "`basename "$i" .tif`.png"; done
echo "Done"

mkdir png-spod
mv *.png ./png-spod/

#echo "Convert TIF into JPG..."
#for i in *.tif; do convert "$i" "`basename "$i" .tif`.jpg"; done
#echo "Done"

#mkdir jpg-spod
#mv *.jpg ./jpg-spod/

# SCRIBO: generate XML and segmentation images
echo "Segmentation of TIF images and creation of XML files..."
for i in *.tif; do scribo-cli doc-dia "$i" "`basename "$i" .tif`.xml --debug-regions "`basename "$i" .tif`"-regions.png"; done
echo "Done"

mkdir regions
# improve the contrast of the segmented image
for i in *.png; do convert -brightness-contrast 35x15  "$i" regions/"$i"; done

mkdir xml-segmentation
mv *.xml ./xml-segmentation/
echo "Done"

echo "Remove PPM files..."
rm *.ppm
echo "Done"

echo "Remove TIF files..."
rm *.tif
echo "Done"

echo "Remove PNG files..."
rm *.png
echo "Done"