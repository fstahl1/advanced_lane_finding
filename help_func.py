import matplotlib.pyplot as plt
import cv2


def plot(img):
    plt.figure()
    plt.imshow(img)
    return None

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
    