from scipy import ndimage, misc
import os
import random
from PIL import Image
import numpy
import sys
import time

# image = ndimage.imread("/Users/ahmetkucuk/Documents/Developer/python/patch-extractor/resource/img/image.jpg")

# i = image[0:25, 0:25]
# misc.imsave('/Users/ahmetkucuk/Documents/Developer/python/patch-extractor/resource/img/image_cut.jpg', i)
# print(i)
#random.seed(100)

classes = ["OII", "OIII", "AII", "AIII", "OAII", "OAIII", "GBM", "GBMII"]


def extract_patches(img_file, patient_id, output_class_dir, n_of_image_per_file, patch_size, index):
	image = Image.open(img_file)
	image = numpy.array(image)

	for i in range(n_of_image_per_file):
		random_x = random.randrange(image.shape[0] - (patch_size + 100)) + 50
		random_y = random.randrange(image.shape[1] - (patch_size + 100)) + 50

		image_out_file = output_class_dir + patient_id + "_" + index + "_" + str(i) + ".jpg"
		region = image[random_x:random_x + patch_size, random_y:random_y + patch_size]
		misc.imsave(image_out_file, region)


def find_files(class_name, input_dir):
	print(input_dir + class_name)
	for root, dirs, files in os.walk(input_dir + class_name):

		patients = []

		for f in files:
			if f.endswith("-0.tif"):  # & ("_" in str(f))
				full_path = input_dir + class_name + "/" + f
				patients.append((f[:-4], full_path))
		random.shuffle(patients)

		return patients


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


def oversample(files, size):
	random.shuffle(files)
	n_files = len(files)
	while len(files) < size:
		index = random.randint(0, n_files - 1)
		files.append(files[index])
	random.shuffle(files)
	return files

'''
	Sample run command:

	python extractor.py /home/ahmet/workspace/medical-image-extractor/ data/patches-256-5000-val/ data/s2_converted/ 625 256
n extractor.py /home/ahmet/workspace/medical-image-extractor/ data/undersampled-bootstrap-32-1000/ data/tif_merged_converted/scan_merged_converted/ 1000 32
'''


def main(args):
	if len(args) < 5:
		print("CommandLine Args: root_dir, output_dir, input_dir, n_of_image_per_file, patch_size")
		exit(0)

	root_dir = args[0]
	output_dir = root_dir + args[1]
	input_dir = root_dir + args[2]
	n_of_image_per_file = int(args[3])
	patch_size = int(args[4])
	random.seed(0)
	os.makedirs(output_dir)

	samples = {}

	with open(output_dir + "metadata.txt", "w") as f_metadata:

		max_n_train = 0
		max_n_test = 0
		for c in classes:
			if not (os.path.isdir(output_dir + "train/" + c)):
				os.makedirs(output_dir + "train/" + c)
				os.makedirs(output_dir + "test/" + c)

			test = []
			train = []
			files = find_files(class_name=c, input_dir=input_dir)
			#files = oversample(files)

			while len(test) == 0:
				train, test = bootstrap632(files)
			samples[c] = (train, test)
			max_n_train = max(len(train), max_n_train)
			max_n_test = max(len(test), max_n_test)

		train = []
		test = []
		for c in samples:
			train, test = samples[c]
			n_of_image_per_train_file = 5000 / len(train)
			n_of_image_per_test_file = 3000 / len(test)

			f_metadata.write("Class: " + c + "\n")
			selected_train = map(lambda i: i[0], train)
			selected_test = map(lambda i: i[0], test)

			print("Selected Files For Train (" + str(len(train)) + "): " + str(selected_train) + "\n")
			print("Selected Files For Test (" + str(len(test)) + "): " + str(selected_test) + "\n")

			f_metadata.write("Selected Files For Train (" + str(len(train)) + "): " + str(selected_train) + "\n")
			f_metadata.write("Selected Files For Test (" + str(len(test)) + "): " + str(selected_test) + "\n")

			for i in range(len(train)):
				extract_patches(train[i][1], train[i][0], output_dir + "train/" + c + "/", n_of_image_per_train_file,
								patch_size, "train" + str(i))

			for i in range(len(test)):
				extract_patches(test[i][1], test[i][0], output_dir + "test/" + c + "/", n_of_image_per_test_file, patch_size, "test" + str(i))


if __name__ == '__main__':
	main(sys.argv[1:])
