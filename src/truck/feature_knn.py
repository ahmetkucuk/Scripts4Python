print(__doc__)

import numpy as np

from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier


#ds = dataset.fake_multilabel()
#ds = fake



train_file_name = "/Users/ahmetkucuk/Documents/Developer/python/truck/data/nov_16_features/extracted_features.txt"
result_file_name = "/Users/ahmetkucuk/Documents/Developer/python/truck/data/nov_16_features/4nn_matches.txt"

data = []
labels = []
labels_str = []
with open(train_file_name, "r") as input_file:
    index = 0
    for line in input_file.readlines():
        separated = line.replace("\n", "").split("\t")
        data.append(separated[1:len(separated)])
        labels.append(index)
        index += 1
        labels_str.append(separated[0])
data = np.asarray(data)
labels = np.asarray(labels)
classifier = KNeighborsClassifier(n_neighbors=4)
classifier.fit(data, labels)

out_file = open(result_file_name, "w")

for i in range(len(data)):
    dist, indices = classifier.kneighbors(data[i])
    for k in indices[0]:
        if k != i:
            out_file.write(labels_str[i] + "\t" + labels_str[k] + "\n")

out_file.close()


