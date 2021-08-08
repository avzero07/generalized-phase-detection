import os
import sys
import subprocess as sp
import argparse as ap
from tqdm import tqdm

if __name__ == "__main__":
    parser = ap.ArgumentParser(
        prog='gpd_predict_batch.py',
        description='Batch Execute Generalized Phase'
                    'Detection')
    parser.add_argument(
        '-C',
        default=False,
        action='store_true',
        help='Clean Output')
    parser.add_argument(
        '-M',
        type=str,
        default=None,
        help='Custom Suffix to Output Folder')
    parser.add_argument(
        '-I',
        type=str,
        default=None,
        help='Input Directory')
    args = parser.parse_args()
    
    # Specify Output Names
    if(args.M):
        op_dir = os.path.join('output-{}'.format(args.M))
    else:
        op_dir = os.path.join('output')
    op_img_dir = os.path.join(op_dir,'images')
    if(not os.path.isdir(op_dir)):
        os.mkdir(op_dir)
    if(not os.path.isdir(op_img_dir)):
        os.mkdir(op_img_dir) 

    if(args.C):
        clean = '-C'
    else:
        clean = ''

    # Input Directory
    ip_dir = os.path.join(args.I)
    if(not os.path.isdir(ip_dir)):
        sys.exit('Input Directory does not exist!')

    # Stations of Interest
    sta_list = {
    'BFSB','CBB','CLRS','HOLB','HOPB','LLLB','NLLB','NTKA',
    'PACB','PHC','PTRF','SNB','SYMB','VGZ','WOSB'
    }

    for station in sta_list:
        if(not os.path.exists(os.path.join(ip_dir,'{}.in'.format(
            station)))):
            # Skip if station data missing
            continue
        save_dir = os.path.join(op_img_dir,'{}.png'.format(station))
        input_dir = os.path.join(ip_dir,'{}.in'.format(station))
        output_dir = os.path.join(op_dir,'{}.out'.format(station))

        # Construct Command
        gpd_command = 'python gpd_predict.py -V {} -S {} -I {} -O {}'.format(
                clean,save_dir,input_dir,output_dir)

        # Run Command
        op = sp.call(gpd_command.split())
