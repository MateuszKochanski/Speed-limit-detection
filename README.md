# Speed-limit-detection
This is a Python script for detecting speed limits on road signs.

## Usage

Select the image with the speed limit sign and place the path to the file in line 5 of the code. 
```python
img = cv2.imread('zdjeciaWMA/zdj1.jpg')
```
After running the script, you should see what the speed limit value is.

## Example
When you choose this image:  
  
![Text](https://github.com/MateuszKochanski/Speed-limit-detection/blob/master/zdjeciaWMA/zdj1.jpg)  
  
You will get the following result:
```
Ograniczenie prędkości do 40 km/h
```
## How it work
All steps of the algorithm are described in the algorithm.pdf file.

## Used

[openCV](https://opencv.org/)
