import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tkinter import *
from tkinter.ttk import *

plt.rc('font', family='AppleGothic')

crop_name = []
crop_low_ave, crop_max_ave, crop_low, crop_max = 0.0, 0.0, 0.0, 0.0
graph_title = ""

def crop_select():
    global crop_low_ave, crop_max_ave, crop_low, crop_max, graph_title
    crop = combo.get()
    for row in crop_data:
        if row[0] == crop:
            crop_low_ave = float(row[1])
            crop_max_ave = float(row[2])
            crop_low = float(row[3])
            crop_max = float(row[4])
            graph_title = f'2003~2023 {crop}의 생육적온 빈도'
            break

def graph_plot():
    plt.figure(figsize=(8, 5))
    cmap = cm.Spectral

    counts = [frequency[mon - 1][day - 1] for mon in months for day in days]

    sc = plt.scatter([mon for mon in months for day in days],
                    [day for mon in months for day in days],
                    c=counts,
                    s=[count * 10 for count in counts],
                    cmap='jet',
                    alpha=0.6)

    cbar = plt.colorbar(sc)
    cbar.set_label('빈도')
    plt.xlabel('월')
    plt.ylabel('일')
    plt.title(graph_title)
    plt.grid(True)
    plt.savefig('deon.png')

    graph_img = PhotoImage(file='deon.png')
    graph_lbl.configure(image=graph_img)
    graph_lbl.image = graph_img

def analysis():
    global days, months, frequency
    days = list(range(1, 32))
    months = list(range(1, 13))

    frequency = [[0 for _ in range(31)] for _ in range(12)]

    for row in data:
        average_temp = float(row[2])
        if row[4] == '':
            row[4] = -999
        maximum_temp = float(row[4])
        if row[3] == '':
            row[3] = 999
        lowest_temp = float(row[3])
        if average_temp >= crop_low_ave and average_temp <= crop_max_ave:
            if maximum_temp <= crop_max and lowest_temp >= crop_low:
                mon = int(row[0].split('-')[1])
                day = int(row[0].split('-')[2])
                frequency[mon - 1][day - 1] += 1
    graph_plot()

f = open('temp-seoul.csv', encoding='utf8')
data = csv.reader(f)
next(data)
data = list(data)

f2 = open('crops.csv', encoding='utf8')
crop_data = csv.reader(f2)
next(crop_data)
crop_data = list(crop_data)
print(len(crop_data))
print(crop_data)

for row in crop_data:
    crop_name.append(row[0])

print(crop_name)
root = Tk()
root.title('생육적온 모델')
root.geometry('800x600')

Box = Frame(root)
Box.grid(row=0, column=0)
Graph = Frame(root)
Graph.grid(row=1, column=0)

combo = Combobox(Box, values=crop_name)
combo.grid(row=0, column=0)

btn = Button(Box, text='선택', width=20, command=crop_select)
btn.grid(row=0, column=1)

btn2 = Button(Box, text='그래프', width=20, command=analysis)
btn2.grid(row=0, column=2)

graph_lbl = Label(Graph)
graph_lbl.grid(row=1, column=0, columnspan=5)

root.mainloop()