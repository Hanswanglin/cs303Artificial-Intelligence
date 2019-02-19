"""
This script is used to separate the train_data.txt to 
two file, file 1 is the train data set when the program running, 
while the file 2 is the test data set without labeled tag represented
as 1 or -1.
"""


"""
extract original data
"""
train_data = []
test_data = []
result_data = []
file = 'train_data_origin.txt'
with open(file, 'r') as f:
    lines = f.readlines()
    line_number = len(lines)
    divide = int(line_number*0.8)
    # first portion to generate train data
    for l in lines[0: divide]:
        temp = l.split()
        temp0 = [t+' ' for t in temp[:-1]]
        temp0.append(temp[-1] + '\n')
        train_data.append(temp0)


    # second portion to generate test data
    for l in lines[divide: ]:
        temp = l.split()
        temp0 = [t+' ' for t in temp[:-2]]
        temp0.append(temp[-2] + '\n')
        test_data.append(temp0)

    # get the result data for test data which represent as 1, -1
    for l in lines[divide:]:
        temp = l.split()
        result_data.append(temp[-1]+'\n')


# print("train_data\n", train_data)
# print("test_data\n", test_data)

"""
put data into corresponding file respectively
"""
file_train_data = 'train_data.txt'
with open(file_train_data, 'a') as f_train:
    for t in train_data:
        f_train.writelines(t)

file_test_data = 'test_data.txt'
with open(file_test_data, 'a') as f_test:
    for t in test_data:
        f_test.writelines(t)

file_result_data = 'result_data.txt'
with open(file_result_data, 'a') as f_result:
    for t in result_data:
        f_result.writelines(t)
