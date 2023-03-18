import numpy as np
import random
from heapq import heappop, heappush
from PIL import Image


#2. Создание матрицы размером 20 на 20 и заполнение ее 1-ми и не пересекающимися прямогугольниками заполнеными 2-ми :

matrix = np.ones((20, 20))

width_all = 20
height_all = 20


rectangles_len = 15 #количество препятсвтий
rectangles = [0 for _ in range(rectangles_len)]


for i in range(rectangles_len):
    flag = False
    while flag is False:
        x_0 = random.randint(1, 14)
        y_0 = random.randint(1, 14)
        width = random.randint(1, 4)
        height = random.randint(1, 4)
        rectangles[i] = ([x_0, y_0, x_0 + width, y_0 + height])
        flag_1 = False
        for j in range(rectangles[i][0], rectangles[i][2]):
            for k in range(rectangles[i][1], rectangles[i][3]):
                if matrix[j][k] == 2 or matrix[j + 1][k] == 2 or matrix[j - 1][k] == 2 or matrix[j][k + 1] == 2 or matrix[j][k - 1] == 2 or matrix[j + 1][k + 1] == 2 or matrix[j - 1][k - 1] == 2 or matrix[j + 1][k - 1] == 2 or matrix[j - 1][k + 1] == 2:
                    flag_1 = True
        flag = not flag_1
        if flag_1 is False:
            for j in range(rectangles[i][0], rectangles[i][2]):
                for k in range(rectangles[i][1], rectangles[i][3]):
                        matrix[j][k] = 2



#3. Выбор случайных координат стартового и конечного элементов с помощью функции random:
start_x, start_y = random.randint(0, 19), random.randint(0, 19)
end_x, end_y = random.randint(0, 19), random.randint(0, 19)


#4. Проверка, что выбранные координаты соответствуют элементам матрицы со значением 1, иначе повторить шаг 3:


while matrix[start_x][start_y] != 1 or matrix[end_x][end_y] != 1:
    start_x, start_y = random.randint(0, 19), random.randint(0, 19)
    end_x, end_y = random.randint(0, 19), random.randint(0, 19)
print(start_x, start_y)
print(end_x, end_y)

#5. Инициализация списка приоритетов и словаря для представления дистанций:


heap = []
distances = {}


#6. Добавление стартового элемента в список приоритетов и установление его дистанции равной 0:


heappush(heap, (0, start_x, start_y))
distances[(start_x, start_y)] = 0


#7. Инициализация переменной для хранения пути:


path = []

#8. Создание списка для хранения посещенных элементов матрицы и добавление в него стартового элемента:


visited = []
visited.append((start_x, start_y))


#9. Основной цикл алгоритма Дейкстры:


while heap:
    # извлечение элемента с минимальной дистанцией
    (distance, current_x, current_y) = heappop(heap)

    # проверка, является ли текущий элемент конечным
    if current_x == end_x and current_y == end_y:
        # обратный проход для восстановления пути
        while current_x != start_x or current_y != start_y:
            path.append((current_x, current_y))
            (current_x, current_y) = distances[(current_x, current_y)][1]
        # инвертируем путь, чтобы получить его в нужном порядке
        path.append((start_x, start_y))
        path.reverse()
        break

    # итерация по соседним элементам
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_x, new_y = current_x + i, current_y + j
            # проверка, что новые координаты находятся внутри матрицы
            if 0 <= new_x < matrix.shape[0] and 0 <= new_y < matrix.shape[1]:
                # проверка, что новый элемент еще не посещен и имеет значение 1
                if (new_x, new_y) not in visited and matrix[new_x][new_y] == 1:
                    # расчет новой дистанции и добавление нового элемента в список приоритетов
                    new_distance = distance + (i**2 + j**2)**0.5 # формула евклидова расстояния
                    heappush(heap, (new_distance, new_x, new_y))
                    distances[(new_x, new_y)] = (new_distance, (current_x, current_y))

    # добавление текущего элемента в список посещенных
    visited.append((current_x, current_y))


#10. Изменение элементов пути на 5 в матрице:


for x, y in path:
    matrix[x][y] = 5


# 11. Вывод матрицы на экран:

# Размеры изображения
width, height = len(matrix[0]), len(matrix)

# Создаём изображение
image = Image.new('RGB', (width, height), color='white')

# Преобразуем матрицу в пиксели
pixels = []
for row in matrix:
    for el in row:
        # Если элемент матрицы равен 1, ставим белый цвет пикселя
        if el == 1:
            pixels.extend([(255, 255, 255)])
        # Если элемент матрицы равен 2, ставим черный цвет пикселя
        elif el == 2:
            pixels.extend([(0, 0, 0)])
        # Если элемент матрицы равен 5, ставим красный цвет пикселя
        #elif el == 5:
        #    pixels.extend([(255, 0, 0)])

print(matrix)
print(path)

# Устанавливаем пиксели в изображение
image.putdata(pixels)

# Сохраняем изображение в файле
image.save('matrix.png')