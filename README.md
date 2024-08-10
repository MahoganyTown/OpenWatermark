## OpenWatermark
OpenWatermark is a very simple and small program that you can use to stamp your files. It allows you to add a watermark on PDF documents as well as images. It is only available through CLI. It is particularly useful for protecting documents that contain sensitive information like ID, passport, birth certificate...

## Installation
Run the following command in a terminal:
```
pip install -r requirements.txt
```
You need Python 3.9 to install all the dependencies.

## Usage
Run the program using CLI:
```
python src/openwatermark.py file1.png file2.pdf -t "My Awesome Watermark"
```

Just input the list of files to watermark and the text to write. You can also specify other argument:
```
-c: color in format R,G,B,A each channel inside 0-255. Example: -c 39,89,182,90
```
```
-f: font name without extension (need font file in res/fonts). Example: -f Geneva
```
```
-p: pages to edit for PDF documents. Example: 1,2,3. By default, all pages will be edited.
```

## Requirements
- python 3.9.19
- pillow
- img2pdf
- pypdf2
- pikepdf
