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

classes = ["OII", "OIII", "AII", "AIII", "OAII", "OAIII", "GBM", "GBMII"]


def extract_patches(img_file, patient_id, output_class_dir, n_of_image_per_file, patch_size):
	print("Before Read " + img_file)
	image = Image.open(img_file)
	image = numpy.array(image)

	print(image.shape)
	for i in range(n_of_image_per_file):
		random_x = random.randrange(image.shape[0] - (patch_size + 100)) + 50
		random_y = random.randrange(image.shape[1] - (patch_size + 100)) + 50

		image_out_file = output_class_dir + patient_id + "_" + str(i) + ".jpg"
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

	n_samples = len(l_patients)

	selected_indexes = [True for i in xrange(n_samples)]
	for i in range(n_samples):
		index = random.randint(0, n_samples - 1)
		list_of_train.append(l_patients[index])
		selected_indexes[index] = False

	for i in range(n_samples):
		if selected_indexes[i]:
			list_of_validation.append(l_patients[i])
	return list_of_train, list_of_validation


'''
	Sample run command:
	python extractor.py /home/ahmet/workspace/medical-image-extractor/ data/patches-256-5000-val/ data/s2_converted/ 625 256

'''


def main(args):
	if len(args) < 5:
		print("CommandLine Args: root_dir, output_dir, input_dir, n_of_image_per_file, patch_size")

	root_dir = args[0]
	output_dir = root_dir + args[1]
	input_dir = root_dir + args[2]
	n_of_image_per_file = int(args[3])
	patch_size = int(args[4])
	random.seed(0)
	with open("metadata.txt", "w") as f_metadata:
		for c in classes:
			if not (os.path.isdir(output_dir + "train/" + c)):
				os.makedirs(output_dir + "train/" + c)
				os.makedirs(output_dir + "test/" + c)

			test = []
			train = []
			files = find_files(class_name=c, input_dir=input_dir)
			files = random.shuffle(files)
			files = files[:3]

			while len(test) == 0:
				train, test = bootstrap632(files)
			f_metadata.write("Class: " + c + "\n")
			selected_train = map(lambda i: i[0], train)
			selected_test = map(lambda i: i[0], test)
			f_metadata.write("Selected Files For Train: " + str(selected_train) + "\n")
			f_metadata.write("Selected Files For Test: " + str(selected_test) + "\n")
			for i in range(len(train)):
				extract_patches(train[i][1], train[i][0], output_dir + "train/" + c + "/", n_of_image_per_file,
								patch_size)
			for i in range(len(test)):
				extract_patches(test[i][1], test[i][0], output_dir + "test/" + c + "/", n_of_image_per_file, patch_size)


if __name__ == '__main__':
	main(sys.argv[1:])
