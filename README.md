# Image_Viewer_Data_Converter
Scripts for converting images to the compatible format for the CIL Image Viewer


## Requirements
* Python3
  * numpy
  * sckit-image
  * joblib
* PHP 7.2+
  * Sqlite
* IMOD
* GDAL (gdal2tiles.py)


### Convert images to the sqlite files for the CIL Image Viewer
```
python3 conver2galNsqlite.py INPUT_IMAGE_FOLDER OUTPUT_GDAL_FOLDER OUTPUT_SQLITE_FOLDER
```

Assumption: The image name contains the Z slice index number. For example, "temp.0000.tif"



### Convert images to the GDAL tile images
```
python3 conver2gal.py INPUT_IMAGE_FOLDER OUTPUT_GDAL_FOLDER
```
