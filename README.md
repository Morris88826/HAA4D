# HAA4D

"HAA4D" is a challenging human action recognition 3D+T dataset that is built on top of the HAA500 dataset. The dataset is clean, diverse, class balanced, and the choice of atomic actions makes annotation even easier as each video clip lasts for only a few seconds. 

Paper can be downloaded in [here](https://cse.hkust.edu.hk/haa4d/images/paper.pdf).

Project Website: https://cse.hkust.edu.hk/haa4d

## Structures of the datasets
Currently, HAA4D consists of more than 3,300 4D skeletons in 300 human atomic action classes. The dataset include 4 different modalities of data:

* RGB videos
* 2D skeletal data
* 3D skeletal data
* Globally aligned skeletons

For RGB videos, it can be downloaded from https://www.cse.ust.hk/haa/ and put it in the video folder.

2D skeletal data, 3D skeletal data, and globally aligned skeletons can be downloaded in [here](https://cse.hkust.edu.hk/haa4d/download.html).

Here is the hierarchical structure of the dataset:

```
/dataset 
├── video
├── images 
├── skeletons_2d 
├── skeletons_3d 
├── processed_data
│ ├── globally_aligned_skeletons
│ │ ├── haa4d
│ │ ├── nturgb+d 
│ ├── normalized_skeletons_3d 
│ │ ├── primary_classes
│ │ ├── additional_classes
├── info.json
```
## Get Started
1. run getHAA500.py to get raw images from the video
```
python getHAA500.py -p action_name
```

2. To view the skeleton example, run demo.py
```
python demo.py
```
## Annotation Tool
Upcoming


## Citation
To cite our datasets, please use the following bibtex records:
```
@misc{tseng2022haa4d,
	title={HAA4D: Few-Shot Human Atomic Action Recognition via 3D Spatio-Temporal Skeletal Alignment}, 
	author={Mu-Ruei Tseng and Abhishek Gupta and Chi-Keung Tang and Yu-Wing Tai},
	year={2022},
	eprint={2202.07308},
	archivePrefix={arXiv},
	primaryClass={cs.CV}
}
```
