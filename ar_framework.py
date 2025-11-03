# Импорты (Всё работает на стандартных либах, я этим доволен)
import socket
from time import sleep
from pickle import dump, load
from os import path

# Пак инструментов для более комфортного и читаемого кода ниже
class ToolPack:

    def __init__(self, type) -> None:
        self.type = type

    # Функция отпарвки пакета на HOST
    def _request(self, mess:any, HOST:tuple) -> bool:
            try:
                sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_DGRAM) # UDP
                sock.sendto(mess.encode(), HOST)
                print(mess)
                sock.close()
                return True
            except Exception as e:
                print(e)
                return False

    # Комбинирование пакета в "понятный" для робота типа type
    def combine_package(self, x:int, y:int, z:int, v:bool) -> str | bool:
        try:
            v = int(v)
            if v in (0, 1):
                if self.type == "M1": return f"g:{x}:{y}:{v}:{z}:0#"
                elif self.type == "M2": return f"p:{x}:{y}:{z}:{v}#"
            else: return False
        except Exception as e:
            print(e)
            return False
        
    # Выбор номера списка iptables в зависимости от type
    def choice_ip(self):
        if self.type == "M1": return 0
        elif self.type == "M2": return 1

    # Обновление файла позиции
    @staticmethod 
    def update_data_files() -> None | bool:
        try:
            if not path.exists("data.pkl"):
                data = {"X": 200, "Y": 0, "Z":90}
                with open("data.pkl", "wb") as file: dump(data, file)
            else: return True
        except Exception as e:
            print(e)
            return False

    # Сохранение позиции
    @staticmethod
    def load_position() -> list:
        try:
            with open("data.pkl", "rb") as file:
                return load(file)
        except Exception as e:
            print(e)
            return False

    # Загрузка позиции
    @staticmethod
    def save_position(x:int, y:int, z:int) -> None:
            try:
                data = {"X":x, "Y":y, "Z":z}
                with open("data.pkl", "wb") as file: dump(data, file)
                return True
            except Exception as e:
                print(e)
                return False

# Основной класс для всех роботов площадки
class Robots:
    def __init__(self, iptables, sleep_time = 2, grap_position = 10, type = "M1"):
        self.ToolPack = ToolPack(type=type)
        self.ToolPack.update_data_files()
        self.vac_status = False
        self.iptables = iptables
        self.HOST = (self.iptables[self.ToolPack.choice_ip()], self.iptables[5])
        self.sleep_time = sleep_time
        self.grap_position = grap_position
        self.Robot = self.Robot_(self, type)

    # Основной класс робота M1 и M2 в зависимости от аргумента type
    class Robot_:
        def __init__(self, parent, type):
             self.parent = parent
             self.ToolPack = parent.ToolPack
             self.type = type

        # Возвращает позицию манипулятора M1 или M2
        def get_position(self) -> list:
            pos = self.parent.ToolPack.load_position()
            return (pos["X"], pos["Y"], pos["Z"])

        # Функция перемещения
        def move_to(self, x:int, y:int, z:int) -> bool:
            try:
                self.ToolPack._request(HOST=self.parent.HOST, mess=self.ToolPack.combine_package(x=x, y=y, z=z, v=self.parent.vac_status))

                self.parent.ToolPack.save_position(x, y, z)

                sleep(self.parent.sleep_time)

                return True
            except Exception as e:
                print(e)
                return False

        # Взять шарик с палетки
        def pick_ball(self) -> None:
            self.parent.vac_status = True
            pos = self.parent.ToolPack.load_position()
            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = pos["X"], y = pos["Y"],z = self.parent.grap_position, v = self.parent.vac_status))

            sleep(self.parent.sleep_time)

            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = pos["X"], y = pos["Y"],z = pos["Z"], v = self.parent.vac_status))

        # Положить мяч на палетку
        def drop_ball(self) -> None:
            self.parent.vac_status = False

            pos = self.parent.ToolPack.load_position()

            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = pos["X"], y = pos["Y"],z = 10, v = self.parent.vac_status))

            sleep(self.parent.sleep_time)

            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = pos["X"], y = pos["Y"],z = pos["Z"], v = self.parent.vac_status))






    #g:x:y:v:z:0#
    #p:x:y:z:v#