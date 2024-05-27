def generate_matrices(N, M):
    def is_valid(matrix, row, col):
        # Проверяем строку
        for c in range(M):
            if matrix[row][c] == 1:
                return False
        # Проверяем столбец
        for r in range(N):
            if matrix[r][col] == 1:
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

# Пример использования:
N = 3  # количество строк
M = 4  # количество столбцов
matrices = generate_matrices(N, M)

# Вывод всех матриц
for idx, matrix in enumerate(matrices):
    print(f"Matrix {idx + 1}:")
    for row in matrix:
        print(row)
    print()
