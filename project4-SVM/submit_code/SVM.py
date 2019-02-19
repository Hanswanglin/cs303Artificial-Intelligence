"""
According to the equation 2/|w|
If you want to maximize the margin of two hyperplanes,
you need to minimize the norm of omega.
However, it also need to meet the constraint y_i⋅(w⋅xi+b)≥1 for any i=1,2,3⋅⋅⋅n
"""

import numpy as np
import argparse
from utils.gd import GD

def arg_parse():
    """
    parser the command line arguement
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('traindata', help='train data', type=str)  # positional argument
    parser.add_argument('testdata', help='test data', type=str)
    parser.add_argument('-t', help='time budget', type=int, required=True)
    namespace = parser.parse_args()  # Namespace
    return namespace

def load_train_data(file_path):
    """
    load data set and parser,because it store in memo, only for small data set
    Matrix calculation
    """
    with open(file_path, 'r') as fr:
        lines = fr.readlines()
        row = len(lines)
        column = len(lines[0].split()) - 1  # 10
        data_mat = np.zeros((row, column), dtype=np.float)
        label_mat = np.zeros(row, dtype=np.float)
        for line, i in zip(lines, range(row)):
            line_arr = [float(l) for l in line.split()]
            data_mat[i] = line_arr[:-1]
            label_mat[i] = line_arr[-1]
    return data_mat, label_mat

def load_test_data(file_path):
    with open(file_path, 'r') as fr:
        lines = fr.readlines()
        row = len(lines)
        column = len(lines[0].split())
        test_data = np.zeros((row, column), dtype=np.float)
        for line, i in zip(lines, range(row)):
            line_arr = [float(l) for l in line.split()]
            test_data[i] = line_arr
    return test_data

def get_gd_result(data_mat, label_mat, test_data):
    gd = GD(x=data_mat, y=label_mat, file_size=len(data_mat))
    gd.train()
    predict_result = gd.predict(test_data)
    return predict_result

def output(result):
    for i in result:
        print(int(i))

def main():
    namespace = arg_parse()
    # get train data to train model
    train_data_file = namespace.traindata
    data_mat, label_mat = load_train_data(train_data_file)

    # get test data to predict result
    test_data_file = namespace.testdata
    test_data = load_test_data(test_data_file)

    # get gradient descend result
    predict_result = get_gd_result(data_mat, label_mat, test_data)

    # get print info
    output(predict_result)


if __name__ == "__main__":
    # start = time.time()
    main()
    # end = time.time()
    # print("Time use:%s" % (end - start))
