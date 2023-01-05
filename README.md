# HAA4D

"HAA4D" is a challenging human action recognition 3D+T dataset that is built on top of the HAA500 dataset. The dataset is clean, diverse, class balanced, and the choice of atomic actions makes annotation even easier as each video clip lasts for only a few seconds. 

Paper can be downloaded in [here](https://cse.hkust.edu.hk/haa4d/images/paper.pdf).

Project Website: https://cse.hkust.edu.hk/haa4d

## Structures of the dataset
Currently, HAA4D consists of more than 3,300 4D skeletons in 300 human atomic action classes. The dataset include 4 different modalities of data:

* RGB videos
* 2D skeletal data
* 3D skeletal data
* Globally aligned skeletons

For RGB videos, it can be downloaded from https://www.cse.ust.hk/haa/

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
├── info.json
```


* 2D skeletal data can be generated from AlphaPose[1] or by human labeling. For human labeling, we provided an annotation tool with interpolation techniques that can faster the annotating process. The shape of the 2D skeletal data is (num_joints, 2), with dimension one being the (x, y) of a joint. A more detailed topology of the skeletal is shown in Figure 1. 

* For 3D skeletal data, we use a 3D lifting tool to lift the 2D joints to 3D, which is implemented based on the open-source EvoSkeleton[2]. The shape of the 3D skeletal data is (num_joints, 3), with dimension one being the (x, y, z) of a joint.

<p align="center">
  <img width="400"  src="https://user-images.githubusercontent.com/32810188/122911842-4d413a00-d38a-11eb-8af6-b167504927a1.png" />
</p>
 <p align="center"> Figure 1. HAA 3D+T Skeleton Topology</p>    
 
## Get Started
1. run get_HAA500.py to get raw images from the video
```
python get_HAA500.py -p action_name
```

2. To view the skeleton example, run demo.py
```
python demo.py
```
## Annotation Tool

### Labelling UI
See the documentation [here](annotation_tool/labelling_ui/README.md).


## References
[1] Fang HS, Xie S, Tai YW, Lu C. Rmpe: Regional multi-person pose estimation. In Proceedings of the IEEE International Conference on Computer Vision, 2017 (pp. 2334-2343).

[2] Shichao Li, Lei Ke, Kevin Pratama, Yu-Wing Tai, Chi-KeungTang, and Kwang-Ting Cheng. Cascaded deep monocular 3dhuman pose estimation with evolutionary training data.

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
