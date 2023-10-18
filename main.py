import csv
from loguru import logger


class Room:
    def __init__(self, name, length, width, height):
        self.name = name
        self.length = length
        self.width = width
        self.height = height

    def calculate_wall_area(self):
        logger.success("Площадь стен посчитана")
        return 2 * (self.length + self.width) * self.height

    def calculate_ceiling_area(self):
        logger.success("Площадь потолка посчитана")
        return self.length * self.width

    def calculate_floor_area(self):
        logger.success("Площадь пола посчитана")
        return self.length * self.width


class Apartment:
    def __init__(self):
        self.rooms = []
        self.total_wall_area = 0
        self.total_ceiling_area = 0
        self.total_floor_area = 0

    def add_room(self, room):
        self.rooms.append(room)
        self.total_wall_area += room.calculate_wall_area()
        self.total_ceiling_area += room.calculate_ceiling_area()
        self.total_floor_area += room.calculate_floor_area()
        logger.success("Комната добавлена")


    def calculate_total_cost(self, wall_cost, ceiling_cost, floor_cost):
        total_cost = (self.total_wall_area * wall_cost +
                      self.total_ceiling_area * ceiling_cost +
                      self.total_floor_area * floor_cost)
        logger.success(f"Результат посчитан total_cost = {total_cost}")
        return total_cost

@logger.catch
def main():
    logger.remove()
    logger.add("app.log")
    logger.debug("Программа инициализирована")

    apartment = Apartment()

    while True:
        name = input("Введите название комнаты (или 'завершить' для завершения): ")
        if name.lower() == 'завершить':
            break
        logger.info(f"Пользователь ввёл данные name = {name}")

        try:
            length = float(input("Введите длину комнаты в метрах: "))
            logger.info(f"Пользователь ввёл данные length = {length}")
            width = float(input("Введите ширину комнаты в метрах: "))
            logger.info(f"Пользователь ввёл данные width = {width}")
            height = float(input("Введите высоту потолка в метрах: "))
            logger.info(f"Пользователь ввёл данные height = {height}")
        except ValueError:
            logger.error("Неверный формат данных. Пожалуйста, введите числа.")
            continue

        room = Room(name, length, width, height)
        apartment.add_room(room)

    wall_cost = float(input("Введите стоимость обоев за квадратный метр: "))
    logger.info(f"Пользователь ввёл данные wall_cost = {wall_cost}")
    ceiling_cost = float(input("Введите стоимость натяжки потолков за квадратный метр: "))
    logger.info(f"Пользователь ввёл данные ceiling_cost = {ceiling_cost}")
    floor_cost = float(input("Введите стоимость покрытия пола за квадратный метр: "))
    logger.info(f"Пользователь ввёл данные floor_cost = {floor_cost}")

    total_cost = apartment.calculate_total_cost(wall_cost, ceiling_cost, floor_cost)

    with open('results.csv', mode='w', newline='') as file:
        logger.info("Открыт файл results.csv")
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Комната", "Площадь стен", "Площадь потолка", "Площадь пола"])
        for room in apartment.rooms:
            writer.writerow(
                [room.name, room.calculate_wall_area(), room.calculate_ceiling_area(), room.calculate_floor_area()])
        writer.writerow(["Итого", apartment.total_wall_area, apartment.total_ceiling_area, apartment.total_floor_area])
        writer.writerow(
            ["Стоимость работ", wall_cost * apartment.total_wall_area, ceiling_cost * apartment.total_ceiling_area,
             floor_cost * apartment.total_floor_area])
        writer.writerow(["Общая стоимость работ", total_cost])
    return True


if __name__ == "__main__":
    good = main()
    if good:
        logger.success("Расчёт стоимости окончен. Программа завершена.")
    else:
        logger.critical("Что-то произошло в процессе работы программы.")
