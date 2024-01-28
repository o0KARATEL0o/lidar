import pathlib
import com_port
import PySimpleGUI as sg
import datetime
from measure import measure
from project_log import project_logger
from protocols import protocols
from threading import Thread


lidar_port = None
measurements = False
toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'

if __name__ == "__main__":
    project_logger.info('Start program')
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('COM Port')],
        [sg.LBox(values=com_port.available_com_ports(),
                 size=(20, 10), key='com_port'),
         sg.LBox(values=[9600, 115200, 460800], size=(20, 10), key='baudrate'),
         sg.LBox(values=list(protocols.keys()), size=(20, 10), key='Protocol')],
        [sg.Text('Off'), sg.Button(image_data=toggle_btn_off, key='Connect', button_color=(
            sg.theme_background_color(), sg.theme_background_color()), border_width=0), sg.Text('On')],
        [sg.Text('Папка для сохранения файлов')],
        [sg.Input(key='folder'), sg.FolderBrowse(target='folder')],
        [sg.Text('Количество импульсов\nв измерении'),
         sg.Text('Время и дата\nначала измерений')],
        [sg.LBox(values=[50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 64000, 100000, 200000, 500000, 1000000, 2000000], size=(
            20, 10), key='pulses'),
         sg.Input(default_text=datetime.datetime.now().strftime(
             '%Y-%m-%d %H:%M:%S'), key='date', size=(20, 10)),
         sg.CalendarButton('Выберете дату', close_when_date_chosen=True, target='date')],
        [sg.Text('Период измерений в минутах'),
         sg.Input(default_text='10', size=(20, 1), key='period')],
        [sg.Text('Количество измерений'),
         sg.Input(default_text='1', size=(20, 1), key='count')],
        [sg.Button('Start'), sg.Button('Start series'),
         sg.Button('Stop'), sg.Button('Exit')]



    ]
    window = sg.Window('Test', layout)
    project_logger.debug(f'Window is generated {window}')

    while True:
        event, values = window.read()
        project_logger.debug(f'Event is {event}')
        project_logger.debug(f'Values is {values}')
        if event == sg.WIN_CLOSED or event == 'Exit':
            if measurements:
                for measurement in measurements:
                    if measurement.is_alive():
                        project_logger.info(
                            f'Measurement {measurement.name} in progress')
                    measurement.join()
            if lidar_port:
                lidar_port.close()
                project_logger.debug('COM port is closed')
            break
        if event == 'Connect':
            if lidar_port:
                lidar_port.close()
                lidar_port = False
                project_logger.debug('COM port is closed')
                window['Connect'].update(
                    image_data=toggle_btn_off
                )
            else:
                try:
                    lidar_port = com_port.LiDAR_Port(
                        values['com_port'][0], (values['baudrate'][0]), protocol=protocols.get(values['Protocol'][0]))
                    window['Connect'].update(
                        image_data=toggle_btn_on if lidar_port is not None else toggle_btn_off)
                    project_logger.debug(f'COM port {lidar_port} is connected')
                except IndexError as index_error:
                    sg.popup_error(
                        'Error', f'Выберете COM порт и скорость\n{index_error}')
                    project_logger.error(
                        f'COM port and baudrate\nNot selected{index_error}')
                    window['Connect'].update(
                        image_data=toggle_btn_off
                    )
                except Exception as e:
                    sg.popup_error('Error',
                                   f'{e}\nCOM {values["com_port"]} baud {values["baudrate"]}')
                    project_logger.error(
                        f'{e}\nCOM {values["com_port"]} baud {values["baudrate"]}')
                    window['Connect'].update(image_data=toggle_btn_off)
        if event == 'Start series':
            if lidar_port:
                pass
            else:
                project_logger.error(
                    'COM port not connected.Can not start measurements')
                sg.popup_error('Error', 'COM port not connected')
        if event == 'Start':
            if lidar_port:
                try:
                    counts = int(values['count'])
                    pulses = int(values['pulses'][0])
                    folder = pathlib.Path(values['folder'])
                except Exception as e:
                    sg.popup_error('Error', f'{e}')
                    project_logger.error(f'{e}')
                    continue
                project_logger.debug('Start measurements')
                measurements = [Thread(target=measure, name='Measure #' + str(
                    i), args=(lidar_port, folder, pulses)) for i in range(counts)]
                for measurement in measurements:
                    measurement.start()

            else:
                project_logger.error(
                    'COM port not connected.Can not start measurements')
                sg.popup_error('Error', 'COM port not connected')
        if event == 'Stop':
            pass
    project_logger.debug('Window is closed')
    window.close()
