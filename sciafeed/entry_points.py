"""
This modules provides the functions of the SCIA FEED package's entry points
"""
from os import listdir, mkdir
from os.path import exists, isdir, isfile, join
import sys

import click

from sciafeed import hiscentral
from sciafeed import process


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
    msgs, _ = process.make_report(**kwargs)
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
    if not isdir(in_folder):
        print('wrong "in_folder": this must be a folder')
        sys.exit(2)
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
        current_msgs, _ = process.make_report(
            in_filepath,
            outdata_filepath=outdata_filepath,
            out_filepath=kwargs['out_filepath']
        )
        if not kwargs['out_filepath']:
            for msg in current_msgs:
                print(msg)


@click.command()
@click.option('--region_id', '-r', help="code of the region to download (for example '01')")
@click.option('--variables', '-v', multiple=True,
              help="list of the variables to download. Default is 'Precipitation', 'Tmax', 'Tmin'",
              default=['Precipitation', 'Tmax', 'Tmin'])
@click.option('--locations', '-l', multiple=True,
              help="list of the locations to download. Default is all the locations of the region")
@click.option('--out_csv_folder', '-o', type=click.Path(exists=False, dir_okay=True),
              help="folder path where to put the downloaded CSV data files")
def download_hiscentral(region_id, variables, locations, out_csv_folder):
    """
    Download CSV of the HISCENTRAL for region, locations and variables selected into an
    output folder.
    """
    if not region_id:
        print('region_id is required')
        return
    if region_id not in hiscentral.REGION_IDS_MAP:
        print("region_id %r is not recognized as a valid code" % region_id)
        return
    if not out_csv_folder:
        print("out_csv_folder is required")
        return
    if not locations:
        locations = None
    if not exists(out_csv_folder):
        mkdir(out_csv_folder)
    ret_value = hiscentral.download_hiscentral(region_id, out_csv_folder, variables, locations)
    print('done')
    return ret_value


@click.command()
@click.option('--data_folder', '-d', type=click.Path(exists=True, dir_okay=True),
              help="folder path where to get the data files")
@click.option('--indicators_folder', '-i', type=click.Path(exists=False, dir_okay=True),
              help="folder path of the output files")
@click.option('--report_path', '-r', type=click.Path(exists=False, dir_okay=False),
              help="file path of the output report. If not provided, prints on screen")
def compute_indicators(data_folder, indicators_folder, report_path):
    """
    Compute daily indicators from data files located at folder `data_folder`,
    and put results in the folder `indicators_folder`.
    """
    # print(data_folder, indicators_folder, report_path)
    if report_path and exists(report_path):
        print('wrong "report_path": the report must not exist or will be overwritten')
        sys.exit(2)
    if not data_folder:
        print('"data_folder" is required')
        sys.exit(2)
    if not isdir(data_folder):
        print('wrong "data_folder": this must be a folder')
        sys.exit(2)
    if indicators_folder:
        if exists(indicators_folder):
            if not isdir(indicators_folder):
                print('wrong "indicators_folder": this must be a folder')
                sys.exit(2)
        else:
            mkdir(indicators_folder)
    else:
        # this will be removed when we can insert in the database
        print('"indicators_folder" is required')
        sys.exit(2)
    msgs, _ = process.compute_indicators(data_folder, indicators_folder, report_path)
    if not report_path:
        for msg in msgs:
            print(msg)

