# EFREI M2 Final Project - AI Movement detection with Openpose - Unemployed Frogs

This project is an EFREI student project in collaboration with the french sport instiue **INSEP**. The project is an algorithm that simulates a training environment for cross hockey goalkeeper (eventually used by other disciplines later on). The algorithms are based on Open Source technologies such as Open Pose and OpenCV libraries.

More info on their repos :

- Open Pose : https://github.com/ildoonet/tf-pose-estimation 
- OpenCV : https://github.com/opencv/opencv 

## Installation

### Dependencies 

You need dependencies below.

- python3
- tensorflow 1.4.1+ BUT NOT 2.0+
- opencv3, protobuf, python3-tk

### Openpose setup

Clone the repository and install the libraries :

```bash
$ git clone https://github.com/mastermanga/OpenPose_PFE.git
$ cd OpenPose_PFE
$ pip install -r requirements.txt
```

Build the C++ library for post processing :

```bash
$ cd OpenPose/tf_pose/pafprocess
$ swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
```

Download the CMU model :
```bash
$ cd models/graph/cmu
$ bash download.sh
```

## Recording

### Data storing

Before performing records, fill the `record/attack_seq` directory with attack sequences. 

It is highly recommended to annotate each video with an identifier, for instance : 

`record/attack_seq/attack1.mp4`


### Start recording

To perform a series of recordings :

```bash
$ cd record
$ python record.py --runs <number-of-runs>
```
Each sequence will be displayed alongside the record.

All records are stored under the `goal` directory with a corresponding datetime folder


## Analytics

You can run a full analysis on a specific image or run each part of the analysis individually.

*Analysis on entire set of images in a directory is in WIP*

To perform full analysis on a single image :

```bash
$ cd analysis
$ ./full_analysis.sh
```

Then input the image and output directory paths

### Openpose analysis

For an analysis performed on a single image, run :

```bash
$ cd analysis
$ python analyse_image.py --image <path-to-image> --output <output-directory>
```

### Cross tracking

asdf

### Grid positionnin draw

The *grid.py* script simply open the image in a web interface to draw a 5x5 grid around the top left corner to the bottom right

To run, launch:
```bash
$ python grid.py <path-to-image> <path-to-output>
```
Specified paths can be absolute or relative

