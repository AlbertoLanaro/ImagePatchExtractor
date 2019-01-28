import argparse
import glob
import os
from pathlib import Path

import jax.numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from sklearn.feature_extraction.image import extract_patches_2d

# random seed is used to extract the same patch from input images and masks
RND_SEED = 44

def create_patches(img_path, n, size, rnd_seed):
    # load imgs
    input_img_list = glob.glob(os.path.join(img_path, '*'))
    print('Detected %d images from folder --> %s' % (len(input_img_list), os.path.abspath(img_path)))
    imgs = np.array([misc.imread(f) for f in input_img_list])
    # extract patches
    imgs_patches = np.array([extract_patches_2d(img, (size, size), n, random_state=rnd_seed) for img in imgs], dtype=np.uint8)
    # create folder to store patches
    patch_path = Path(img_path).parents[0].joinpath(os.path.basename(img_path) + '_patch')
    patch_path.mkdir(exist_ok=True)
    # save to folder
    [misc.imsave(os.path.join(patch_path, os.path.basename(im_path).split('.')[-2] + '_PATCH_' + str(n) + '.png'), imgs_patches[id,n,:,:]) for id,im_path in zip(range(imgs_patches.shape[0]), input_img_list) for n in range(imgs_patches.shape[1])]

def main():

    # parse command line arguments
    parser = argparse.ArgumentParser(description='Patch extractor. Extract patch from a set of images (and from their associated masks [optionally]) and save them.')
    parser.add_argument('-i', '--input_imgs_path', help='Path to input images', type=str, required=True)
    parser.add_argument('-m', '--input_masks_path', help='Path to image masks', type=str, default=None)
    parser.add_argument('-N', '--n_patches', help='Number of patches to be extracted', type=int, default=None)
    parser.add_argument('-s', '--patch_size', help='Patches size will be: ($patch_size, $patch_size)', type=int, required=True)
    args = parser.parse_args()

    create_patches(args.input_imgs_path, args.n_patches, args.patch_size, RND_SEED)   
    # if any input masks path is passed
    if args.input_masks_path:
        create_patches(args.input_masks_path, args.n_patches, args.patch_size, RND_SEED)

if __name__ == "__main__":
    main()
