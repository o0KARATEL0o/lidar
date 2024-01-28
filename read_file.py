import asyncio
import os
from datetime import datetime
from pathlib import Path
import re
import sys
from project_log import project_logger
from protocols import protocols
import pandas as pd
import tqdm.asyncio
from tqdm import tqdm


def read_header(lidar_file):
    """ Read the header of the lidar file """
    datetime_str = lidar_file.readline().decode().strip()
    hist_datetime = datetime.strptime(
        datetime_str, 'Datetime %Y-%m-%d %H:%M:%S')
    project_logger.info(f'Histogram datetime: {hist_datetime}')
    project_logger.debug(
        f'Histogram datetime: {hist_datetime} from {datetime_str}')

    lidar_name_str = lidar_file.readline().decode().strip()
    lidar_name = re.findall(r'(?<=LiDAR ).*', lidar_name_str)[0]
    project_logger.info(f'Lidar name: {lidar_name}')
    project_logger.debug(f'Lidar name: {lidar_name} from {lidar_name_str}')

    pulses_str = lidar_file.readline().decode().strip()
    project_logger.debug(f'Pulses str: {pulses_str}')
    pulses = re.findall(r'(?<=Pulses )\d+', pulses_str)[0]
    pulses = int(pulses)
    project_logger.info(f'Pulses: {pulses}')

    return hist_datetime, lidar_name, pulses


def signals(
        result_file,
        channel1: pd.Series,
        channel2: pd.Series,
        hist_datetime: datetime
):
    aerosol_bounds = [70, 179]
    target_bounds = [180, 290]
    df_signals = pd.DataFrame(
        {
            0: hist_datetime,
            1: channel1.loc[aerosol_bounds[0]:aerosol_bounds[1]].sum(),
            2: channel1.loc[target_bounds[0]:target_bounds[1]].sum(),
            3: channel2.loc[aerosol_bounds[0]:aerosol_bounds[1]].sum(),
            4: channel2.loc[target_bounds[0]:target_bounds[1]].sum()
        },
        index=[0]
    )
    df_signals.to_csv(
        result_file,
        header=False,
        index=False,
        mode='a',
        sep=';',
        date_format='%Y-%m-%d %H:%M:%S'
    )


async def read_file(
    result_file,
    file_dir,
    file_name
):
    project_logger.info(f'Reading file {file_name}')
    file = open(os.path.join(file_dir, file_name), 'rb')
    histogram_datetime, lidar_name, pulses = read_header(file)
    lidar_device = protocols[lidar_name]
    data = lidar_device.read_data_from_file(file)
    file.close()
    signals(
        result_file,
        pd.Series(data['channel1'].get('delays')
                  ).value_counts().sort_index(),
        pd.Series(data['channel2'].get('delays')
                  ).value_counts().sort_index(),
        histogram_datetime
    )


async def signals_from_dir(
    result_file,
        dir_f
):
    files = os.listdir(dir_f)
    for f in tqdm(files):
        await read_file(result_file, dir_f, f)
    return

if __name__ == "__main__":
    project_logger.configure(handlers=[{"sink": sys.stderr, "level": "ERROR"},
                                       {"sink": 'logs/file{time}.log', "level": "INFO"}
                                       ])
    dir = Path('C:/Users/KARATEL/Desktop/lidar/100k_1h/')
    asyncio.run(signals_from_dir('result.csv', dir))
