import os


class File_Func:
    def check_file_exists(self, filename):
        if os.path.isfile(filename):
            return True
        else:
            return False

    def read_file(self, filename):
        with open(filename, 'r') as dataset:
            # print(dataset)
            # for line in dataset:
            #     print(line)
            return dataset
