input_file = "/Users/ahmetkucuk/Documents/Developer/python/Scripts4Vision/resources/medical/merged_converted_tifs.txt"
input_file2 = "/Users/ahmetkucuk/Documents/Developer/python/Scripts4Vision/resources/medical/merged_tifs.txt"

def count_files(input_file):

    data_map = {"AII": [], "AIII": [], "OAII": [], "OAIII": [], "OII": [], "OIII": [], "GBM": [], "GBMII": []}
    with open(input_file, "r") as f:
        for l in f:
            tuple3 = l.strip().split("/")
            #if("-" in tuple3[2]):
            data_map.get(tuple3[1]).append(tuple3[2])

    for l in data_map:
        #print(l + " " + str(len(data_map.get(l))))
        print(l + "\t" + str(data_map.get(l)))

count_files(input_file)
print()
count_files(input_file2)