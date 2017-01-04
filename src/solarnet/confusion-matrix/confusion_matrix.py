import numpy as np
from PIL import Image
import itertools
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

confusion_matrix = []
event_indexes = {"AR": 0, "CH": 1, "SG": 2, "FL": 3, "QS": 4}

confusion_matrix = np.zeros((5, 5))

def plot_confusion_matrix(cm, classes,
						  normalize=False,
						  title='Confusion matrix',
						  cmap=plt.cm.Blues):
	"""
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
	fig1 = plt.gcf()
	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	print(cm)

	thresh = cm.max() / 2.
	for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, cm[i, j],
				 horizontalalignment="center",
				 color="white" if cm[i, j] > thresh else "black")

	#plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.draw()
	fig1.savefig('confusion.eps', dpi=120)


with open("Confusion_Matrix_Input_For_AlexNet.txt", "r") as f:
	for line in f:
		pair = line.strip().split("\t")
		actual_index = event_indexes.get(pair[0])
		predicted_index = event_indexes.get(pair[1])
		print(actual_index)
		print(predicted_index)
		confusion_matrix[actual_index][predicted_index] += 1
		confusion_matrix[predicted_index][actual_index] += 1

plot_confusion_matrix(confusion_matrix, ["AR", "CH", "SG", "FL", "QS"], normalize=False)
for i in range(5):
	for k in range(5):
		print str(confusion_matrix[i][k]), ',',
	print