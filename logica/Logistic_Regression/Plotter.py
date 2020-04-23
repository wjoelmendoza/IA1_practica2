from .Model import Model
import matplotlib.pyplot as chart
import os

def show_picture(pixels):
    chart.imshow(pixels)
    chart.show()


def show_Model(models):
    print("----------------MODELOS EN PLOTTER")
    print(len(models))
    chart.clf()
    for model in models:
        chart.plot(model.bitacora, label=str(model.alpha))
    chart.ylabel('Costo')
    chart.xlabel('Iteraciones')
    legend = chart.legend(loc='upper center', shadow=True)
    return chart
    
    #chart.show()
