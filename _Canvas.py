from Canvas import Canvas
from Parser import Parser
from threading import Thread
import matplotlib.pyplot as plt

def _shareData():
    test_odt = "data/firstData/voltage-spin-diode.odt"
    odt_data = Parser.getOdtData(test_odt)
    print("DETECTED COLUMNS:")
    print(odt_data[0].columns)
    picked_column = 'MR::magnetoresistance'
    print(odt_data[1])
    #create data dict that is then passed to canvas
    #this is the exemplary dict, the order must be preserved
    data_dict = {
                'i': 0,
                'iterations': odt_data[1],
                'graph_data': odt_data[0][picked_column].tolist(),
                'title' : picked_column
                }
    new_canvas = Canvas()
    new_canvas.shareData(**data_dict)
    new_canvas.createPlotCanvas()

    return new_canvas


def _runCanvas(canvas):
    print("DONE CREATING CANVAS... PREPARING THE RUN...")
    canvas.runCanvas()


def _iterateCanvas(canvas):
    iterations = canvas.iterations
    while(iterations):
        canvas.replot()
        canvas.increaseIterator()
        iterations -= 1

if __name__ == "__main__":
    canvas = _shareData()
    _runCanvas(canvas)
    _iterateCanvas(canvas)
