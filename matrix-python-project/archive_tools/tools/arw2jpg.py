import rawpy
import imageio
import argparse
import sys
import os
import multiprocessing

from PIL import Image
from os import listdir
from os.path import isfile, join
from joblib import Parallel, delayed
from tqdm import tqdm



def make_dir(dir_path):
    """
    Make a directory if it does not exists.
    :param dir_path: Directory path.
    :return: None.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def convert_raw(source, target, rawpy_params):
    """
    Converts a ARW file to a JPG file.
    :param source: ARW file path.
    :param target: JPG file path.
    :return: 1 if successful, else 0.
    """
    result = 0
    try:
        with rawpy.imread(source) as raw:
            rgb = raw.postprocess(**rawpy_params)
            Image.fromarray(rgb).save(target, quality=100, optimize=True)
            result = 1	
    except:
        result = 0
    return result


def parse_args(args):
    """
    :param args: Arguments passed to program.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Convert ARW to JPG')
    parser.add_argument('-s', '--source', 
        help='source directory', 
        required=True)
    parser.add_argument('-t', '--target', 
        help='target directory', 
        required=True)
    parser.add_argument('-v', '--verbosity', 
        help='verbosity', 
        required=False, 
        type=int, 
        default=0)
    parser.add_argument('-e', '--extension',
        help='output extension; JPG or TIFF',
        required=False,
        default='JPG')
    parser.add_argument('--use_camera_wb', 
        help='whether to use the as-shot white balance values', 
        required=False, 
        type=bool, 
        default=False)
    parser.add_argument('--use_auto_wb', 
        help='whether to try automatically calculating the white balance', 
        required=False, 
        type=bool, 
        default=False)
    parser.add_argument('--bright', 
        help='brightness scaling', 
        required=False, 
        type=float, 
        default=1.0)
    parser.add_argument('--median_filter_passes', 
        help='number of median filter passes after demosaicing to reduce color artifacts', 
        required=False, 
        type=int, 
        default=0)
    parser.add_argument('--noise_thr', 
        help='threshold for wavelet denoising (default disabled)', 
        required=False, 
        type=float, 
        default=None)
    parser.add_argument('--dcb_enhance', 
        help='DCB interpolation with enhanced interpolated colors', 
        required=False, 
        type=bool, 
        default=False)
    parser.add_argument('--four_color_rgb', 
        help='whether to use separate interpolations for two green channels', 
        required=False, 
        type=bool, 
        default=False)
    parser.add_argument('--demosaic_algorithm', 
        help='default is AHD; AAHD, AFD, AHD, AMAZE, DCB, DHT, LINEAR, LMMSE, MODIFIED_AHD, PPG, VCD, VCD_MODIFIED_AHD, VNG', 
        required=False, 
        default='AHD')
    parser.add_argument('--fbdd_noise_reduction', 
        help='controls FBDD noise reduction before demosaicing; Full, Light, Off', 
        required=False, 
        default='Off')
    parser.add_argument('--output_color', 
        help='output color space; Adobe, ProPhoto, Wide, XYZ, raw, sRGB', 
        required=False, 
        default='sRGB')
    parser.add_argument('--output_bps', help='8 or 16', 
        required=False, 
        type=int, 
        default=8)
    return parser.parse_args(args)


def get_rawpy_params(args):
    """
    Gets rawpy parameters for postprocessing.
    :param args: Arguments.
    :return: Dictionary of parameters for rawpy.
    """
    def get_value(d, key, default_key):
        """
        Gets a value coresponding to the specified key from the dictionary.
        :param d: Dictionary.
        :param key: Key.
        :param default_key: Default key to use if the one specified is not found.
        :return: Value corresponding to key in the dictionary.
        """
        if key in d:
            return d[key]
        return d[default_key]

    demosaic_algorithms = {
        'AAHD': rawpy.DemosaicAlgorithm.AAHD,
        'AFD': rawpy.DemosaicAlgorithm.AFD,
        'AHD': rawpy.DemosaicAlgorithm.AHD,
        'AMAZE': rawpy.DemosaicAlgorithm.AMAZE,
        'DCB': rawpy.DemosaicAlgorithm.DCB,
        'DHT': rawpy.DemosaicAlgorithm.DHT,
        'LINEAR': rawpy.DemosaicAlgorithm.LINEAR,
        'LMMSE': rawpy.DemosaicAlgorithm.LMMSE,
        'MODIFIED_AHD': rawpy.DemosaicAlgorithm.MODIFIED_AHD,
        'PPG': rawpy.DemosaicAlgorithm.PPG,
        'VCD': rawpy.DemosaicAlgorithm.VCD,
        'VCD_MODIFIED_AHD': rawpy.DemosaicAlgorithm.VCD_MODIFIED_AHD,
        'VNG': rawpy.DemosaicAlgorithm.VNG
    }
    output_colors = {
        'Adobe': rawpy.ColorSpace.Adobe,
        'ProPhoto': rawpy.ColorSpace.ProPhoto,
        'Wide': rawpy.ColorSpace.Wide,
        'XYZ': rawpy.ColorSpace.XYZ,
        'raw': rawpy.ColorSpace.raw,
        'sRGB': rawpy.ColorSpace.sRGB
    }
    fbdd_noise_reductions = {
        'Full': rawpy.FBDDNoiseReductionMode.Full,
        'Light': rawpy.FBDDNoiseReductionMode.Light,
        'Off': rawpy.FBDDNoiseReductionMode.Off
    }

    demosaic_algorithm = get_value(demosaic_algorithms, args.demosaic_algorithm, 'AHD')
    output_color = get_value(output_colors, args.output_color, 'sRGB')
    fbdd_noise_reduction = get_value(fbdd_noise_reductions, args.fbdd_noise_reduction, 'Off')

    return {
        'use_camera_wb': args.use_camera_wb,
        'use_auto_wb': args.use_auto_wb,
        'bright': args.bright,
        'median_filter_passes': args.median_filter_passes,
        'noise_thr': args.noise_thr,
        'dcb_enhance': args.dcb_enhance,
        'four_color_rgb': args.four_color_rgb,
        'half_size': False,
        'demosaic_algorithm': demosaic_algorithm,
        'fbdd_noise_reduction': fbdd_noise_reduction,
        'output_color': output_color,
        'output_bps': args.output_bps if args.output_bps == 8 or args.output_bps == 16 else 8
    }

def get_arw_files(dir_path):
    """
    :param dir_path: Directory path where ARW files live.
    :return: A list of just the ARW file names.
    """
    arw_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return arw_files


def get_source_files(source_dir, files):
    """
    :param source_dir: ARW directory path.
    :param files: List of ARW files in the ARW directory.
    :return: List of ARW source files.
    """
    source_files = [join(source_dir, f) for f in files]
    source_files = [f.replace('\\', '/') for f in source_files]
    return source_files


def get_target_files(target_dir, files, ext='JPG'):
    """
    :param target_dir: JPG directory path.
    :param files: List of ARW files in the ARW directory.
    :return: List of JPG target files.
    """
    target_files = [join(target_dir, f).replace('ARW', ext).replace('arw', ext) for f in files]
    target_files = [f.replace('\\', '/') for f in target_files]
    return target_files


def get_source_target_files(source_dir, target_dir, ext='JPG'):
    """
    :param source_dir: ARW source directory path.
    :param target_dir: JPG target directory path.
    :return: List of tuples. Each tuple has a source ARW and target JPG file path.
    """
    arw_files = get_arw_files(source_dir)
    source_files = get_source_files(source_dir, arw_files)
    target_files = get_target_files(target_dir, arw_files, ext)
    tups = [(s, t) for s, t in zip(source_files, target_files)]
    return tups


if __name__ == "__main__":
    # python arw2jpg.py -s ./Your_ARW -t ./out_jpg
    args = parse_args(sys.argv[1:])
    print('{} to {}'.format(args.source, args.target))
    make_dir(args.target)

    rawpy_params = get_rawpy_params(args)

    ext = args.extension.upper() if args.extension.upper() == 'JPG' or args.extension.upper() == 'TIFF' else 'JPG'
    tups = get_source_target_files(args.source, args.target, ext)
    verbosity = args.verbosity
    n_jobs = multiprocessing.cpu_count()
    results = Parallel(n_jobs=n_jobs, verbose=verbosity)(delayed(convert_raw)(tup[0], tup[1], rawpy_params) for tup in tqdm(tups))
    n_successes = sum(results)
    n_conversions = len(tups)
    print('{} of {} successful'.format(n_successes, n_conversions))
    
