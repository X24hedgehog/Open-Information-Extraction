from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from tqdm import tqdm
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

# Our sentences we like to encode
sentences = []

with open("extract_predicate.txt", "r") as file:
    for line in file:
        sentence = line
        sentences.append(sentence)

# Sentences are encoded by calling model.encode()
sentence_embeddings = model.encode(sentences)


def clustering(model_type, num_cluster):
    assert model_type in ['k-means', 'agglomerative', 'fast']
    if model_type == 'k-means':
        kmeans_clustering(num_cluster)
    elif model_type == 'agglomerative':
        agglomerative_clustering()
    else:
        fast_clustering()


def kmeans_clustering(n):
    # Perform k-mean clustering
    clustering_model = KMeans(n_clusters=n)
    clustering_model.fit(sentence_embeddings)
    cluster_assignment = clustering_model.labels_

    print(cluster_assignment)
    print(len(cluster_assignment))

    clustered_sentences = [[] for i in range(n)]
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_sentences[cluster_id].append(sentence_embeddings[sentence_id])

    for i, cluster in enumerate(clustered_sentences):
        print("Cluster ", i+1)
        print(cluster)
        print("")


def agglomerative_clustering():
    # Normalize the embeddings to unit length
    sentence_embeddings_normed = sentence_embeddings / np.linalg.norm(sentence_embeddings, axis=1, keepdims=True)

    # Perform k-mean clustering
    clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=1.5)  # , affinity='cosine', linkage='average', distance_threshold=0.4)
    clustering_model.fit(sentence_embeddings_normed)
    cluster_assignment = clustering_model.labels_

    clustered_sentences = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clustered_sentences:
            clustered_sentences[cluster_id] = []

        clustered_sentences[cluster_id].append(sentences[sentence_id])

    for i, cluster in clustered_sentences.items():
        print("Cluster ", i + 1)
        print(cluster)
        print("")


def fast_clustering():
    clusters = util.community_detection(sentence_embeddings, min_community_size=25, threshold=0.75)
    # Print for all clusters the top 3 and bottom 3 elements
    for i, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(i + 1, len(cluster)))
        for sentence_id in cluster[0:3]:
            print("\t", sentences[sentence_id])
        print("\t", "...")
        for sentence_id in cluster[-3:]:
            print("\t", sentences[sentence_id])


def find_k():
    wcss = []
    for i in tqdm(range(50)):
        kmeans = KMeans(n_clusters=10*i+10, init='k-means++', random_state=42)
        kmeans.fit(sentence_embeddings)
        wcss.append(kmeans.inertia_)
    x_axis = np.arange(10, 501, 10)
    plt.plot(x_axis, wcss)
    plt.show()

# Note: Elbow point around 100 clusters.
# clustering('k-means', 20)


def silhouette():
    range_n_clusters = [20*i for i in range(1, 21)]

    for n_clusters in range_n_clusters:
        print(n_clusters)
        # Create a subplot with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax1.set_xlim([-0.1, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(sentence_embeddings) + (n_clusters + 1) * 10])

        # Initialize the cluster with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        clusterer = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
        clusterer.fit(sentence_embeddings)
        cluster_labels = clusterer.labels_

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(sentence_embeddings, cluster_labels)
        print(
            "For n_clusters =",
            n_clusters,
            "The average silhouette_score is :",
            silhouette_avg,
        )

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(sentence_embeddings, cluster_labels)

        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7,
            )

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        # 2nd Plot showing the actual clusters formed
        colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
        ax2.scatter(
            sentence_embeddings[:, 0], sentence_embeddings[:, 1], marker=".", s=30, lw=0, alpha=0.7, c=colors, edgecolor="k"
        )

        # Labeling the clusters
        centers = clusterer.cluster_centers_
        # Draw white circles at cluster centers
        ax2.scatter(
            centers[:, 0],
            centers[:, 1],
            marker="o",
            c="white",
            alpha=1,
            s=200,
            edgecolor="k",
        )

        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker="$%d$" % i, alpha=1, s=50, edgecolor="k")

        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("Feature space for the 1st feature")
        ax2.set_ylabel("Feature space for the 2nd feature")

        plt.suptitle(
            "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
            % n_clusters,
            fontsize=14,
            fontweight="bold",
        )

    plt.show()


# if __name__ == '__main__':
#     print("It's main!")
#     # find_k()
#     silhouette()
#     print(1)


# For n_clusters = 20 The average silhouette_score is : 0.11113619
# 40
# For n_clusters = 40 The average silhouette_score is : 0.1478991
# 60
# For n_clusters = 60 The average silhouette_score is : 0.18223952
# 80
# For n_clusters = 80 The average silhouette_score is : 0.21297908
# 100
# For n_clusters = 100 The average silhouette_score is : 0.23734835
# 120
# For n_clusters = 120 The average silhouette_score is : 0.2596902
# 140
# For n_clusters = 140 The average silhouette_score is : 0.27751443
# 160
# For n_clusters = 160 The average silhouette_score is : 0.30069086
# 180
# For n_clusters = 180 The average silhouette_score is : 0.3035969
# 200
# For n_clusters = 200 The average silhouette_score is : 0.33137906
# 220
# For n_clusters = 220 The average silhouette_score is : 0.33960155
# 240
# For n_clusters = 240 The average silhouette_score is : 0.36129484
# 260
# For n_clusters = 260 The average silhouette_score is : 0.37492612
# 280
# For n_clusters = 280 The average silhouette_score is : 0.38613054
# 300
# For n_clusters = 300 The average silhouette_score is : 0.40326053
# 320
# For n_clusters = 320 The average silhouette_score is : 0.4066935
# 340
# For n_clusters = 340 The average silhouette_score is : 0.42694968
# 360
# For n_clusters = 360 The average silhouette_score is : 0.43850458
# 380
# For n_clusters = 380 The average silhouette_score is : 0.4493733
# 400
# For n_clusters = 400 The average silhouette_score is : 0.46217233

# Save fitted model for later analyze:
cache = []
for i in tqdm(range(1, 51)):
    kmeans = KMeans(n_clusters=20*i, init='k-means++', random_state=42)
    kmeans.fit(sentence_embeddings)
    cache.append(kmeans)

filename = 'k-means_models.sav'
with open(filename, "wb") as f:
    pickle.dump(cache, f)




