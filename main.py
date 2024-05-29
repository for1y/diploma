import copy
from random import randint

import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, blas, targets):
        self.blas: list[BLA] = blas
        self.targets: list[Target] = targets

    def draw(self):
        fig, ax = plt.subplots(figsize=(graph_screen_size / 96, graph_screen_size / 96))
        ax.set_xlim([min_field_size_x, max_field_size_x])
        ax.set_ylim([min_field_size_y, max_field_size_y])

        # Отрисовка целей как треугольников, цвет зависит от type
        color = ['black', 'orange', 'red']
        for target in self.targets:
            triangle = self.draw_triangle_with_center(target.x, target.y, color=color[target.type - 1])
            plt.text(target.x, target.y + fig_size, f't:{target.id}', horizontalalignment='center')
            ax.add_patch(triangle)

        # Отрисовка BLAs как голубых прямоугольников
        for bla in self.blas:
            bla.update_visible_objects()

            rect = self.rectangle_with_center(bla.x, bla.y)
            circ = plt.Circle((bla.x, bla.y), bla.visability_radius, fill=None, linestyle='--')
            bla_target = bla.find_general_target()
            if bla_target:
                plt.plot([bla.x, bla_target.x], [bla.y, bla_target.y])

            plt.text(bla.x, bla.y + fig_size, f'b:{bla.id}')
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


class Target:
    def __init__(self, x, y, n, index):
        self.id: int = index
        self.x: int = x
        self.y: int = y
        self.type: int = n
        self.worth: float = 0.5 * (n - 1)


class BLA:
    def __init__(self, x, y, current_fuel, index):
        self.id: int = index

        self.x: int = x
        self.y: int = y
        self.visability_radius: int = standard_radius_vision

        self.visible_targets: list[Target] = []
        self.visible_BLAs: list[BLA] = []

        self.fuel: int = current_fuel
        self.fuel_capacity: int = standard_fuel_capacity

    def win_probability(self, target: Target) -> float:
        distance = self.distance_to(target)
        sij = distance / self.visability_radius

        if target.type == 3:
            rho = (-2 / 3 * sij + 1)
        else:
            rho = 1 / 3 * sij

        cij = rho * (target.worth - sij)
        return cij

    def distance_to(self, target: Target):
        return ((self.x - target.x) ** 2 + (self.y - target.y) ** 2) ** 0.5

    def find_visible_objects(self, list_objects):
        visible_objects = [target for target in list_objects if
                           self.distance_to(target) <= self.visability_radius and self.distance_to(target) > 0]
        return visible_objects

    def update_visible_objects(self):
        self.visible_targets.clear()
        self.visible_BLAs.clear()

        self.visible_targets = self.find_visible_objects(list_targets)
        self.visible_BLAs = self.find_visible_objects(list_BLAs)

    def find_general_target(self) -> Target or None:
        rows: list[BLA] = self.visible_BLAs
        rows.insert(0, self)
        cols: list[Target] = self.visible_targets
        matrices = generate_matrices(len(rows), len(cols) + 1)
        max_sum_win_probability: float = 0
        index_max_worth_matrix: int = 0

        for index_m, matrix in enumerate(matrices):
            sum_win_probability: float = 0
            # print(f'matrix:{matrix}')
            for m_rows in matrix:
                # print(f'm_rows::{m_rows}')
                for m_col in m_rows:
                    # print(f'm_col:{m_col}')
                    if m_col == 1 and m_rows.index(m_col) == len(cols):
                        sum_win_probability += self.fuel / self.fuel_capacity

                    elif m_col == 1:
                        col_index: int = m_rows.index(m_col)
                        row_index: int = matrix.index(m_rows)
                        bla: BLA = rows[row_index]
                        target: Target = cols[col_index]
                        win_probability: float = bla.win_probability(target)

                        # print(m_rows)
                        # print(f'cols:{cols}\t{col_index}\tlen(cols):{len(cols)}')
                        # print(f'for bla {self.id}:--> bla_id:{bla.id} \t with \t t_id:{target.id} have {win_probability}')

                        sum_win_probability += win_probability

                if sum_win_probability > max_sum_win_probability:
                    max_sum_win_probability = sum_win_probability
                    index_max_worth_matrix = index_m
        general_target_index: int = matrices[index_max_worth_matrix][0].index(1)

        if general_target_index == len(cols):
            print(f'--------------------------------------------------------------')
            print(f'bla:{self.id} :\t: {self.fuel} :\t: {max_sum_win_probability} :\t: dont attack anywhere')
            print(f'--------------------------------------------------------------')
            return None
        else:
            general_target: Target = cols[general_target_index]
            print(f'--------------------------------------------------------------')
            print(f'bla:{self.id} :\t: {self.fuel} :\t: {max_sum_win_probability} :\t: attack on {general_target.id}')
            print(f'--------------------------------------------------------------')
            return general_target


def create_blas(count: int) -> list[BLA]:
    list_of_blas = []
    for i in range(count):
        x_cord = randint(min_field_size_x, max_field_size_x)
        y_cord = randint(min_field_size_y, max_field_size_y)
        fuel = randint(1, standard_fuel_capacity)

        list_of_blas.append(BLA(x_cord, y_cord, 0, i + 1))
    return list_of_blas


def create_targets(count: int) -> list[Target]:
    list_of_targets = []
    for i in range(count):
        x_cord = randint(min_field_size_x, max_field_size_x)
        y_cord = randint(min_field_size_y, max_field_size_y)
        target_type = randint(1, 3)

        list_of_targets.append(Target(x_cord, y_cord, target_type, i + 1))
    return list_of_targets


def generate_matrices(N: int, M: int) -> list[list[int]]:
    matrices = []

    def is_valid(matrix: list[int], row: int, col: int):
        # Проверяем строку
        sum_row: int = 0
        for i in range(M):
            sum_row += matrix[row][i]
            if sum_row == 1:
                return False
        # Проверяем столбец
        sum_col: int = 0
        for i in range(N):
            if col != M - 1:
                sum_col += matrix[i][col]
                if sum_col == 1 or col == M:
                    return False
        return True

    def recursive_generate(matrix, row):
        nonlocal matrices
        if row == N:
            # Когда все строки обработаны, добавляем копию текущей матрицы в список
            matrices.append(copy.deepcopy(matrix))  # Глубокое копирование матрицы
            return

        # Пробуем разместить единицу в каждом столбце текущей строки
        for col in range(M):
            if is_valid(matrix, row, col):
                matrix[row][col] = 1
                recursive_generate(matrix, row + 1)
                matrix[row][col] = 0  # откат изменений

    # Создаем пустую матрицу
    matrix = [[0] * M for _ in range(N)]
    # Запускаем рекурсивную генерацию с первой строки
    recursive_generate(matrix, 0)
    return matrices


if __name__ == '__main__':
    # параметры для БЛА
    standard_fuel_capacity = 100
    standard_radius_vision = 500

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
    count_targets = 5
    count_blas = 10

    list_BLAs = create_blas(count_blas)
    list_targets = create_targets(count_targets)

    visualizer = Visualizer(list_BLAs, list_targets)
    visualizer.draw()
