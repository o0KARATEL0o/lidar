from datetime import datetime
import com_port as com_port
import os
import pathlib
from project_log import project_logger
from threading import BoundedSemaphore

connections = BoundedSemaphore()


def measure(
        port: com_port.LiDAR_Port,
        folder: os.PathLike,
        pulses: int = 50
) -> None:
    """Measure."""
    connections.acquire()
    project_logger.info(f'Start measurement')
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.bin'
    path = pathlib.Path(folder, filename)
    project_logger.info(f'File in {path}')
    try:
        file = open(path, 'wb')
        project_logger.info(f'File {path} is opened')
        file.write(
            b'Datetime ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode() + b'\n')
        file.write(b'LiDAR ' + port.protocol.name.encode() + b'\n')
        file.write(b'Pulses ' + str(pulses).encode() + b'\n')
        file.write(b'Data\n')
    except Exception as error:
        project_logger.error(error)
        raise
    if port.set_pulses(pulses):
        port.read_lidar_data(file)
        file.write(b'\nEnd of data;\n')
        file.write(b'Parameters\n')
        project_logger.info(f'Data collected')
        port.read_parameters(file)
        file.write(b'\nEnd of parameters;')
        project_logger.info(f'Parameters collected')
        project_logger.info(f'Measure is done')
        file.close()
        project_logger.info(f'File {path} is closed')
    else:
        project_logger.error(f'Measure can\'t set pulses. Abort.')
        file.close()
        project_logger.info(f'File {path} is closed')
    connections.release()
    return
