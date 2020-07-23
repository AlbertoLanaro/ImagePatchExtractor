import argparse
import glob
import os
from pathlib import Path

import jax.numpy as np
from sklearn.feature_extraction.image import extract_patches_2d
import imageio

# random seed is used to extract the same patch from input images and masks
RND_SEED = 44


def is_defective(mask_patch, th=0.01):
    """
    Check if @mask_patch is defective i.e. the percentage of white pixel is > @th
        - if the mask associated to the extracted patch is defective -> the patch is saved with a '*KO.png' extension
        - if the mask associated to the extracted patch is NOT defective -> the patch is saved with a '*OK.png' extension
    """
    return np.sum(
        mask_patch) > 255 * mask_patch.shape[0] * mask_patch.shape[1] * th


def create_patches(img_path, n, size, mask_path=None):
    """
    Load imgs and masks and extract @n random patches possibly with overlap. 
    If @mask_path is not set, only patch from input images are extracted
    """
    # load imgs
    input_img_list = glob.glob(os.path.join(img_path, '*'))
    print('Detected %d images from folder --> %s' %
          (len(input_img_list), os.path.abspath(img_path)))
    print(input_img_list)
    imgs = np.asarray([imageio.imread(f) for f in input_img_list])
    # extract patches
    imgs_patches = np.array(
        [extract_patches_2d(img, (size, size), n, RND_SEED) for img in imgs],
        dtype=np.uint8)
    # create folder to store patches
    imgs_patches_path = Path(img_path).parents[0].joinpath(
        os.path.basename(img_path) + '_patch')
    imgs_patches_path.mkdir(exist_ok=True)
    # save to folder
    if not (mask_path):
        print('No mask path has been specified...')
        [
            imageio.imwrite(
                os.path.join(
                    imgs_patches_path,
                    os.path.basename(im_path).split('.')[-2] + '_PATCH_' +
                    str(n) + '.png'),
                imgs_patches[id, n, :, :]) for id, im_path in zip(
                    range(imgs_patches.shape[0]), input_img_list)
            for n in range(imgs_patches.shape[1])
        ]
    else:
        # load masks
        input_mask_list = glob.glob(os.path.join(mask_path, '*'))
        print('Detected %d masks from folder --> %s' %
              (len(input_mask_list), os.path.abspath(mask_path)))
        masks = np.asarray([imageio.imread(f) for f in input_mask_list])
        # extract patches
        masks_patches = np.array([
            extract_patches_2d(mask, (size, size), n, RND_SEED)
            for mask in masks
        ],
                                 dtype=np.uint8)
        # create folder to store patches
        masks_patch_path = Path(mask_path).parents[0].joinpath(
            os.path.basename(mask_path) + '_patch')
        masks_patch_path.mkdir(exist_ok=True)
        for (id, m_path, im_path) in zip(range(masks_patches.shape[0]),
                                         input_mask_list, input_img_list):
            for n in range(masks_patches.shape[1]):
                curr_img_patch = imgs_patches[id, n, :, :]
                curr_mask_patch = masks_patches[id, n, :, :]
                if is_defective(curr_mask_patch):
                    imageio.imwrite(
                        os.path.join(
                            imgs_patches_path,
                            os.path.basename(im_path).split('.')[-2] +
                            '_PATCH_' + str(n) + '_KO.png'), curr_img_patch)
                    imageio.imwrite(
                        os.path.join(
                            masks_patch_path,
                            os.path.basename(m_path).split('.')[-2] +
                            '_PATCH_' + str(n) + '_KO.png'), curr_mask_patch)
                else:
                    imageio.imwrite(
                        os.path.join(
                            imgs_patches_path,
                            os.path.basename(im_path).split('.')[-2] +
                            '_PATCH_' + str(n) + '_OK.png'), curr_img_patch)
                    imageio.imwrite(
                        os.path.join(
                            masks_patch_path,
                            os.path.basename(m_path).split('.')[-2] +
                            '_PATCH_' + str(n) + '_OK.png'), curr_mask_patch)


def main():

    # parse command line arguments
    parser = argparse.ArgumentParser(
        description=
        'Patch extractor. Extract patch from a set of images (and from their associated masks [optionally]) and save them.'
    )
    parser.add_argument('-i',
                        '--input_imgs_path',
                        help='Path to input images',
                        type=str,
                        required=True)
    parser.add_argument('-m',
                        '--input_masks_path',
                        help='Path to image masks',
                        type=str,
                        default=None)
    parser.add_argument('-N',
                        '--n_patches',
                        help='Number of patches to be extracted',
                        type=int,
                        default=None)
    parser.add_argument(
        '-s',
        '--patch_size',
        help='Patches size will be: ($patch_size, $patch_size)',
        type=int,
        required=True)
    args = parser.parse_args()

    create_patches(args.input_imgs_path, args.n_patches, args.patch_size,
                   args.input_masks_path)


if __name__ == "__main__":
    main()
