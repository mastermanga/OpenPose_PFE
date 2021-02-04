import argparse
import logging
import sys
import time

import sys
sys.path.insert(0, "../OpenPose") 

from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimatorRun')
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--image', type=str, default='./img/goalkeeper.png')
    parser.add_argument('--image_last', type=str, default='./img/goalkeeper.png')
    parser.add_argument('--image_white', type=str, default='./img/goalkeeper.png')
    parser.add_argument('--output', type=str, default='.')
    parser.add_argument('--model', type=str, default='mobilenet_thin',
                        help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--resize', type=str, default='432x368',
                        help='if provided, resize images before they are processed. '
                             'default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    args = parser.parse_args()

    w, h = model_wh(args.resize)
    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))


    # estimate human poses from a single image !
    # pic = "video/track/bleu1video.png"
    
    #first frame args:image
    pic = args.image

    pic_name = pic.split('/')[-1].split('.',1)[0]

    image = common.read_imgfile(pic, None, None)
    if image is None:
        logger.error('Image can not be read, path=%s' % args.image)
        sys.exit(-1)

    t = time.time()
    humans_first = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
    elapsed = time.time() - t

    logger.info('inference image: %s in %.4f seconds.' % (args.image, elapsed))

    # loading the white image and draw the skeleton of the first frame
    white_image = common.read_imgfile(args.image_white, None, None)
    
    pos, skeleton_first = TfPoseEstimator.draw_humans(white_image, humans_first, imgcopy=False)
    
    print('human_first_pos')
    print(pos)

    # last frame extracting skeleton 
    last_image = common.read_imgfile(args.image_last, None, None)
    
    if last_image is None:
        logger.error('Image can not be read, path=%s' % args.image_last)
        sys.exit(-1)

    t = time.time()
    humans_last = e.inference(last_image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
    elapsed = time.time() - t

    logger.info('inference image: %s in %.4f seconds.' % (args.image_last, elapsed))

    grey_skeleton = cv2.cvtColor(skeleton_first, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(args.output + '/' + pic_name.replace('_first','') + '_opp.png',grey_skeleton)
    
    grey_white = cv2.imread(args.output + '/' + pic_name.replace('_first','') + '_opp.png')
    pos_, skeleton = TfPoseEstimator.draw_humans(grey_white, humans_last, imgcopy=False)

    cv2.imwrite(args.output + '/' + pic_name.replace('_first','') + '_opp_white.png', skeleton)

    #print('posi_last')
    #print(pos_)

    grey = cv2.imread(args.output + '/' + pic_name.replace('_first','') + '_opp.png')
    a = cv2.line(grey, pos, pos_, (34,0,255),4)
    cv2.imwrite(args.output + '/' + pic_name.replace('_first','') + '___opp_white.png', a)
    
    
    ##### 
    #changing image to imag
    posi, imag_first = TfPoseEstimator.draw_humans(image, humans_first, imgcopy=False)
    poos, imag_last = TfPoseEstimator.draw_humans(last_image, humans_last, imgcopy=False)

    try:
        import matplotlib.pyplot as plt

        ## First image

        fig = plt.figure()
        #a = fig.add_subplot(2, 2, 1)
        #a.set_title('Result')
        pic_color = cv2.cvtColor(imag_first, cv2.COLOR_BGR2RGB)
        #plt.imshow(pic_color)
        cv2.imwrite(args.output + '/' + pic_name + '_opp.png', pic_color)
        #bgimg = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2RGB)
        #bgimg = cv2.resize(bgimg, (e.heatMat.shape[1], e.heatMat.shape[0]), interpolation=cv2.INTER_AREA)

        # show network output
        #a = fig.add_subplot(2, 2, 2)
        #plt.imshow(bgimg, alpha=0.5)
        #tmp = np.amax(e.heatMat[:, :, :-1], axis=2)
        #plt.imshow(tmp, cmap=plt.cm.gray, alpha=0.5)
        #plt.colorbar()

        tmp2 = e.pafMat.transpose((2, 0, 1))
        tmp2_odd = np.amax(np.absolute(tmp2[::2, :, :]), axis=0)
        tmp2_even = np.amax(np.absolute(tmp2[1::2, :, :]), axis=0)
        #a = fig.add_subplot(2, 2, 3)
        #a.set_title('Vectormap-x')
        # plt.imshow(CocoPose.get_bgimg(inp, target_size=(vectmap.shape[1], vectmap.shape[0])), alpha=0.5)
        #plt.imshow(tmp2_odd, cmap=plt.cm.gray, alpha=0.5)
        #plt.colorbar()

        #a = fig.add_subplot()
        #a.set_title('Vectormap-y')
        # plt.imshow(CocoPose.get_bgimg(inp, target_size=(vectmap.shape[1], vectmap.shape[0])), alpha=0.5)
        
        plt.imshow(tmp2_even, cmap=plt.cm.Greys)
        figure = plt.gcf()
        figure.set_size_inches(8, 6)
        plt.savefig(args.output + '/' + pic_name + '_opp_grey.png', dpi=100)
        #plt.colorbar()
        #plt.show()

        # Last image         
        imag_last_color = cv2.cvtColor(imag_last, cv2.COLOR_BGR2RGB)
        pic_last_name = args.image_last.split('/')[-1].split('.',1)[0]
        cv2.imwrite(args.output + '/' + pic_last_name + '_opp.png', imag_last_color)



    except Exception as e:
        logger.warning('matplitlib error, %s' % e)
        cv2.imshow('result', image)
        cv2.waitKey()
