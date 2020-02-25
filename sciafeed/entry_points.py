"""
This modules provides the functions of the SCIA FEED package's entry points
"""
from os import listdir, mkdir
from os.path import exists, isfile, join
import sys

import click

from sciafeed import formats


@click.command()
@click.argument('in_filepath', type=click.Path(exists=True, dir_okay=False))
@click.option('--out_filepath', '-o', type=click.Path(exists=False, dir_okay=False),
              help="file path of the output report. If not provided, prints on screen")
@click.option('--outdata_filepath', '-d', type=click.Path(exists=False, dir_okay=False),
              help="file path of the output data file")
@click.option('--parameters_filepath', '-p', type=click.Path(exists=True, dir_okay=False),
              help="customized file path containing information about parameters")
def make_report(**kwargs):
    """
    Parse a file containing data located at `in_filepath` and generate a report.
    Optionally, it can also export parsed data.
    """
    msgs, _ = formats.make_report(**kwargs)
    if not kwargs['out_filepath']:
        for msg in msgs:
            print(msg)
    if kwargs['outdata_filepath']:
        print('data saved on %s' % kwargs['outdata_filepath'])


@click.command()
@click.argument('in_folder', type=click.Path(exists=True, dir_okay=True))
@click.option('--out_filepath', '-o', type=click.Path(exists=False, dir_okay=False),
              help="file path of the output report. If not provided, prints on screen")
@click.option('--outdata_folder', '-d', type=click.Path(exists=False, dir_okay=True),
              help="folder path where to put the output data files")
def make_reports(**kwargs):
    """
    Parse a folder containing data located at `in_folder` and generate a report.
    Optionally, it can also export parsed data.
    """
    in_folder = kwargs['in_folder']
    outdata_folder = kwargs['outdata_folder']
    if kwargs['out_filepath'] and exists(kwargs['out_filepath']):
        print('wrong "out_filepath": the report must not exist or will be overwritten')
        sys.exit(2)
        # return
    if outdata_folder and not exists(outdata_folder):
        mkdir(outdata_folder)
    children = sorted(listdir(in_folder))
    for child in children:
        in_filepath = join(in_folder, child)
        if not isfile(in_filepath):
            continue
        print('processing file %r' % child)
        if outdata_folder:
            outdata_filepath = join(outdata_folder, child + '.csv')
        else:
            outdata_filepath = None
        current_msgs, _ = formats.make_report(
            in_filepath,
            outdata_filepath=outdata_filepath,
            out_filepath=kwargs['out_filepath']
        )
        if not kwargs['out_filepath']:
            for msg in current_msgs:
                print(msg)
