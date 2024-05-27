from random import randint

import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, blas, targets):
        self.blas = blas
        self.targets = targets

    def draw(self):
        fig, ax = plt.subplots(figsize=(graph_screen_size / 96, graph_screen_size / 96))
        ax.set_xlim([min_field_size_x, max_field_size_x])
        ax.set_ylim([min_field_size_y, max_field_size_y])

        # Отрисовка целей как треугольников, цвет зависит от type
        color = ['black', 'orange', 'red']
        for target in self.targets:
            triangle = self.draw_triangle_with_center(target.x, target.y, color=color[target.type - 1])
            ax.add_patch(triangle)

        # Отрисовка BLAs как голубых прямоугольников
        for bla in self.blas:
            rect = self.rectangle_with_center(bla.x, bla.y)
            circ = plt.Circle((bla.x, bla.y), bla.radius_vision, fill=None, linestyle='--')
            plt.text(bla.x, bla.y + fig_size, f'{bla.index}')
            ax.add_patch(circ)
            ax.add_patch(rect)

        plt.show()

    def rectangle_with_center(self, x, y, color='blue'):
        """
        Рисует прямоугольник с центром в точке (x, y).
        :param x: Координата x центра прямоугольника.
        :param y: Координата y центра прямоугольника.
        :param color: Цвет прямоугольника
        """

        # Расчет позиции верхнего левого угла прямоугольника
        left = x - fig_size / 2
        top = y - fig_size / 2

        # Создание прямоугольника
        return plt.Rectangle((left, top), fig_size, fig_size, fill=color, edgecolor=color)

    def draw_triangle_with_center(self, x, y, color='red'):
        """
        Рисует треугольник с центром в точке (x, y).

        :param x: Координата x центра треугольника.
        :param y: Координата y центра треугольника.
        :param color: Цвет треугольника.
        """

        # Определяем вершины треугольника
        vertices = [(x - fig_size / 2, y - fig_size / 2),  # Левый нижний
                    (x + fig_size / 2, y - fig_size / 2),  # Правый нижний
                    (x, y + fig_size / 2)]  # Центр

        # Создаем треугольник
        return plt.Polygon(vertices, closed=True, fill=True, color=color)


class BLA:
    def __init__(self, x, y, current_fuel, index):
        self.index = index

        self.x = x
        self.y = y
        self.radius_vision = standard_radius_vision

        self.visible_targets = []
        self.visible_BLAs = []

        self.fuel = current_fuel
        self.fuel_capacity = standard_fuel_capacity

    def distance_to(self, target):
        return ((self.x - target.x) ** 2 + (self.y - target.y) ** 2) ** 0.5

    def find_visible_objects(self, list_objects):
        visible_objects = [target for target in list_objects if self.distance_to(target) <= self.radius_vision]
        return visible_objects

    def update_visible_objects(self):
        self.visible_targets.clear()
        self.visible_BLAs.clear()

        self.visible_targets = self.find_visible_objects(list_targets)
        self.visible_BLAs = self.find_visible_objects(list_BLAs)


class Target:
    def __init__(self, x, y, n):
        self.x = x
        self.y = y
        self.type = n
        self.worth = 0.5 * (n - 1)


def create_blas(count):
    list_of_blas = []
    for i in range(count):
        x_cord = randint(min_field_size_x, max_field_size_x)
        y_cord = randint(min_field_size_y, max_field_size_y)
        fuel = randint(1, standard_fuel_capacity)

        list_of_blas.append(BLA(x_cord, y_cord, fuel, i + 1))
    return list_of_blas


def create_targets(count):
    list_of_targets = []
    for i in range(count):
        x_cord = randint(min_field_size_x, max_field_size_x)
        y_cord = randint(min_field_size_y, max_field_size_y)
        target_type = randint(1, 3)

        list_of_targets.append(Target(x_cord, y_cord, target_type))
    return list_of_targets

def generate_matrices(N, M):
    def is_valid(matrix, row, col):
        # Проверяем строку
        if sum(matrix[row][:]) == 1:
            return False

        # Проверяем столбец
        if sum(matrix[:][col]) == 1:
            return False

        return True

    def recursive_generate(matrix, row, matrices):
        if row == N:
            # Когда все строки обработаны, добавляем текущую матрицу в список
            matrices.append([row[:] for row in matrix])
            return

        # Пробуем разместить единицу в каждом столбце текущей строки
        for col in range(M):
            if is_valid(matrix, row, col):
                matrix[row][col] = 1
                recursive_generate(matrix, row + 1, matrices)
                matrix[row][col] = 0  # откат изменений

        # Также рассматриваем вариант без единицы в текущей строке
        recursive_generate(matrix, row + 1, matrices)

    # Создаем пустую матрицу
    matrix = [[0] * M for _ in range(N)]
    matrices = []
    # Запускаем рекурсивную генерацию с первой строки
    recursive_generate(matrix, 0, matrices)
    return matrices




if __name__ == '__main__':
    # параметры для БЛА
    standard_fuel_capacity = 100
    standard_radius_vision = 400

    # размер окна с графиком
    graph_screen_size = 800

    # ограничения размера оси графиков
    max_field_size_x = 1000
    min_field_size_x = 0
    max_field_size_y = 1000
    min_field_size_y = 0

    # параметры размеров фигур на плоскости
    fig_zoom = 50
    fig_size = (((max_field_size_x - min_field_size_x) + (max_field_size_y - min_field_size_y)) / 2 / fig_zoom)
    # кол-во БЛА и целей
    count_targets = 20
    count_blas = 5

    list_BLAs = create_blas(count_blas)
    list_targets = create_targets(count_targets)

    visualizer = Visualizer(list_BLAs, list_targets)
    visualizer.draw()

    # Пример использования:
    N = 3  # количество строк
    M = 3  # количество столбцов
    matrices = generate_matrices(N, M)

    # Вывод всех матриц
    for idx, matrix in enumerate(matrices):
        print(f"Matrix {idx + 1}:")
        for row in matrix:
            print(row)
        print('\n')
