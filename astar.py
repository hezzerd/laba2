import numpy as np
import random
from heapq import heappop, heappush
from PIL import Image


def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def astar(array, start, goal):
    # создание списка приоритетов и добавление стартового узла
    heap = []
    heappush(heap, (0, start))
    # создание словаря для представления расстояний
    distances = {start: 0}
    # создание словаря для представления пути
    path = {start: []}
    # создание списка для хранения посещенных узлов
    visited = set()
    # основной цикл A*
    while heap:
        # извлечение узла с минимальным расстоянием
        (distance, current) = heappop(heap)
        # проверка, является ли текущий узел конечным
        if current == goal:
            return path[current] + [current]
        # добавление узла в список посещенных
        visited.add(current)
        # итерация по соседним узлам
        for i, j in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            # координаты соседнего узла
            neighbor = current[0] + i, current[1] + j
            # проверка, что соседний узел находится внутри матрицы
            if 0 <= neighbor[0] < array.shape[0] and 0 <= neighbor[1] < array.shape[1]:
                # проверка, что соседний узел имеет значение 1 и еще не посещен
                if array[neighbor] == 1 and neighbor not in visited:
                    # вычисление нового расстояния
                    new_distance = distances[current] + 1
                    # проверка, есть ли новый путь короче старого
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        priority = new_distance + heuristic(goal, neighbor)
                        heappush(heap, (priority, neighbor))
                        path[neighbor] = path[current] + [current]
    # если конечный узел недостижим, возвращаем None
    return None

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


#8. Создание списка для хранения посещенных элементов матрицы и добавление в него стартового элемента:


visited = []
visited.append((start_x, start_y))

start = start_x, start_y
goal = end_x, end_y
path = astar(matrix, start, goal)


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
        elif el == 5:
            pixels.extend([(255, 0, 0)])

print(matrix)
print(path)

# Устанавливаем пиксели в изображение
image.putdata(pixels)

# Сохраняем изображение в файле
image.save('matrix.png')