import RPi.GPIO as GPIO
from matplotlib import pyplot as plt
import time


leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

def adc(): # измеряет напряжение на выходе тройки-модуля
    n = 0
    s = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        s[i] = 1
        GPIO.output(dac, s)
        time.sleep(0.01)
        compvalue = GPIO.input(comp)
        if compvalue == 1:
            s[i] = 0
        else:
            n += 2**(7-i)          
    return n

def for_leds(value): # выводит двоичное представление числа в область светодиодов
    s = [int(x) for x in bin(value)[2:].zfill(8)]
    GPIO.output(leds, s)

c = 0

try:
    troyka_value_list = [] # сюда добавляются новые измерения
    start_time = time.time()
    GPIO.output(troyka, 1)
    troyka_value = 0
    
    while troyka_value < 213 * 0.97: # зарядка конденсатора (пока выходное наряжение не достигнет 97% от входного)
        troyka_value = adc()
        troyka_value_list.append(troyka_value)
        for_leds(troyka_value)
        c += 1
        print(troyka_value)
    GPIO.output(troyka, 0)
    
    while troyka_value > 169: # разрядка конденсатора
        troyka_value = adc()
        troyka_value_list.append(troyka_value)
        for_leds(troyka_value)
        c += 1
        print(troyka_value)
    
    finish_time = time.time()
    full_time = finish_time - start_time
    
    plt.plot(troyka_value_list)
    plt.xlabel("Номер измерения")
    plt.ylabel("Показания АЦП")
    plt.show()

    troyka_value_list_str = [str(x) for x in troyka_value_list]
    
    with open("data.txt", "w") as f: # показания АЦП
        f.write("\n".join(troyka_value_list_str))
    
    for_settings = [str(round(1 / (full_time / c), 2)), str(round(3.3 / 256, 5))]
    with open("settings.txt", "w") as g: # средняя частота дискретизации и шаг квантования АЦП
        g.write("\n".join(for_settings))
    
    print("\n")
    print("Общая продолжительность эксперимента", round(full_time, 2), "c", "\n")
    print("Период одного измерения", round(full_time / c, 2), "c", "\n")
    print("Средняя частота дискретизации", round(c / full_time, 2), "Гц", "\n")
    print("Шаг квантования АЦП", round(3.3 / 256, 5))

finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()