import socket
import subprocess
import time

from cls.furnace_data import FurnaceData


class FurnaceIO:
    temperature = 0

    def __init__(self, ip: str, port: str):
        self.ip = ip
        self.port = port

    def check_ping(self) -> bool:
        """
        Check resuorce availability
        :return: bool: resource is available or not
        """
        try:
            response = subprocess.check_output(f"ping -n 1 {self.ip}",
                                               shell=True).decode("cp866")

            if "TTL" in response:
                print(f'resource {self.ip} is avalable,')
                return True
            else:
                print(f'resource {self.ip} + is unavalable')
                return False

        except:
            print(f'{self.ip} - Invalid Hostname')
            return False

    def scanCell(self, cell_n: int) -> str:
        """
        Get data from setup memory cell
        :param cell_n: memory cell adrress
        :return: cell value in string
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.ip, int(self.port)))
            str_2_send = "Get:" + str(cell_n)
            print('->', str_2_send)
            sock.sendall(str_2_send.encode())
            time.sleep(0.01)
            str_get = sock.recv(16)
            print('<-', str_get)
            sock.close()
        return str_get.decode()

    def get_current_data(self) -> FurnaceData:
        """
        Get furnace temperature and working setpoint
        :return: class FurnaceData object
        """
        return FurnaceData(temperature=self.scanCell(cell_n=1),
                           working_set_point=self.scanCell(cell_n=2))
