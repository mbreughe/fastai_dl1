#!/home/ubuntu/anaconda2/bin/python
from collections import defaultdict
import os
import sys
import numpy as np
import shutil

def read_label_mapping(l_file):
    l_dict = defaultdict(list)
    with open(l_file) as ifh:
        for line in ifh:
            (f, l) = line.strip().split(",")
            l_dict[l].append(f)

    return l_dict

def move_to_label_dirs(l_map, dirname):
    for k in l_map.keys():
        k_dir = os.path.join(dirname, k)

        # create a directory for every label
        mkdir_safe(k_dir)

        # For every img with this label, attempt to move it
        for f in l_map[k]:
            src_path = os.path.join(dirname, f)
            dst_path = os.path.join(k_dir, f)
            if os.path.exists(src_path):
                os.rename(src_path, dst_path)

def reorganize_dir(l_map, dirname, val_frac):
    if val_frac > 0.5:
        print "validation fraction should be smaller than 0.5"
        sys.ext(-1)

    # Create test/val/train dirs
    test = os.path.join(dirname, "test")
    train = os.path.join(dirname, "train")
    val = os.path.join(dirname, "val")

    mkdir_safe(test)
    mkdir_safe(train)
    mkdir_safe(val)

    labelled_imgs = []
    for v in l_map.values():
        labelled_imgs.extend(v)

    imgs = find_jpgs(dirname)
    
    # Move unlabelled imgs to test directory
    for f in imgs:
        if not f in labelled_imgs:
            src_path = os.path.join(dirname, f)
            dst_path = os.path.join(test, f)
            os.rename(src_path, dst_path)

    # For all remaining (i.e., labelled images), 
    # select per label (!!!) randomly which ones go in validation and which in train
    # This is important because we want at least 1 whale per label during training
    move_to_label_dirs(l_map, dirname)

    # In the sample set, some whale types are not present
    # keep track of that here
    no_whales_found = []
    for label in l_map.keys():
        label_dir = os.path.join(dirname, label)
        if not os.path.exists(label_dir):
            continue

        imgs = find_jpgs(label_dir)
        img_cnt = len(imgs)

        if img_cnt == 0:
            no_whales_found.append(label)
            shutil.rmtree(label_dir)
            continue 

        val_cnt = int(val_frac * img_cnt)
        trn_cnt = img_cnt - val_cnt
        print img_cnt, val_cnt, trn_cnt
        assert(trn_cnt >= 1)

        # Randomly pick images for the validation set of this label
        if val_cnt > 0:
            label_val = os.path.join(val, label)
            mkdir_safe(label_val)
            shuf = np.random.permutation(imgs)
            for i in range(val_cnt): os.rename(os.path.join(label_dir, shuf[i]), os.path.join(label_val, shuf[i]))

        # Move all remaining images to the training set
        shutil.move(label_dir, os.path.join(train))

    print "Reorganized directory. Did not find the following whales: "
    print no_whales_found

def find_jpgs(dirname): 
    imgs = []
    for f in os.listdir(dirname):
        if f.endswith(".jpg"):
            imgs.append(f)
    return imgs


def mkdir_safe(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

if __name__ == "__main__":
    print "Hello Texas"
    label_file = "train.csv"
    labels = read_label_mapping(label_file)
    reorganize_dir(labels, "imgs_subset", val_frac = 0.5)
