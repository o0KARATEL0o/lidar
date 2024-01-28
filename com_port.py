import serial
import serial.tools.list_ports
from project_log import project_logger
from protocols import Protocol


class LiDAR_Port(object):
    """Class for LiDAR_Port."""

    def __init__(self, com_port: str, baudrate: int, protocol: Protocol):
        try:
            self.port = serial.Serial(com_port, baudrate, timeout=1.6)
            self.protocol = protocol
            project_logger.debug(f'COM port {com_port} is connected')
        except Exception:
            raise

    def close(self):
        self.port.close()
        project_logger.debug('COM port is closed')
        return

    def read_bytes(self, num_of_bytes: int = 1) -> bytes:
        input_bytes = self.port.read(num_of_bytes)
        project_logger.debug(f'Read {num_of_bytes} bytes')
        return input_bytes

    def set_pulses(
        self,
        pulses: int,
    ) -> bool:
        """Set pulses."""
        project_logger.debug(f'Set pulses {pulses}')
        command = self.protocol.get_pulses_command(pulses)
        project_logger.debug(f'Command for set pulses is {command.hex()}')
        self.port.write(command)
        read_answer = self.port.read(2)
        project_logger.debug(f'Answer is {read_answer.hex()}')
        if command.find(read_answer) != -1 and read_answer != b'':
            project_logger.info(
                f'Pulses are set.\n Find answer in command with index {command.find(read_answer)}')
            return True
        else:
            project_logger.error(f'Invalid answer {read_answer.hex()}')
            return False

    def read_lidar_data(
            self,

            file,
    ):
        self.port.write(self.protocol.start)
        project_logger.info(
            f'Start measure with command {self.protocol.start.hex()}')
        stop = bytes(0)
        lidar_bytes = bytes(1)
        stop_index = -1
        buffer = 64
        while not (stop == self.protocol.stop or lidar_bytes == b''):
            lidar_bytes = self.read_bytes(buffer)
            project_logger.debug(f'Read bytes {lidar_bytes.hex()}')
            file.write(lidar_bytes)
            stop_index = lidar_bytes.find(self.protocol.stop)
            project_logger.debug(f'Stop index is {stop_index}')
            if stop_index != -1:
                stop = self.protocol.stop
        if stop_index != -1:
            last_buffer = 12 - buffer + stop_index + 2
            project_logger.debug(f'Number of last bytes {last_buffer}')
            if last_buffer > 0:
                lidar_bytes = self.read_bytes(last_buffer)
                project_logger.debug(f'Last bytes are {lidar_bytes.hex()}')
                file.write(lidar_bytes)

    def read_parameters(self, file):
        project_logger.info(f'Read parameters')
        for key in self.protocol.parameters.keys():
            self.port.write(self.protocol.parameters[key].get('command'))
            project_logger.debug(
                f'Get {key}. Send command {self.protocol.parameters[key].get("command").hex()}'
            )
            answer = self.port.read(
                self.protocol.parameters[key].get('answer_bytes'))
            project_logger.debug(
                f'Read answer {answer.hex()}'
            )
            file.write(key.encode() + b'\n' + answer + b'\n')


def available_com_ports() -> list:
    result = []
    ports = serial.tools.list_ports.comports()
    for port, _, _ in sorted(ports):
        result.append(port)
    return result
