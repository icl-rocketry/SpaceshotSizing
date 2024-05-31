import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

throatdiameters = np.arange(0.7, 1.21, 0.1)
for i, throatdiameter in enumerate(throatdiameters):
    data = pd.read_csv(f"aero2m8inthroat/flightthroat{str(int(round(throatdiameter*10))).zfill(2)}.csv", header=0)
    plt.plot(data['Time (sec)'], data['Altitude (ft)'] / 3.28084, label=f"Throat Diameter: {throatdiameter} in")
plt.legend()
plt.show()