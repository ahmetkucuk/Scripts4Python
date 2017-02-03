import random


def bootstrap632(l_patients):
	list_of_train = []
	list_of_validation = []
	#train_set = set()

	n_samples = len(l_patients)
	selected_index = [False for i in range(n_samples)]
	for i in range(n_samples):
		index = random.randint(0, n_samples - 1)
		list_of_train.append(l_patients[index])
		selected_index[index] = True
		#train_set.add(l_patients[index])

	for i in range(n_samples):
		if not selected_index[i]:
			list_of_validation.append(l_patients[i])
	return list_of_train, list_of_validation


def oversample(files):
	random.shuffle(files)
	n_files = len(files)
	while len(files) < 43:
		index = random.randint(0, n_files - 1)
		files.append(files[index])
	random.shuffle(files)
	return files

files = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]
files = oversample(files)


test = []
train = []
while len(test) == 0:
	train, test = bootstrap632(files)

print("train: " + str(len(train)))
print("test: " + str(len(test)))

print(train)
print(test)
