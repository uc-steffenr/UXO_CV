"""Put desired train/test/val data in the right dir, and make appropriate yaml file."""
import numpy as np
from numpy.random import default_rng
import cv2 as cv

import os, shutil, subprocess
from xml.dom import minidom
import yaml
import argparse


classes = {'PFM-1' : 0, 'KSF Casing' : 1}

def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def xml2yolo(fname, target_dir):
    xmldoc = minidom.parse(fname)
    fname_out = os.path.join(target_dir, fname.split('/')[-1][:-4]+'.txt')

    with open(fname_out, 'w') as f:
        itemlist = xmldoc.getElementsByTagName('object')
        size = xmldoc.getElementsByTagName('size')[0]
        width = int((size.getElementsByTagName('width')[0]).firstChild.data)
        height = int((size.getElementsByTagName('height')[0]).firstChild.data)

        for item in itemlist:
            classid = (item.getElementsByTagName('name')[0]).firstChild.data
            xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
            ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
            xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
            ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert_coordinates((width, height), b)

            f.write(str(classes[classid]) + ' ' + ' '.join([f'{a:.6f}' for a in bb]) + '\n')

def cmd(msg):
    subprocess.run(msg, shell=True, executable='/bin/bash')

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=12345)
    parser.add_argument('--percent_train', type=float, default=0.8)
    parser.add_argument('--percent_val', type=float, default=0.1)
    parser.add_argument('--orthoimage_dir', type=list, default=None, nargs='*')
    parser.add_argument('--split_image_dir', type=list, default=None, nargs='*')
    parser.add_argument('--database_name', metavar='-db', type=str, required=True)
    parser.add_argument('--dataset_name', metavar='-ds', type=str, required=True)
    parser.add_argument('--offset', type=int, nargs=2, default=[1032, 1032])
    parser.add_argument('--shuffle_only', action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parse()

    # get vals from args
    seed = args.seed
    percent_train = args.percent_train
    percent_val = args.percent_val
    percent_test = 1. - percent_train - percent_val

    orthoimage_dirs = args.orthoimage_dir
    split_image_dirs = args.split_image_dir

    database_name = args.database_name
    offset = args.offset
    dataset_name = args.dataset_name

    # set up directories based on args
    cwd = os.getcwd()

    data_dir = os.path.join(cwd, 'raw_data', 'roboflow')
    ortho_dir = os.path.join(data_dir, 'orthoimages')
    split_dir = os.path.join(data_dir, 'split_images')    

    database_img_dir = 'databases/'+database_name+'/images'
    database_xml_dir = 'databases/'+database_name+'/xml'

    database_orthoimg_dir = 'databases/'+database_name+'/orthoimgs'
    database_orthoann_dir = 'databases/'+database_name+'/orthoanns'

    databases_dir = os.path.join(cwd, 'databases')
    database_dir = os.path.join(databases_dir, database_name)
    database_ann_dir = os.path.join(database_dir, 'labels')

    if not args.shuffle_only:
        print('Setting up database')
        os.mkdir(database_dir)
        os.mkdir(database_img_dir)
        os.mkdir(database_ann_dir)
        os.mkdir(database_xml_dir)

        os.mkdir(database_orthoimg_dir)
        os.mkdir(database_orthoann_dir)

        # if there's just one dir, it should just loop over that list still
        for dir in [''.join(i) for i in orthoimage_dirs]:
            curr_dir = os.path.join(ortho_dir, dir, 'train')
            img_files = [img for img in os.listdir(curr_dir) if '.jpg' in img or '.png' in img]
            ann_files = [ann for ann in os.listdir(curr_dir) if '.xml' in ann]

            for img_file in img_files:
                shutil.copy(os.path.join(curr_dir, img_file), database_orthoimg_dir)
            for ann_file in ann_files:
                shutil.copy(os.path.join(curr_dir, ann_file), database_orthoann_dir)

        for dir in [''.join(i) for i in split_image_dirs]:
            curr_dir = os.path.join(split_dir, dir, 'train')

            img_files = [img for img in os.listdir(curr_dir) if '.jpg' in img or '.png' in img]
            ann_files = [ann for ann in os.listdir(curr_dir) if '.xml' in ann]

            for img_file in img_files:
                shutil.copy(os.path.join(curr_dir, img_file), database_img_dir)
            for ann_file in ann_files:
                shutil.copy(os.path.join(curr_dir, ann_file), database_xml_dir)

        print('Splitting orthoimages')
        cmd(f'conda run -n impy python split_images.py --offset {offset[0]} {offset[1]} --dbName {database_name} ' + \
            f'--img_input_path {database_orthoimg_dir} --ann_input_path {database_orthoann_dir} --img_output_path {database_img_dir} ' + \
            f'--ann_output_path {database_xml_dir}')

        print('Converting xml files to yolo format')
        for xml in os.listdir(database_xml_dir):
            xml2yolo(os.path.join(database_xml_dir, xml), database_ann_dir)

        shutil.rmtree(database_orthoimg_dir)
        shutil.rmtree(database_orthoann_dir)
        shutil.rmtree(database_xml_dir)

    datasets_dir = os.path.join(cwd, 'datasets')
    dataset_dir = os.path.join(datasets_dir, dataset_name)

    train_dir = os.path.join(dataset_dir, 'train')
    test_dir = os.path.join(dataset_dir, 'test')
    val_dir = os.path.join(dataset_dir, 'val')

    print('Setting dataset directory')
    if os.path.isdir(dataset_dir):
        shutil.rmtree(dataset_dir)

    os.mkdir(dataset_dir)
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

    num_data = len(os.listdir(database_img_dir))

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

    database_images = os.listdir(database_img_dir)

    for i, img in enumerate(database_images):
        txt = img[:-4]+'.txt'

        if i in train_indices:
            cp_dir = train_dir
        elif i in test_indices:
            cp_dir = test_dir
        elif i in val_indices:
            cp_dir = val_dir

        shutil.copy(os.path.join(database_img_dir, img), os.path.join(cp_dir, 'images'))
        shutil.copy(os.path.join(database_ann_dir, txt), os.path.join(cp_dir, 'labels'))

    data_yaml = dict(train=train_dir,
                     test=test_dir,
                     val=val_dir,
                     nc=2,
                     names=['PFM-1', 'KSF Casing'],
                     shuffle_seed=seed)

    f = open(os.path.join(dataset_dir, 'data.yaml'), 'w')
    yaml.dump(data_yaml, f, default_flow_style=False)
    f.close()

    print('All done!')
