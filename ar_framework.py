# Импорты (Всё работает на стандартных либах, я этим доволен)
import socket
from time import sleep

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

# Класс позиции, как будто далее будет удалён или перемещён
class Position:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

# Основной класс для всех роботов площадки
class Robots:
    def __init__(self, iptables, sleep_time = 2, grap_position = 10, type = "M1"):
        self.position = Position(200, 0, 90)
        self.ToolPack = ToolPack(type=type)
        self.vac_status = False
        self.iptables = iptables
        self.HOST = (self.iptables[0], self.iptables[5])
        self.sleep_time = sleep_time
        self.grap_position = grap_position
        self.Robot = self.Robot_(self, type)

    #Основной класс робота M1 и M2 в зависимости от аргумента type
    class Robot_:
        def __init__(self, parent, type):
             self.parent = parent
             self.ToolPack = parent.ToolPack
             self.type = type

        #Возвращает позицию манипулятора M1 или M2
        def get_position(self) -> Position:
            return self.parent.position
        
        def get_all_position(self) -> Position:
            return self.parent.position.x, self.parent.position.y, self.parent.position.z

        #Функция перемещения (без защиты)
        def move_to(self, x:int, y:int, z:int) -> bool:
            try:
                self.ToolPack._request(HOST=self.parent.HOST, mess=self.ToolPack.combine_package(x=x, y=y, z=z, v=self.parent.vac_status))

                self.parent.position.x = x
                self.parent.position.y = y
                self.parent.position.z = z

                sleep(self.parent.sleep_time)

                return True
            except Exception as e:
                print(e)
                return False

        # Взять шарик с палетки
        def pick_ball(self):
            self.parent.vac_status = True
            #_request(HOST=self.parent.HOST, mess=f"g:{self.parent.position.x}:{self.parent.position.y}:{self.parent.vac_status}:10:0#")
            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = self.parent.position.x, y = self.parent.position.y, z = self.parent.grap_position, v = self.parent.vac_status))

            sleep(self.parent.sleep_time)

            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = self.parent.position.x, y = self.parent.position.y, z = self.parent.position.z, v = self.parent.vac_status))

        # Положить мяч на палетку
        def drop_ball(self):
            self.parent.vac_status = False
            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = self.parent.position.x, y = self.parent.position.y, z = self.parent.grap_position, v = self.parent.vac_status))

            sleep(self.parent.sleep_time)

            self.ToolPack._request(HOST = self.parent.HOST, mess=self.ToolPack.combine_package(x = self.parent.position.x, y = self.parent.position.y, z = self.parent.position.z, v = self.parent.vac_status))

        # Перемещает манипулятор M1 или M2 в парковочную зону (с защитой)
        def go_to_parking(self):
            x0, y0 = self.parent.position.x, self.parent.position.y
            x_parking, y_parking = 140, -180

            path = []

            if y0 > 0 and y_parking < 0:
                path.append((150, 150))
                path.append((200, 0))

            path.append((x_parking, y_parking))

            for x, y in path:
                sleep(self.parent.sleep_time)
                self.move_to(x, y, z=90)






    #g:x:y:v:z:0#
    #p:x:y:z:v#