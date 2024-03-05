# Developed by Nastya Fomina, 2024
from tkinter import *
from tkinter import ttk
from backend import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
root = Tk()
root.title("Experement planning and analisis")
# %% Функции приложения
# Запоминаем значения, возвращаемые главной функцией
def transit():
 global xplan, pplan
 xplan, pplan = Sequential(int(n_field.get()), float(d_field.get()), 
int(seed_field.get()))
 process_label.config(text= "План успешно синтезирован. Для просмотра результатов откройте владки 'Графики' и 'Таблицы'", wraplength=400)
# Вычисление и отображение характеристик плана
def plan_results(x_plan, p_plan, delta):
 det, trace = plan_parametrs(x_plan, p_plan, delta)
 det_label.config(text="|M| = " + str(det))
 trace_label.config(text="tr(D) = " + str(trace))
# Заполнение таблицы плана
def table_results(x_plan, p_plan):
 for i in range(len(x_plan)):
  table.insert("", "end", values=(i, x_plan[i], p_plan[i]))
# График спектра плана
def plotter(x_plan):
 figure = Figure(figsize=(5, 4), dpi=100)
 plot = figure.add_subplot(1, 1, 1)
 for i in range(len(x_plan)):
  plot.scatter(x_plan[i][0], x_plan[i][1])
 canvas = FigureCanvasTkAgg(figure, tab2)
 canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)
 plan_button.config(state="disabled")
 dxe_button.config(state="active")
# График d(x, ε)
def dxe_plotter():
 grid, dots = dxe_plot(xplan, pplan, float(d_field.get()))
 figure = Figure(figsize=(5, 4), dpi=100)
 plot = figure.add_subplot(1, 1, 1)
 plot.plot(xplan, dots)
 canvas = FigureCanvasTkAgg(figure, tab2)
 canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)
 plan_button.config(state="active")
 dxe_button.config(state="disabled")
# %% Инициализируем вкладки
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tabControl.add(tab1, text ='Синтез')
tabControl.add(tab2, text ='Графики')
tabControl.add(tab3, text ='Таблицы')
tabControl.add(tab4, text ='О приложении')
tabControl.pack(expand = 1, fill ="both")
# %% Меню " О приложении "
text_label = ttk.Label(tab4, wraplength=300 ,text="Приложение 'Experement planning and analisis' осуществляет синтез дискретных D-оптимальных планов эксперимента для нечётких ли-нейных двухфакторных моделей. Приложение разработал студентка группы ПМ-01 Фомина Анастасия, 2024 год.")
text_label.grid(row=0, column=0)
# %% Меню " Графики "
# Кнопки во вкладке "Графики"
plan_button = Button(tab2, text="График спектра", state="disabled", 
command=lambda: [plotter(xplan)])
plan_button.grid(row=2, column=0, padx=15, pady=10)
dxe_button = Button(tab2, text="График d(x,ε)", state="disabled", 
command=lambda: [dxe_plotter()])
dxe_button.grid(row=2, column=1, padx=15, pady=10)
# %% Меню " Cинтез "
# Выбор количества точек в плане
n_label = ttk.Label(tab1, text="Число точек в плане:")
n_label.pack()
n = [20, 30, 40]
# Значение количества точек в плане
n_field = ttk.Combobox(tab1, values=n, state="readonly")
n_field.pack()
n_field.current(0)
# Выбор дельты
d_label = ttk.Label(tab1, text="Значение дельты:")
d_label.pack()
d = [0.2, 0.3, 0.4, 0.5]
# Значение дельты
d_field = ttk.Combobox(tab1, values=d, state="readonly")
d_field.pack()
d_field.current(0)
# Выбор семени случайного значения
seed_label = ttk.Label(tab1, text="Семечко для ГСЧ")
seed_label.pack()
seed = [1, 2, 3, 4, 5]
# Значение семени ГСЧ
seed_field = ttk.Combobox(tab1, values=seed, state="readonly")
seed_field.pack()
seed_field.current(0)
# Кнопка выполнения главной функции
enter = Button(tab1, text="Синтезировать план",
 command=lambda: [transit(), plotter(xplan), table_results(xplan,pplan), plan_results(xplan, pplan, float(d_field.get()))])
enter.pack(pady=50)
# Индикицая о завершении процесса главной функции
process_label = ttk.Label(tab1, text="Нажмите на кнопку, чтобы начать синтез плана")
process_label.pack(pady=50)
# %% Меню " Таблицы "
cols = ('N', 'Точка', 'Вес')
table = ttk.Treeview(tab3, columns=cols, show='headings', height=19)
for col in cols:
 table.column(col, anchor=CENTER, width=160, stretch=NO)
 table.heading(col, text=col)
table.grid(row=0, column=0, columnspan=2, padx=8)
# Строка с определителем
det_label = ttk.Label(tab3, text="|M| = ")
det_label.grid(row=1, column=0)
# Строка со следом
trace_label = ttk.Label(tab3, text="tr(D) = ")
trace_label.grid(row=1, column=1)
# %% Main&some settings
root.call('wm', 'iconphoto', root._w, PhotoImage(file='icon2.png'))
root.geometry('500x470+760+300')
root.mainloop()
