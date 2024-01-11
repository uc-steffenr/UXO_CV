"""Split up images using impy. impy is unsupported and requires different Python version."""
from impy.ObjectDetectionDataset import ObjectDetectionDataset
import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--offset', '-o', nargs=2, type=int,
                        help='List of int that contains amount of pixels per image')
    parser.add_argument('--dbName', '-db', type=str,
                        help='Name of database')
    parser.add_argument('--img_input_path', '-ii', type=str,
                        help='str that contains path to dir with current images')
    parser.add_argument('--ann_input_path', '-ai', type=str,
                        help='str that contains path to dir with current annotations')
    parser.add_argument('--img_output_path', '-io', type=str,
                        help='str that contains path to dir where images will be stored')
    parser.add_argument('--ann_output_path', '-ao', type=str,
                        help='str that contains path to dir where annotations will be stored')

    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parse()

    offset = args.offset
    dbName = args.dbName
    img_input_path = args.img_input_path
    ann_input_path = args.ann_input_path
    img_output_path = args.img_output_path
    ann_output_path = args.ann_output_path

    obda = ObjectDetectionDataset(imagesDirectory=img_input_path,
                                  annotationsDirectory=ann_input_path,
                                  databaseName=dbName)
    obda.reduceDatasetByRois(offset=offset,
                             outputImageDirectory=img_output_path,
                             outputAnnotationDirectory=ann_output_path)
