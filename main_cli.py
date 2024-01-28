
from com_port import LiDAR_Port
import schedule
from os import PathLike
from protocols import protocols
from measure import measure
from project_log import project_logger
import click


@click.command()
@click.option('--com_port', '-c', type=str, default='COM3', help='COM port')
@click.option('--baudrate', '-b', type=int, default=115200, help='Baudrate')
@click.option('--protocol', '-p', type=str, default='delft', help='Protocol')
@click.option('--folder', '-f', type=click.Path(exists=True, file_okay=False, dir_okay=True), default='.', help='Folder')
@click.option('--pulses', '-pulses', type=int, default=5000, help='Pulses int')
@click.option('--period', '-period', type=int, default=10, help='Period. Interval in minutes.')
def LiDAR_cli(
    com_port: str,
    baudrate: int,
    protocol: str,
    folder: PathLike,
    pulses: int = 50,
    period: int = 10
) -> None:
    project_logger.info(f'Input COM port {com_port}')
    project_logger.info(f'Input Baudrate {baudrate}')
    project_logger.info(f'Input protocol {protocol}')
    project_logger.info(f'Input Folder {folder}')
    project_logger.info(f'Input Pulses {pulses}')
    project_logger.info(f'Input Period {period}')
    lidar_protocol = protocols.get(protocol)
    project_logger.info(f'Protocol for LiDAR_Port {lidar_protocol}')
    lidar = LiDAR_Port(com_port, baudrate, lidar_protocol)
    list_of_times = [':'+str(minutes).zfill(2)
                     for minutes in range(0, 60, period)]
    for time in list_of_times:
        project_logger.info(f'Time {time}')
        schedule.every().hour.at(time).do(measure, lidar, folder, pulses)
    while True:
        try:
            schedule.run_pending()
        except Exception as error:
            project_logger.error(error)
            lidar.close()
            project_logger.debug('COM port is closed')
            break


if __name__ == "__main__":
    LiDAR_cli()
