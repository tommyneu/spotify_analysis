import pandas as pd
import matplotlib.pyplot as plt

data = pd.DataFrame.empty

def load_data(json_data):
    global data
    data = pd.read_json(json_data)

def plot_data(attr_1, attr_2, attr_3=None):
    global data

    if attr_3 is not None:
        ts = data.plot.scatter(x=attr_1, y=attr_2, c=attr_3, colormap='viridis')
    else:
        ts = data.plot.scatter(x=attr_1, y=attr_2, c='DarkBlue')

    ts.plot()
    plt.show()

def print_data():
    global data
    print(data.head(5))