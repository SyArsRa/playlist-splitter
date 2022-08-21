import SP.helper
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

def cluster(playlist):
    data = [[song.danceability,song.energy,song.speechiness,song.acousticness,song.instrumentalness,song.valence,song.liveness,song.tempo/108] for song in playlist]
    data = np.array(data)
    #Creating PCA Model which reduces dimensions to amount needed for 99% variance
    pca = PCA(n_components=0.99, svd_solver='full')
    data = pca.fit_transform(data)
    #determining number of clusters
    nclusters = len(playlist)//50 if len(playlist) > 100 else len(playlist) // 25
    #Creating KMeans Model
    kmean = KMeans(n_clusters=nclusters,init = "k-means++",n_init=30, random_state=0)
    labels = kmean.fit_predict(data)
    #3D Cluster Graphs
    """
    u_labels = np.unique(labels)
    centroids = kmean.cluster_centers_
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in u_labels:
        ax.scatter(data[labels == i , 1] , data[labels == i , 2],data[labels == i , 0] , label = i)
    ax.scatter(centroids[:,1] , centroids[:,2],centroids[:,0] , s = 80, color = 'black')
    plt.legend()
    plt.show()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in u_labels:
        ax.scatter(data[labels == i , 1] , data[labels == i , 3],data[labels == i , 0] , label = i)
    ax.scatter(centroids[:,1] , centroids[:,3],centroids[:,0] , s = 80, color = 'black')
    plt.legend()
    plt.show()
    """
    return labels
