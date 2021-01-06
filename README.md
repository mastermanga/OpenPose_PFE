# OpenPose_PFE

### Installation

How to make it work :

`git clone https://github.com/mastermanga/OpenPose_PFE.git`

`cd OpenPose_PFE/Src`

`pip install -r requirements.txt`

`cd tf_pose/pafprocess`

`swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace`

`cd models/graph/cmu`

`bash download.sh`

`cd Src`

`python analyse.py`

### Analytics

The *grid.py* script simply open the image in a web interface to draw a 5x5 grid around the top left corner to the bottom right

##### How to run
Launch
`python grid.py <path-to-image><path-to-output>`

Specified paths can be absolute or relative

###### Example

`python grid.py img/goalkeeper.png output/fig1.png`
