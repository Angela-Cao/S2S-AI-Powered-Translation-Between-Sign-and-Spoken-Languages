# S2S: AI-Powered Translation Between Sign and Spoken Languages




## Useful links

<div align="center">
    <a href="https://youtu.be/R3M-wiifcCs" class="button"><b>[YouTube Link]</b></a> 
        <a href="https://youtu.be/ZTU_QdGwDts" class="button"><b>[Demo]</b></a> &nbsp;&nbsp;&nbsp;&nbsp;
</div>


## 




## Data preprocessing

- ```preprocess_asllrp_data_new.py``` new preprocessing the ASLLRP 518 video clips using mp4 --> csv --> png. The png files were generated for each frame from the video. 

### Extract keypoints of skeleton from the video data

-  ```video_to_csv.py``` Convert a video to skeleton keypoints data (csv). The function ```sample_and_export``` in this file is the old way to sample images from the video: get 4 samples from the (0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6, 0.65) from the video. 
-  ```video_to_csv_asllrp.py``` The same ```video2csv``` function as the one in ```video_to_csv.py```. A different way to ```sample_and_export``` to get the samples from the ASLLRP video. Since the word videos are short, the samples were taken from the durations (0, 0.2), (0.2, 0.5), (0.5, 0.8), (0.8, 1) of the videos. 

### Generate skeleton images from the keypoints data 

- ```pose_to_img_2.py``` Generate images for each frame from the csv file if at least one hand can be detected on this frame of the video.

### Sample from the frames of the video and combine the 4 sampled skeleton images as one image

- ```combine_png_ASLLRP.py```  Given a list of images with the file names ending with gloss_video_name\_sample\_[].png, combine the 4 samples for the same gloss\_video\_name. 
- ```combine_png_WLASL.py```  Given a list of images with the file names ending with gloss_video_name\_sample\_[].png, combine the 4 samples for the same gloss\_video\_name. 
- ```csv2png.py``` old file for generating image (png) file from the skeleton keypoints data. This is the old version which first generate svg files from an csv file, and then convert it to the png file.  

## Sign LoRA ViT classifier
- ```train_timm_asl.py``` Fine tune LoRA ViT from a base model, such as ViT_base_patch16_224 using preprocessed image data. Usage example:

```
python train_timm_asl.py -bs 32 -data_path '../data/WLASL_pngs_organized'  -epochs 10 -num_classes 2002 -use_WLASL2000 True
```


## Segmentation

- ```segmentation_using_classifier.py``` the latest segmentation model.
- ```test_segmentation.py``` run experiments for sentence segmentation. Usage example:

```
python test_segmentation.py
```


## Translate sequence of glosses to spoken English

- ```spoken_asl_fine_tuning.ipynb`` Fine-tune BART model "facebook/bart-large" to translate glosses to spoken English. 



## Credit
- ViT code and imagenet pretrained weight come from ```lukemelas/PyTorch-Pretrained-ViT```
- LoRA ViT code was modified from ```JamesQFreeman/LoRA-ViT```