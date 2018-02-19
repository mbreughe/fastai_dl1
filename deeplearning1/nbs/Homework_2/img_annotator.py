import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

def get_bb_coords(fname):
    # Simple mouse click function to store coordinates
    def onclick(event):
        global ix, iy
        ix, iy = event.xdata, event.ydata
        
        #print ix, iy
        ## Cap the coordinates:
        #ix = min(max(0, ix), x_max)
        iy = min(max(0, iy), y_max)
        #print "--->"
        #print ix, iy
        
        ax.scatter(ix,iy,c="r" )
        fig.canvas.draw()

        if (not ix is None) and (not iy is None):
            coords.append((ix, iy))

        # Disconnect after 2 clicks
        if len(coords) == 4:
            fig.canvas.mpl_disconnect(cid)
            plt.close(1)
        return
        
    img = imageio.imread(fname)
    x_max = img.shape[1]
    y_max = img.shape[0]

    fig, ax = plt.subplots(1,1)
    ax.imshow(img)

    coords = []

    # Call click func
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show(1)
    
    print coords
    return coords
    
def label_images(img_dir, label_fname):
    label_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), label_fname)
    
    existing_labels = []
    if os.path.exists(label_file):
        with open(label_file) as ifh:
            for line in ifh:
                img_fname = str((line.strip().split(","))[0]).strip("\"")
                existing_labels.append(img_fname)
    
    if len(existing_labels) > 0:
        print "Appending to existing label file which had the following information:"
        print existing_labels
        
    imgs = os.listdir(img_dir)
    np.random.shuffle(imgs)
    with open(label_file, 'a') as ofh:
        for fname in imgs:
            if (not fname.endswith(".jpg")) or fname in existing_labels:
                continue
            
            print "Annotating image " + fname
            coords = get_bb_coords(os.path.join(img_dir, fname))
            line = "\"" + fname + "\"" + ", " + str(coords) + "\n"
            ofh.write(line)
            
def read_label_file(fname):
    labels = dict()
    with open(fname) as ifh:
        for line in ifh:
            naam, lijst = eval(line)
            labels[naam] = lijst
            
    return labels

if __name__ == "__main__":    
    img_dir = "."
    fname = "bb_coords.csv"
    label_images(img_dir, fname)

                
            

