import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Theme
sns.set_theme(
    context="notebook", 
    # https://seaborn.pydata.org/generated/seaborn.axes_style.html#seaborn.axes_style    
    style="ticks",
    palette="rocket_r", 
    font="sans-serif", 
    font_scale=1, 
    color_codes=True, 
    rc=None
)

# A. Single Style

# Style 1: Histogram Graph
df = pd.DataFrame(np.random.rand(1, 500).transpose(), columns=['x'])
chart = sns.histplot(data=df, x="x", bins=50, kde=True)
chart.set(title='Histogram', xlabel='its x_label', ylabel='its y_label')
plt.show()

# Style 2: Line Graph
df = pd.DataFrame(np.random.rand(1, 500).transpose(), columns=['x', 'y'])
chart = sns.histplot(data=df, x="x", bins=50, kde=True)
chart.set(title='Line Graph', xlabel='its x_label', ylabel='its y_label')
plt.show()

# Style 3: Joint Graph 
rs = np.random.RandomState(11)
x = rs.gamma(2, size=1000)
y = -.5 * x + rs.normal(size=1000)
sns.jointplot(x=x, y=y, kind="hex", color="#4CB391")
plt.show()

# Stype 4: Boxplot


# B. MULTIPLE PLOT GRIDS


# C. MULTIPLE PLOT


# D. COLOR SELECTION


# E. SAVE
