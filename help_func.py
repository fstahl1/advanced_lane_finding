import matplotlib.pyplot as plt
import numpy as np
import cv2



# def draw_lines(img, lines, color=[255, 0, 0], thickness=3):
# #     import pdb; pdb.set_trace()
#     for line in lines:
#         if np.all(line == 0): break
#         else:
#             for x1, y1, x2, y2 in line:
#                 cv2.line(img, (x1, y1), (x2, y2), color, thickness)          



def draw_lines_from_points(img, pts, color=[255, 0, 0], 
                           thickness = 3):
    pts = pts.reshape((4,2))
    cv2.line(img, (pts[0, 0], pts[0, 1]), (pts[1, 0], pts[1, 1]), 
             color, thickness)
    cv2.line(img, (pts[0, 0], pts[0, 1]), (pts[1, 0], pts[1, 1]), 
             color, thickness)
    cv2.line(img, (pts[1, 0], pts[1, 1]), (pts[2, 0], pts[2, 1]), 
             color, thickness)
    cv2.line(img, (pts[3, 0], pts[3, 1]), (pts[0, 0], pts[0, 1]), 
             color, thickness)
    return None


def show_img(img, cmapval=None, ttl=''):
    plt.imshow(img, cmap=cmapval)
    plt.title(ttl)
    plt.show()
    return None


def show_imgs(imgs, cmaps, ttls, nrows=3, ncols=2, width=10, height=5, res=100):

    fig, ax = plt.subplots(nrows, ncols, figsize=(width, height), dpi=res)
    ax = ax.ravel()
  
    for i in range(len(imgs)):
        img = imgs[i]
        cmapval = cmaps[i]
        ttl = ttls[i]
        ax[i].imshow(img, cmap=cmapval)
        ax[i].set_title(ttl)
  
    for i in range(nrows * ncols):
        ax[i].axis('off')
    
#     if save==True:
#         fig.savefig(path)
#     fig.savefig('output_images/test.jpg')
#     return fig
    return None


def create_comb_img(main_img, side_img1_in, side_img2_in, side_img3_in, side_img4_in, side_img5_in):

    main_shape = main_img.shape

    # prepare images
    final_shape = (int(main_shape[0]*1.5), int(main_shape[1]*1.5),3)
    half_shape = (main_shape[0]//2, main_shape[1]//2)
    final_img = np.zeros(final_shape, dtype=main_img.dtype)

    side_img1 = cv2.resize(side_img1_in, half_shape[::-1])
    if len(side_img1.shape)==2:
        side_img1 = side_img1*255
        side_img1 = np.dstack((side_img1, side_img1, side_img1))

    side_img2 = cv2.resize(side_img2_in, half_shape[::-1])
    if len(side_img2.shape)==2:
        side_img2 = side_img2*255
        side_img2 = np.dstack((side_img2, side_img2, side_img2))

    side_img3 = cv2.resize(side_img3_in, half_shape[::-1])
    if len(side_img3.shape)==2:
        side_img3 = side_img3*255
        side_img3 = np.dstack((side_img3, side_img3, side_img3))

    side_img4 = cv2.resize(side_img4_in, half_shape[::-1])
    if len(side_img4.shape)==2:
        side_img4 = side_img4*255
        side_img4 = np.dstack((side_img4, side_img4, side_img4))
        
    side_img5 = cv2.resize(side_img5_in, half_shape[::-1])
    if len(side_img5.shape)==2:
        side_img5 = side_img5*255
        side_img5 = np.dstack((side_img5, side_img5, side_img5))

    # fill final image
    # main image
    final_img[-main_shape[0]:,-main_shape[1]:] = main_img
    # side image 1 (top left)
    final_img[:-main_shape[0],:-main_shape[1]] = side_img1
    # side image 2 (top middle)
    final_img[:-main_shape[0],-main_shape[1]:main_shape[1]] = side_img2
    # side image 3 (top right)
    final_img[:-main_shape[0],main_shape[1]:] = side_img3
    # side image 4 (left mid)
    final_img[-main_shape[0]:main_shape[0],:-main_shape[1]] = side_img4
    # side image 5 (left bottom)
    final_img[main_shape[0]:,:-main_shape[1]] = side_img5

    return final_img