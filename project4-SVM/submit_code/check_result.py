import SVM
import time
import matplotlib.pylab as plt

def load_real_result(file_path):
    """
    get the correct result for test data
    :param file_path: the path of test data file
    :return:
        total amount of test data;
        real_result represent as list
    """
    real_result = []
    with open(file_path, 'r') as rr:
        lines = rr.readlines()
        total = len(lines)
        for i in lines:
            real_result.append(float(i))

    return total, real_result

def cal_accuracy(total, real_result, predict_result):
    right = 0
    if len(real_result) == len(predict_result):
        for r in range(len(predict_result)):
            if real_result[r] == predict_result[r]:
                right += 1
    else:
        print("the two result are not the same length")
        exit(0)

    accuracy = float(right/total) * 100
    return str(accuracy) + " %"


if __name__ == '__main__':
    start = time.time()

    predict_result, loss_value, epochs = SVM.main()
    print("predict_result\n", predict_result)
    file_path = 'test_data/result_data.txt'
    total, real_result = load_real_result(file_path)
    accuracy = cal_accuracy(total, real_result, predict_result)
    print("accuracy:", accuracy)
    print("epochs", epochs)
    # x=[]
    # for i in range(epochs):
    #     x.append(i+1)
    # print(x)
    # print(loss_value)
    # plt.plot(x, loss_value)
    # plt.grid(True)
    # plt.legend()
    # plt.ylabel('loss value')
    # plt.title("Loss value changes with the number of iterations")
    # plt.show()

    end = time.time()
    print("Time use:%s" % (end - start))