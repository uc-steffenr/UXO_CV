"""Put desired train/test/val data in the right dir, and make appropriate yaml file."""
import numpy as np
from numpy.random import default_rng

import os, shutil
import yaml
import argparse


classes = {'PFM-1' : 1, 'KSF Casing' : 0}


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', metavar='-ds', type=str, required=True)
    parser.add_argument('--percent_train', type=float, default=0.8)
    parser.add_argument('--percent_val', type=float, default=0.1)
    parser.add_argument('--roboflow_name', type=list, default=[i for i in 'original'], nargs='*')
    parser.add_argument('--seed', type=int, default=12345)

    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parse()

    # get vals from args
    seed = args.seed
    percent_train = args.percent_train
    percent_val = args.percent_val
    percent_test = 1. - percent_train - percent_val
    dataset_name = args.dataset_name
    roboflow_name = args.roboflow_name

    # set up directories based on args
    cwd = os.getcwd()

    data_dir = os.path.join(cwd, 'raw_data', 'roboflow')

    datasets_dir = os.path.join(cwd, 'datasets')
    dataset_dir = os.path.join(datasets_dir, dataset_name)
    
    all_img_dir = os.path.join(dataset_dir, 'all_images')
    all_ann_dir = os.path.join(dataset_dir, 'all_annotations')

    train_dir = os.path.join(dataset_dir, 'train')
    test_dir = os.path.join(dataset_dir, 'test')
    val_dir = os.path.join(dataset_dir, 'val')

    print('Setting dataset directory')
    if os.path.isdir(dataset_dir):
        shutil.rmtree(dataset_dir)

    os.mkdir(dataset_dir)

    os.mkdir(all_img_dir)
    os.mkdir(all_ann_dir)
    
    for dir in [''.join(i) for i in roboflow_name]:
        curr_dir = os.path.join(data_dir, dir, 'train')
        img_dir = os.path.join(curr_dir, 'images')
        ann_dir = os.path.join(curr_dir, 'labels')
        
        img_files = os.listdir(img_dir)
        ann_files = os.listdir(ann_dir)
        
        for img, ann in zip(img_files, ann_files):
            shutil.copy(os.path.join(img_dir, img), all_img_dir)
            shutil.copy(os.path.join(ann_dir, ann), all_ann_dir)
    
    os.mkdir(train_dir)
    os.mkdir(os.path.join(train_dir, 'labels'))
    os.mkdir(os.path.join(train_dir, 'images'))

    os.mkdir(test_dir)
    os.mkdir(os.path.join(test_dir, 'labels'))
    os.mkdir(os.path.join(test_dir, 'images'))

    os.mkdir(val_dir)
    os.mkdir(os.path.join(val_dir, 'labels'))
    os.mkdir(os.path.join(val_dir, 'images'))

    print('Shuffling train, test, and val data')
    rng = default_rng(seed)

    num_data = len(os.listdir(all_img_dir))

    train_size = int(percent_train*num_data)
    val_size = int(percent_val*num_data)

    train_indices = rng.choice(num_data, size=(train_size,), replace=False)
    val_indices = []

    i = 0
    while i < val_size:
        tmp = rng.choice(num_data, replace=False)
        if tmp in val_indices or tmp in val_indices:
            continue
        val_indices.append(tmp)
        i += 1

    val_indices = np.array([val_indices])
    test_indices = np.array([ind for ind in range(num_data) if ind not in train_indices and ind not in val_indices])

    images = os.listdir(all_img_dir)

    for i, img in enumerate(images):
        txt = img[:-4]+'.txt'

        if i in train_indices:
            cp_dir = train_dir
        elif i in test_indices:
            cp_dir = test_dir
        elif i in val_indices:
            cp_dir = val_dir

        shutil.copy(os.path.join(all_img_dir, img), os.path.join(cp_dir, 'images'))
        shutil.copy(os.path.join(all_ann_dir, txt), os.path.join(cp_dir, 'labels'))

    shutil.rmtree(all_img_dir)
    shutil.rmtree(all_ann_dir)

    data_yaml = dict(train=train_dir,
                     test=test_dir,
                     val=val_dir,
                     nc=2,
                     names=['KSF Casing', 'PFM-1'],
                     shuffle_seed=seed)

    f = open(os.path.join(dataset_dir, 'data.yaml'), 'w')
    yaml.dump(data_yaml, f, default_flow_style=False)
    f.close()

    print('All done!')
