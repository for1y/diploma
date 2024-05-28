import copy  # Импортируем модуль copy для глубокого копирования


def is_valid(matrix, row, col, N, M):
    # Проверяем строку
    sum_row = 0
    for i in range(M):
        sum_row += matrix[row][i]
        if sum_row == 1:
            return False
    # Проверяем столбец
    sum_col = 0
    for i in range(N):
        if col != M - 1:
            sum_col += matrix[i][col]
            if sum_col == 1 or col == M:
                return False
    return True


def generate_matrices(N, M) -> list:
    matrices = []

    def recursive_generate(matrix, row):
        nonlocal matrices
        if row == N:
            # Когда все строки обработаны, добавляем копию текущей матрицы в список
            matrices.append(copy.deepcopy(matrix))  # Глубокое копирование матрицы
            return

        # Пробуем разместить единицу в каждом столбце текущей строки
        for col in range(M):
            if is_valid(matrix, row, col, N, M):
                matrix[row][col] = 1
                recursive_generate(matrix, row + 1)
                matrix[row][col] = 0  # откат изменений

    # Создаем пустую матрицу
    matrix = [[0] * M for _ in range(N)]
    # Запускаем рекурсивную генерацию с первой строки
    recursive_generate(matrix, 0)
    print('end')
    return matrices


# Пример использования:
N = 3  # размер матрицы N x M
M = 4
matrices = generate_matrices(N, M)
for i, matrix in enumerate(matrices, start=1):
    print(f"Matrix {i}:")
    for row in matrix:
        print(row)
    print()  # Отступ между матрицами
