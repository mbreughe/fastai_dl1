from matplotlib import pyplot as plt
import imageio
from scipy import ndimage
import math
import numpy as np

##
# @brief: Crop image ifname and store to ofname
# @param ifname: input file name
# @param ofnmae: output file name
# @param bb_dots: four dots defining the bounding box of what needs to be cropped
# @verbose: visualize the cropping process
def crop_and_save_img(ifname, ofname, bb_dots, verbose=False):
    tl, tr, br, bl = bb_dots
    img = imageio.imread(fname)
    
    theta = calc_rot_angle(tl, tr, br, bl)
    r_img, r_details = rotate_img(img, theta)
    cr_img = crop_rotated_img_four_dots(r_img, rotate_dots([tl, tr, br, bl], theta, r_details[0], r_details[1]))
    
    imageio.imwrite(ofname, cr_img)
    
    if verbose:
        fig,axes = plt.subplots(2,2)
        dbg_add_img_and_dots(axes[0,0], img, [tl, tr, br, bl])
        dbg_add_img_and_dots(axes[0,1], r_img, rotate_dots([tl, tr, br, bl], theta, r_details[0], r_details[1]))
        dbg_add_img_and_dots(axes[1,0], cr_img, [])
        
        plt.show()

##
# @brief: Crop a rectangular patch, which is parallel with the image itself.
# @param: img_array: array containing pixels
# @param top_l, bottom_r: two tuples with respectively coordinates of top left pixel and bottom right pixel
def crop_img(img_array, top_l, bottom_r):
    return img_array[top_l[1]:bottom_r[1], top_l[0]:bottom_r[0]]

    
##
# @brief: Crop a rectangular patch with any orientation out of the image
# @param: img_array: array containing pixels
# @param: dots -- four dots defining the bounding box
def crop_rotated_img_four_dots(img_array, dots):
    top_l = [min(xy[0] for xy in dots), min(xy[1] for xy in dots)]
    bottom_r = [max(xy[0] for xy in dots), max(xy[1] for xy in dots)]
    
    return crop_img(img_array, top_l, bottom_r)

##
# @brief: calculate the angle to rotate the image over before cropping
# @param: tl, tr, br and bl are tuples containing respectively top left, top right, bottom right and bottom left pixels     
def calc_rot_angle(tl, tr, br, bl):
    adj = bl[1] - tl[1]
    opp = bl[0] - tl[0]
    tan = opp/adj
    theta = math.degrees(math.atan(tan))
    return theta
    
## 
# @brief: Rotate an image and get rotation details
# @note: rotation details are needed to perform coordinate transformations efficiently
def rotate_img(image_arr, angle):
    im_rot = ndimage.rotate(image_arr,angle)
    org_center = (np.array(image_arr.shape[:2][::-1])-1)/2.
    rot_center = (np.array(im_rot.shape[:2][::-1])-1)/2.
    
    return im_rot, [org_center, rot_center]

##
# @brief: perform the necessary actions to rotate a coordinate
# @note: i.e, translate it to the center of the image, perform rotation, translate to new coordinates (with new center of img).
def rotate_xy_fast(xy, angle, org_center, rot_center):
    xy_org = xy-org_center
    a = np.deg2rad(angle)
    xy_rot_new = np.array([xy_org[0]*np.cos(a) + xy_org[1]*np.sin(a),
            -xy_org[0]*np.sin(a) + xy_org[1]*np.cos(a) ])
    xy_rot = xy_rot_new + rot_center
    return xy_rot.astype(int)
    
def rotate_dots(dots, angle, org_center, rot_center):
    new_dots = []
    for xy in dots:
        new_dots.append(rotate_xy_fast(xy, angle, org_center, rot_center))
        
    return new_dots
    
def dbg_add_img_and_dots(ax, img_arr, dots, colors=['r', 'g', 'y', 'b']):
     ax.imshow(img_arr)
     for i in xrange(len(dots)):
        x,y = dots[i]
        ax.scatter(x,y, c = colors[i])

def dbg_show_img_and_dot(data_orig, xy, theta):
    x0, y0 = xy
    fig,axes = plt.subplots(2,2)

    axes[0,0].imshow(data_orig)
    axes[0,0].scatter(x0,y0,c="r" )
    axes[0,0].set_title("original")

    for i, angle in enumerate([66,-32,theta]):
        data_rot, (x1,y1) = dbg_rot(data_orig, np.array([x0,y0]), angle)
        axes.flatten()[i+1].imshow(data_rot)
        axes.flatten()[i+1].scatter(x1,y1,c="r" )
        axes.flatten()[i+1].set_title("Rotation: {}deg".format(angle))

    plt.show()
    
def dbg_rot(image, xy, angle):
    im_rot = ndimage.rotate(image,angle) 
    org_center = (np.array(image.shape[:2][::-1])-1)/2.
    rot_center = (np.array(im_rot.shape[:2][::-1])-1)/2.
    org = xy-org_center
    a = np.deg2rad(angle)
    new = np.array([org[0]*np.cos(a) + org[1]*np.sin(a),
            -org[0]*np.sin(a) + org[1]*np.cos(a) ])
    return im_rot, new+rot_center
    
if __name__ == "__main__":
    fname = "w_59.jpg"
    
    tl = (500, 800)
    tr = (980, 380)
    br = (2400, 1200)
    bl = (2000, 1800)
    
    crop_and_save_img(fname, "teelbal.jpg", [tl, tr, br, bl], verbose=True)
    






    
