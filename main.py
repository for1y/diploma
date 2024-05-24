from random import randint


class BLA():
    def __init__(self, x, y, current_fuel, fuel_capacity):
        self.x = x
        self.y = y
        self.fuel = current_fuel
        self.fuel_capacity = fuel_capacity
        self.targets = []


class Target():
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.type = 0.5 * (n - 1)


def create_BLAs(count):
    list_BLAs = []
    for i in range(count):
        list_BLAs.append(BLA(randint(1, field_size_x), randint(1, field_size_y), randint(1, standard_fuel_capacity),
                             standard_fuel_capacity))
    return list_BLAs


if __name__ == '__main__':
    standard_fuel_capacity = 100
    field_size_x = 1000
    field_size_y = 1000
    print(randint(1, 3))
