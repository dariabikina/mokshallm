#clusterizing the texts into texts in Moksha and texts in Russian based on strings that are more common in MOksha 

import os
from shutil import copyfile
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from charset_normalizer import detect

source = '/Users/dariabikina/Documents/python learning/moksha llm/processed'

cluster_0_directory = os.path.join(source, "russian")
cluster_1_directory = os.path.join(source, "moksha")

os.makedirs(cluster_0_directory, exist_ok=True)
os.makedirs(cluster_1_directory, exist_ok=True)


moksha_keywords = ["яй", "фт", "лг", "хн", "нт", "кя", "ря", "фн", "нды",
                   "нц", "нди", "нз", "нкс", "мг", "ткс", "мф", "ьсь", "кшн", "хт", "зг", "рх", "лх"]

def detect_moksha(text):
    detected_keywords = [keyword for keyword in moksha_keywords if keyword in text]
    return detected_keywords

# summary dictionaries
summary = defaultdict(list)
keyword_counts = []  # store keyword counts per text
files = []  # store filenames for clustering results


for root, _, filenames in os.walk(source):
    for filename in filenames:
        if filename.endswith('.txt'):
            file_path = os.path.join(root, filename)

          
            try:
                with open(file_path, 'rb') as file:
                    raw_data = file.read()
                    result = detect(raw_data)
                    encoding = result['encoding']

                with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                    text = file.read()
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                continue

            detected_keywords = detect_moksha(text)
            k_count = len(detected_keywords)
            keyword_counts.append(k_count)
            files.append(file_path)


#K-Means clustering based on the number of detected keywords
k_count_array = np.array(keyword_counts).reshape(-1,1)

n_clusters = 2 #the distribution is binomial

if len(keyword_counts) > 0:
    k_count_array = np.array(keyword_counts).reshape(-1, 1)
    n = 2  # The distribution is binomial
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(k_count_array)
    cluster_labels = kmeans.labels_

#Viz the clusters
plt.scatter(keyword_counts, cluster_labels, c=cluster_labels, cmap='viridis', edgecolor='k')
plt.title("Clustering of Texts Based on Keyword Counts")
plt.xlabel("Number of Keywords Detected")
plt.ylabel("Cluster Label")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


print("\nCluster Summary:")
for cluster in range(n_clusters):
    cluster_files = [files[idx] for idx, label in enumerate(cluster_labels) if label == cluster]
    print(f"Cluster {cluster}: {len(cluster_files)} files")
    print(f"Files: {', '.join(cluster_files)}")

#saving files
for idx, file_path in enumerate(files):
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Skipping...")
        continue

    cluster = cluster_labels[idx]
    if cluster == 0:
        destination = os.path.join(cluster_0_directory, os.path.basename(file_path))
    else:
        destination = os.path.join(cluster_1_directory, os.path.basename(file_path))
    
    # Copy file to the appropriate cluster directory
    copyfile(file_path, destination)
    print(f"Saved {file_path} to Cluster {cluster} directory: {destination}")

print("\nClustering and file saving complete.")
    
