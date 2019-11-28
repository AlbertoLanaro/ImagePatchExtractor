# Patch Extractor with Masks

Simple python script that extract a given number of overlapping patches from a set of images and their corresponding masks (optionally).
The script can be run with several input parameters:
- `--input_imgs_path`: path to images folder [`str` - required]
- `--input_masks_path`: path to masks folder [`str` - optional]
- `--n_patches`: number of extracted patches per image. If `None`, the maximum number of patches is extracted [`int` - optional].
- `--patch_size`: patch dimensions, i.e. `(patch_size, patch_size)` [`int` - required]

## Dependencies
All the dependencies are detailed in the `requirements.txt` file and can be installed with `pip` and the following command:
```pip3 install -r requirements.txt```

## Example

Here are two examples of patches extracted from a set if images and their correnspondent masks:

![](https://github.com/AlbertoLanaro/ImagePatchExtractor/blob/master/samples/0b918fa2-9113-47f6-80b1-b3fca845686d_PATCH_1_KO.png?raw=true)  ![](https://github.com/AlbertoLanaro/ImagePatchExtractor/blob/master/samples/0e80d63d-ebd8-4eb1-a2e0-f5d2c5913761_PATCH_0_KO.png?raw=true) 
![](https://github.com/AlbertoLanaro/ImagePatchExtractor/blob/master/samples/0b918fa2-9113-47f6-80b1-b3fca845686d_PATCH_1_KO_MASK.png?raw=true) ![](https://github.com/AlbertoLanaro/ImagePatchExtractor/blob/master/samples/0e80d63d-ebd8-4eb1-a2e0-f5d2c5913761_PATCH_0_KO_MASK.png?raw=true)
