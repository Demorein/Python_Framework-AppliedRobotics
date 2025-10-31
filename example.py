import ar_framework
import config

Robot_M1 = ar_framework.Robots(iptables=config.iptables, type="M1") # Объект робота M1, можно поменять на M2

print(Robot_M1.Robot.get_all_position()) # Выведет стартовую позицию робота при включении x200 y0 z90 в формате (200, 0, 90)

Robot_M1.Robot.move_to(150,150,50) # Отправляет робота на координаты x150 y150 z50

print(Robot_M1.Robot.get_position().x) # Выводит одну координату x
print(Robot_M1.Robot.get_position().y) # Выводит одну координату y
print(Robot_M1.Robot.get_position().z) # Выводит одну координату z

Robot_M1.Robot.pick_ball() # Робот возьмёт шарик под своими координатами
Robot_M1.Robot.drop_ball() # Робот отпустит шарик под своими координатами

Robot_M1.Robot.go_to_parking() # Отпавляет робота на парковочную зону при необходимости через промижуточную точку на x150 y150 z90 и x200 y0 z 90