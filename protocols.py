from project_log import project_logger
import copy


class Protocol(object):
    def __init__(self, name: str):
        self.name = name
        self.pulses_commands = {}
        self.start = bytes()
        self.stop = bytes()
        self.SPAD_voltage = bytes()
        self.parameters = {}
        self.read_data_protocol = {}

    def get_pulses_command(self, pulses: int) -> bytes:
        if self.pulses_commands != {}:
            try:
                return self.pulses_commands.get(pulses)
            except Exception:
                raise
        else:
            raise NotImplemented

    def set_spad_voltage(self, voltage: int):
        if self.set_spad_voltage != bytes:
            try:
                return self.SPAD_voltage + bytes(voltage)
            except Exception:
                raise
        else:
            raise NotImplemented

    def read_parameters(self):
        if self.parameters != {}:
            try:
                return self.parameters
            except Exception:
                raise
        else:
            raise NotImplemented

    def read_data_from_file(self, lidar_file):
        result = copy.deepcopy(self.read_data_protocol)
        if lidar_file.readline() == b'Data\n':
            read_bytes = lidar_file.read(2)
            project_logger.debug(f'Read bytes: {read_bytes.hex()}')
            while read_bytes != bytes.fromhex('FFFF'):
                project_logger.debug(f'Read bytes: {read_bytes.hex()}')
                for key in result.keys():
                    project_logger.debug(f'Key: {key}')
                    if read_bytes == result[key].get('mask'):
                        read_bytes = lidar_file.read(
                            result[key].get('number_of_bytes'))
                        project_logger.debug(
                            f'Data bytes: {read_bytes.hex()}, {int.from_bytes(read_bytes, byteorder="big")}')
                        result[key].get('delays').append(
                            int.from_bytes(read_bytes, byteorder='big'))
                        break
                    elif result[key].get('mask') is None:
                        project_logger.debug(
                            f'Data bytes: {read_bytes.hex()}, {int.from_bytes(read_bytes, byteorder="big")}')
                        result[key].get('delays').append(
                            int.from_bytes(read_bytes, byteorder='big'))
                        break
                read_bytes = lidar_file.read(2)

        else:
            raise NotImplemented
        return result


hokkaido = Protocol("hokkaido")
hokkaido.pulses_commands = {
    50: bytes.fromhex('F5 F5 70'),
    100: bytes.fromhex('F5 F5 71'),
    200: bytes.fromhex('F5 F5 72'),
    500: bytes.fromhex('F5 F5 73'),
    1000: bytes.fromhex('F5 F5 74'),
    2000: bytes.fromhex('F5 F5 75'),
    5000: bytes.fromhex('F5 F5 76'),
    10000: bytes.fromhex('F5 F5 77'),
    20000: bytes.fromhex('F5 F5 78'),
    50000: bytes.fromhex('F5 F5 79'),
    65536: bytes.fromhex('F5 F5 7A'),
    100000: bytes.fromhex('F5 F5 7B'),
    200000: bytes.fromhex('F5 F5 7C'),
    500000: bytes.fromhex('F5 F5 7D'),
    1000000: bytes.fromhex('F5 F5 7E'),
    2000000: bytes.fromhex('F5 F5 7F')
}
hokkaido.start = bytes.fromhex('F5 F5 51')
hokkaido.stop = bytes.fromhex('FF FF')
hokkaido.parameters = {
    'number_of_stops': {'command': bytes.fromhex('F5 F5 52'), 'answer_bytes': 6}
}
hokkaido.SPAD_voltage = bytes.fromhex('FA FA')
hokkaido.read_data_protocol = {
    'channel1': {'mask': None, 'number_of_bytes': 2, 'delays': list()}
}

delft = Protocol("delft")
delft.pulses_commands = {
    50: bytes.fromhex('F5 F5 70'),
    100: bytes.fromhex('F5 F5 71'),
    200: bytes.fromhex('F5 F5 72'),
    500: bytes.fromhex('F5 F5 73'),
    1000: bytes.fromhex('F5 F5 74'),
    2000: bytes.fromhex('F5 F5 75'),
    5000: bytes.fromhex('F5 F5 76'),
    10000: bytes.fromhex('F5 F5 77'),
    20000: bytes.fromhex('F5 F5 78'),
    50000: bytes.fromhex('F5 F5 79'),
    64000: bytes.fromhex('F5 F5 7A'),
    100000: bytes.fromhex('F5 F5 7B'),
    200000: bytes.fromhex('F5 F5 7C'),
    500000: bytes.fromhex('F5 F5 7D'),
    1000000: bytes.fromhex('F5 F5 7E'),
    2000000: bytes.fromhex('F5 F5 7F')
}
delft.start = bytes.fromhex('F5 F5 51')
delft.stop = bytes.fromhex('FF FF')
delft.parameters = {
    'energy': {'command': bytes.fromhex('F5 F5 54'), 'answer_bytes': 5},
    'temperature': {'command': bytes.fromhex('F5 F5 55'), 'answer_bytes': 4},
    'Ch1': {'command': bytes.fromhex('F5 F5 01'), 'answer_bytes': 5},
    'Ch2': {'command': bytes.fromhex('F5 F5 02'), 'answer_bytes': 5}
}
delft.SPAD_voltage = bytes.fromhex('FA FA')
delft.read_data_protocol = {
    'channel1': {'mask': bytes.fromhex('EBEB'), 'number_of_bytes': 2, 'delays': list()},
    'channel2': {'mask': bytes.fromhex('EDED'), 'number_of_bytes': 2, 'delays': list()},
    'noise1': {'mask': bytes.fromhex('EAEA'), 'number_of_bytes': 2, 'delays': list()},
    'noise2': {'mask': bytes.fromhex('ECEC'), 'number_of_bytes': 2, 'delays': list()}
}

protocols = {
    'hokkaido': hokkaido,
    'delft': delft
}
