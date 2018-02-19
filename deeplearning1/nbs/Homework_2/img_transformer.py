import img_annotator as IA
import os
from img_manipulation import crop_and_save_img

if __name__ == "__main__":
    labels = IA.read_label_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "bb_coords.csv"))
    
    out_dir = "cropped"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    for fname in labels.keys():
        dots = labels[fname]
        crop_and_save_img(fname, os.path.join(out_dir, fname), dots)