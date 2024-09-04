import pandas as pd

# Code block 1
df = pd.read_csv('data.csv', index_col=False)

import plotly.express as px

fig = px.scatter(df, x='sepal.length', y='petal.length', color='variety')
fig.show()


df.to_csv('processed_data.csv', index=False)
# Code block 2
df = pd.read_csv('data.csv', index_col=False)

fig.write_image("./chart.png")


df.to_csv('processed_data.csv', index=False)
