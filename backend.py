import numpy as np
import random
import matplotlib.pyplot as plt
# Квадратичная двухфакторная модель
def model_v1(x, delta):
 return [[mu1(x[0], delta)], [mu2(x[1], delta)], [mu1(x[0], delta) * x[0]], [mu2(x[1], delta) * x[0]],[mu1(x[0], delta) * x[1]],[mu2(x[1], delta) * x[1]]]
def model_v2(x, delta):
 return [[1], [x[0]], [x[1]], [mu1(x[0], delta)], [mu2(x[1], delta)], [mu1(x[0], delta) * x[0]],[mu2(x[1], delta) * x[0]],[mu1(x[0], delta) * x[1]], [mu2(x[1], delta) * x[1]]]
def model(x):
 return [[1], [x[0]], [x[1]], [x[0]*x[1]]]
# Вычисление информационной матрицы
def inf_matrix(x, p, delta):
 M = np.zeros((9, 9))
 for i in range(len(x)):
   M += p[i] * np.dot(model_v2(x[i], delta), np.transpose(model_v2(x[i], delta)))
 return M
# Вычисление дисперсионной матрицы
def disp_matrix(M):
 return np.linalg.inv(M)
# Генерируем регулярную сетку 21х21
def make_dots(n, step):
 x = []
 grid = np.linspace(1, -1, step+1)
 for i in range(len(grid)):
  for j in range(len(grid)):
   x.append([grid[j], grid[i]])
 return x
# Генерируем начальный план
def entrance_plan(x, n):
 x_plan, p_plan = [], []
 for i in range(n):
  p_plan.append(1/n)
  tmp = random.choices(x) # Выбираем случайную точку из сетки
  tmp_x = tmp[0][0]
  tmp_y = tmp[0][1]
  tmp = [tmp_x, tmp_y]
  x_plan.append(tmp)
  x.pop(x.index(tmp)) # Удаляем выбранную точку из сетки
 return x_plan, p_plan
# Вычисление d(x,ε)
def dxe(x, x_plan, p_plan, delta):
 return np.dot(np.dot(np.transpose(model_v2(x, delta)), disp_matrix(inf_matrix(x_plan, p_plan, delta))), model_v2(x, delta))
# Стуктура для графика d(x,ε)
def dxe_plot(x_plan, p_plan, delta):
 dots = []
 grid = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
 for i in range(len(x_plan)):
  dots.append(dxe(x_plan[i], x_plan, p_plan, delta))
 return grid, dots
# Функции принадлежности патриций
def mu1(x, delta):
 if x <= -delta:
  return 1
 elif -delta <= x <= delta:
  return (delta-x)/(2*delta)
 elif x > delta:
  return 0
def mu2(x,delta):
 return 1 - mu1(x, delta)
# Приводим планы в нормальный вид
def normalization(x_plan, n):
 n_plan = []
 p_plan = []
 # Получаем все уникальные точки из плана и их количество
 unique, count = np.unique(x_plan, return_counts=True, axis=0)
 for i in range(len(unique)): # Перезаписываем план в более удобный вид
  n_plan.append(unique[i])
  p_plan.append((1/n)*count[i])
 return n_plan, p_plan
# Характеристики плана (определитель, след)
def plan_parametrs(x_plan, p_plan, delta):
 M = inf_matrix(x_plan, p_plan, delta)
 return np.linalg.det(M), np.trace(np.linalg.inv(M))
# Для последовательного алгоритма достраивания
   """
    Последовательный алгоритм достраивания для синтеза дискретных D-оптимальных планов эксперимента.
    
    Аргументы:
    n -- количество точек в плане
    delta -- параметр модели
    seed -- зерно для генерации случайных чисел
    
    Возвращает:
    n_plan -- список точек плана
    pn_plan -- список вероятностей выбора соответствующих точек
    """
def Sequential(n, delta, seed):
    random.seed(seed)
    step = 20
    x = make_dots(n, step)
    x_plan, p_plan = entrance_plan(x, n)

    while len(x_plan) < n:
        argmax, argmin = 0, 1000
        ind_i, ind_j = -1, -1
  # Находим точку с максимальным приростом критерия эффективности
        for i in range(len(x)):
            arg = dxe(x[i], x_plan, p_plan, delta)
            if arg > argmax:
                argmax = arg
                ind_i = i

        tmp_1 = x[ind_i]
        x_plan.append(tmp_1)
        p_plan.append(1 / n)
# Проверяем определенность матрицы информации
        if np.linalg.det(inf_matrix(x_plan, p_plan, delta)) == 0:
            x_plan.pop()
            p_plan.pop()
            continue
 # Удаляем точку с наименьшим приростом, если она не равна добавленной точке
        while True:
            for j in range(len(x_plan)):
                arg = dxe(x_plan[j], x_plan, p_plan, delta)
                if arg < argmin:
                    argmin = arg
                    ind_j = j

            tmp_2 = x_plan[ind_j]
            if tmp_1 == tmp_2:
                x_plan.pop(ind_j)
                p_plan.pop()
                break
            else:
                x_plan.pop(ind_j)
                p_plan.pop()
                x_plan.append(tmp_1)
                p_plan.append(1 / n)
                break

    n_plan, pn_plan = normalization(x_plan, n)
    return n_plan, pn_plan
