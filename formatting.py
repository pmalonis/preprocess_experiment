import sys
import argparse
import os
from glob import glob
import xml.etree.ElementTree as ET
import yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocesses and correctly formats raw data')
    parser.add_argument('-i', '--imaging', required=True,
                        help='Directory containing raw imaging data')
    parser.add_argument('-b', '--behavioral', required=True,
                        help='Directory containing raw behavioral movies')
    parser.add_argument('-o', '--output', default='.',
                        help='Output directory (defaults to current directory)')
    #args = parser.parse_args(['-i', 'image', '-b', 'behave'])
    args = parser.parse_args(['-i', '/home/pmalonis/data_analysis/data/e1m1d1s2', '-b', 'asdf'])

    output_imaging = args.output + 'raw_imaging'
    output_behavior = args.output + 'raw_behavior'
    os.system('mkdir ' + output_imaging)
    os.system('mkdir ' + output_behavior)

    # reading imaging metadata
    inscopix_meta = glob(args.imaging + '/*.xml')
    try:
        assert(len(inscopix_meta) == 1)
    except AssertionError as e:
        if len(inscopix_meta) == 0:
            print('Error: xml file not found in the imaging directory.')
        else:
            print('Error: There are multiple xml files in the imaging directory.')
        raise e

    metadata_dict = dict()
    parsed = ET.parse(inscopix_meta[0])
    for child in parsed.getroot():
        if child.tag == 'attrs':
            # copies recording attributes
            for attr in child:
                try:
                    metadata_dict[attr.attrib['name']] = int(attr.text)
                except ValueError:
                    try:
                        metadata_dict[attr.attrib['name']] = float(attr.text)
                    except ValueError:
                        metadata_dict[attr.attrib['name']] = attr.text

        elif child.tag == 'decompressed':
            # gets number of total frames in decompressed file
            frames = 0
            for file in child:
                frames += int(file.attrib['frames'])
            metadata_dict['frames'] = frames

    with open(output_imaging + '/attributes.yaml', 'w') as attribute_file:
        yaml.dump(metadata_dict, attribute_file, default_flow_style=False)
