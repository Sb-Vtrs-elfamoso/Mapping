import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

# Loading dataset
df = pd.read_csv(r'./Data/data.csv')
pd.options.display.max_rows = 100
NB_SAMPLES = 20

# Error corecction
x = df['x']
df['x'] = df['angle']
df['angle'] = x

y = df['y']
df['y'] = df['dist']
df['dist'] = y

# Showing df info
print(df.to_string())
print(df.info())

# ploting data
# angle / distance
df.plot(x='angle', y='dist', kind='scatter',marker='.', s=.5)
# x/y
df.plot(x='x', y='y', kind='scatter',marker='.', s=.5)
plt.show()

#Nearest Neighbors graph
neigh = NearestNeighbors(n_neighbors=2)
nbrs = neigh.fit(df[['x','y']])
distances, indices = nbrs.kneighbors(df[['x','y']])
distances = np.sort(distances, axis=0)
distances = distances[:,1]
plt.plot(distances)
plt.show()
plt.clf()

# Dbscan Clustering
clustering = DBSCAN(eps=50, min_samples=3*NB_SAMPLES).fit_predict(df[['x','y']])
# angle / distance
plt.scatter(df['angle'],df['dist'],c = clustering, marker='.', s=.5)
plt.show()
plt.clf()
# x/y
plt.scatter(df['x'],df['y'],c = clustering, marker='.', s=.5)
plt.show()
print(np.unique(clustering, return_counts=True)[1])
#print(pd.crosstab(clustering, pd.cut(df['angle'], np.arange(-120,125, 5))).sum())
