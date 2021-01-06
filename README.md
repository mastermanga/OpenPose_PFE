# Final Project - AI Movement detection with Openpose

This project is an student project in collaboration with the french sport instiue **INSEP**. The project is an algorithm that simulates a training environment for cross hockey goalkeeper (and maybe used for other disciplines later on). The algorithm are based on Open Source technologies such as Open Pose and OpenCV libraries.

More info on their repos :

- Open Pose : https://github.com/ildoonet/tf-pose-estimation 
- OpenCV : https://github.com/opencv/opencv 

## Installation

### Dependencies 



asdf

### Openpose setup

Clone the repository and install the libraries :

```bash
$ git clone https://github.com/mastermanga/OpenPose_PFE.git
$ cd OpenPose_PFE`
$ pip install -r requirements.txt
```

Build the C++ library for post processing :

```bash
$ cd tf_pose/pafprocess
$ swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace
```

Download the CMU model :
```bash
$ cd models/graph/cmu
$ bash download.sh
```




## Recording

asdf

## Analytics

You can run a full analysis on a specific image or run each part of the analysis indivdually

Full analysis : asdf

### Openpose analysis

Run :

```bash
$ python analyse.py
```

### Cross tracking


### Grid positionnin draw

The *grid.py* script simply open the image in a web interface to draw a 5x5 grid around the top left corner to the bottom right

#### How to run
Launch:

`python grid.py <path-to-image><path-to-output>`

Specified paths can be absolute or relative

###### Example

`python grid.py img/goalkeeper.png output/fig1.png`
