
---


# Writeup: Advanced Lane Finding

## Udacity - Self Driving Car Nanodegree Project


---

#### In the course of this project, the following steps were completed:

* Camera calibration
* Distortion correction
* Creation of a thresholded binary image using color transform and gradients
* Perspective transform (Warp)
* Identification of lane-line pixels and polynomial fit
* Curve radius and offset calculation
* Creating an overlay with the detected lane

---

#### Final result

With the implemented pipeline lane-line were reliably detected:

![final_gif](./output_videos/final_subclip.gif)


## Camera calibration

For distortion correction of an image, the camera matrix and distortion coefficients are required. They are calculated using the openCV function `cv2.calibrateCamera()` (*code cell 3, line 31*), which takes real world 3D object points (x,y,z) and 2D image points (x,y) of the calibration pattern as input arguments.

Since the use of more than 10 calibration images is recommended ([openCV documentation](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html)), all of the provided 20 images are used. The respective object and image points of the individual images are simply appended and then passed to the calibration function.

Since the chessboard pattern is assumed to be fixed at the (x,y) plane at z=0, the object points for all 9x6 calibration images defined as $(0,0,0), (1,0,0), ... (8,5,0)$ (*code cell 3, line 1-5*).
The image points are determinded by the `cv2.findChessboardCorners()` (*code cell 3, line 20*), which outputs the 2D-coordinates of all chessboard corners from the input image.

Distorted images taken with the same camera can now be corrected by using the `cv2.undistort()` function, which takes the calibration matrix and distortion coefficients as input arguments. It is used in *code cell 3, line 33*. The output is provided below.

![png](01_calib_img.png)



## Pipeline (test images)


### Example of a distortion-corrected image.

Now that the calibration matrix and distortion coefficients are available, all images taken with the same camera can be undistorted. The result of the function `cv2.undistort()` is shown below.

![png](02_dist_corr_img.png)


### Perspective transform

A perspective transform requires a transformation matrix which can be computed using the `cv2.getPerspectiveTransform()` function (*code cell 12, line 2*). This function takes 4 source points and 4 destination points as input and returns the transformation matrix. The source points are manually chosed based on a zoomed image:
 
| Source points (x,y)| Destination points (x,y) |
|: --- :|: --- :|
|  580, 460 | 290,   0 |
|  700, 460 | 990,   0 |
| 1100, 720 | 990, 720 |
|  200, 720 | 290, 720 |
 
Since the region of interest represents a rectangle on the road, the destination points are chosen to form a rectange as well:
 
With the selected points, a perspective transform can be performed, which leads to a bird's eye view.
In case of changing source and image points before passing them to the `cv2.getPerspectiveTransform()` function, the output is a matrix for transforming from bird's eye view back to the original perspective (*code cell 12, line 3*).

The transform is performed using the `cv2.warpPerspective()` function (*code cell 14, line 2*), which takes the image and the transformation matrix as inputs and returns the transformed ("warped") image. An example of a transformed image is shown below. Since the lane lines appear parallel on the warped image, the transform is assumed to work properly.

![png](warp.png)




### Creation of a thresholded binary image using color transforms and gradients

To create a thresholded binary image, a combination of gradients and color transforms has been used. Both methods are described below.

#### Gradients

For creating a binary gradient image, the function `grad_thresh()` was defined (*code cell 18*). It first transforms the RGB image into a grayscale with `cv2.cvtColor()` (*code cell 18, line 7*), and then applies the [sobel operator](https://en.wikipedia.org/wiki/Sobel_operator) by using `cv2.Sobel()` (*code cell 18, line 9-12*), to get an image of the gradient in either x or y direction. The sobel function takes a grayscale image, the required datatype, the direction and the kernel size as input arguments.  
Since the output of the sobel function can be both positive and negative (depending on if the transition is from bright-to-dark or from dark-to-bright), a high, signed datatype of float 64 (cv2.CV_64F) is used first [openCV documentation](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_gradients/py_gradients.html). After calculating the absolute value (so both edges can be found), the image is converted to 8-bit unsigned integer.  
Since the lane lines are assumed to appear mostly vertical in the warped images, only the gradient in x direction was used. A kernel size of 3 provided good detection results.

To get the binary image, a blank one-channel image with the x and y dimensions of the original image is created first (*code cell 18, line 17*). Then the threshold is applied by setting the blank image to 1 where the values of the gradient image are above the low threshold and below the high threshold values.


#### Color transforms

To create a color threshold binary image, both [RGB](https://en.wikipedia.org/wiki/RGB_color_model) (Red, Green, Blue) and [HLS](https://en.wikipedia.org/wiki/HSL_and_HSV) (Hue, Saturation, Lightness) color spaces are used. The function `rbg_color_thresh()` (*code cell 20*) is defined to create a binary image based on the RGB channels, while  `hls_color_thresh()` (*code cell 21*) does the same for an HLS image.  

In both cases a blank image is created first and set to 1 where the value of the color channel is above the low threshold and below the high threshold (as with the binary gradient image before). For the binary HLS image, the original RGB image must be converted to HLS, of course (`cv2.cvtColor()`, *code cell 21, line 4*).

#### Combination

To combine color and gradient binary images, the function `create_bin_img()` (*code cell 24*) is defined, which uses bitwise operations on images. Good results have been achieved by using the following bitwise combination:

RGB-Red **OR (** HLS-Saturation **AND** HLS-Hue **) OR** Gradient

An example of the binary combined color image and gradient image is shown below.

![png](04_bin_img.png)



### Identification of lane-line pixels polynomial fit

To identify lane-line pixels, two different methods are used. First, a sliding window approach is applied, which returns the pixel values of potential lane-lines. After fitting a polynomial and a check if the result is plausible, a more efficient proximity search around the previous fit is performed in the next frame. Both methods are described below.

#### Sliding window search

The `sliding_window()` function is defined in *code cell 30*. The method starts with calculating a histgram, which sums up the number of pixels in every column for the lower half of the binary image. An example histogram is shown below. After splitting the histogramm into left and right for both lines (*code cell 30, line 9*), its left and right maximum values are used as starting points for the sliding windows (*code cell 30, line 11-14*), since it is likely to find the lines in this area. The image is searched from bottom to top with the sliding windows, which are adapted horizontally if the mean values of the detected pixels change (*code cell 30, line 44-52*). Since the method is implemented with a for loop, it is relatively inefficient. An example image with the line pixels marked in red and blue is shown below the histogram.


#### Proximity search

To avoid the relatively slow sliding window search, `proximity_search()` is applied if possible, which is defined in *code cell 37*. The use of the function requires, that a line was found and successfully fit in the frame before, since the fitted polynomial is used for this method. It searches the lines only in the area of the fitted polynomial from the previous frame and returns its pixel values.

#### Polynomial fit

To fit a polynomial, the function `fit_poly()` is defined (*code cell 34*). It basically uses the `np.polyfit()` function to fit a 2nd order polynomial and return its coefficients (*code cell 34, line 6*). Since the lane-lines are assumed to be vertical in the transformed images, x and y are switched here.
After creating the y and x values of the polynomial (*line 9-10*), the x values are limited in case of a fit that exceeds the image bounds (*line 13-14*). An example of the fitted polynomial lines is shown below the histogram and the marked pixel image.

![png](05_hist.png)

![png](06_marked_pix.png)

![png](07_poly_img.png)




### Radius of lane curvature and the position of the vehicle with respect to the lane center

The radius of a curve is calculated by using
$R_{curve} = \frac{\big[1 + (\frac{dy}{dx})²\big]^{3/2}}{\lvert\frac{d²y}{dx²}\rvert}$ [\[https://www.intmath.com\]](https://www.intmath.com/applications-differentiation/8-radius-curvature.php).

Assuming the 2nd order polynomial curve $f(y) = Ay² + By + C$ and their derivatives $f'(y) = 2Ay + B$ and $f''(y) = 2A$, this leads to

$R_{curve} = \frac{\big[1 + (2 Ay + B)²\big]^{3/2}}{\lvert2A\rvert}$.
This formular is used in the `get_radius()` function *code cell 39, line 6-8*. The radius is calculated at the bottom of the image, since this is the closest approximation to the current position of the car.

The distance to the lane center results from the difference between the calculated lane center and the middle of the image, which can be seen in function `get_offset()` (*code cell 40, line 4-8*). By definition, a negative offset means a car position left from the lane center.

For converting the measures from pixel to real world space, conversion coefficients for x and y directions are required (`xm_per_pix` and `ym_per_pix` in *code cell 38, line 8 and 15*). Their values have been determined based on the warped image above, assuming a lane width of 3.7 meters and a dashed line length of 3 meters.



### Example image the result plotted back down onto the road

For plotting the result on the road, an overlay has been created 

![png](08_overlay.png)


### Final video output

Here is the link to the [complete video](./output_videos/project_video.mp4).

The following gif shows a debug video, with the binary color image (bottom left), the binary gradient image (center left) and the combinated binary image (top left). The main image is shown bottom right with the fitted lane lines above:

![final_gif](./output_videos/final_subclip_debug.gif)


### Discussion

The algorithm fails under harder conditions, for example when there are shadows or other lines from the road parallel to the lane lines.

Recent line detections are used in the current implementation for smoothing the lines. Besides the implemented sanity check, these history values could be used to check if the lines are plausible as well. Generally, the implemented sanity check could be improved to filter wrong detections.

For a better detection performance, the used threshold methods could be improved by other combination of colormaps and gradients and tuning the appropriate thresholds.