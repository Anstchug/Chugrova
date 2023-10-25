import numpy as np
from matplotlib import pyplot as plt

tmp = np.loadtxt("/home/b03-301/Desktop/settings.txt", dtype = float)
data_array = np.loadtxt("/home/b03-301/Desktop/data.txt", dtype = int)

fig, ax = plt.subplots(figsize = (16, 10), dpi = 250)
volt_array = data_array * tmp[0]
x = np.linspace(0,tmp[0], data_array.size)
t = x * tmp[1]
ax.plot(t, volt_array, label = 'V(t)', c = 'b', linestyle = '-', linewidth = 1, marker = 'o')

ax.set_xlabel("Время, с")
ax.set_ylabel("Напряжение, В")

ax.set_title("Процесс зарядки и разрядки конденсатора в RC-цепи")

ax.set_xlim([0, t.max() + 0.2])
ax.set_ylim([0, volt_array.max() + 0.2])

plt.minorticks_on()
plt.grid(which = "major")
plt.grid(which = "minor", linestyle = "--")

i = 0
while data_array[i + 1] - data_array[i] >= -2:
    i += 1
    
istr = str(i * tmp[1])
istr1 = str((x.max() - i) * tmp[1])

f = ['Время зарядки = ', istr, 'c']
f1 = ['Время разрядки = ', istr1, 'c']
f_str = " ".join(f)
f_str1 = " ".join(f1)

ax.text(6, 2.2, f_str, fontsize = 8)
ax.text(6, 1.6, f_str1, fontsize = 8)

ax.legend()

fig.savefig("numpy.png")

plt.show()