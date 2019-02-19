import numpy as np

class GD(object):
    """
    expend the demension of the 
    ::parameter
      :x: a matrix contain all data represented as [[],[]]
    """
    def __init__(self, x, y, file_size, learning_rate=0.01):
        self.x = np.c_[np.ones((x.shape[0])), x]  # add one column, no need to add an extra b
        self.y = y
        self.epochs = int(file_size/6)
        self.learning_rate = learning_rate
        self.w = np.random.uniform(size=np.shape(self.x)[1],)  # initially random our w value

    # calculate the loss
    def get_loss(self, x, y):
        """
        Calculate the cost error by the w and b currently.
        "np.dot(x, w)" represent the distance from certain sample to hyperplane
        if "1 - y * np.dot(x, w)" less than 0 which means the sample point is suitable for the constraint
        if "1 - y * np.dot(x, w)" larger than 0, it means it is not a good prediction
        """
        loss = max(0, 1 - y * np.dot(x, self.w))
        return loss

    def cal_sgd(self, x, y, w):
        if (y * np.dot(x, w)) < 1:  # if the sample is inside the two hyperplane
            w = w - self.learning_rate * (-y * x)
        else:
            w = w
        return w

    def train(self):
        # iteration 
        for epoch in range(self.epochs):
            # For all data samples, scramble order
            randomize = np.arange(len(self.x))
            np.random.shuffle(randomize)
            x = self.x[randomize]
            y = self.y[randomize]
            loss = 0
            # Calculate all samples
            for xi, yi in zip(x, y):
                loss += self.get_loss(xi, yi)
                self.w = self.cal_sgd(xi, yi, self.w)
            # print("epoch: {0} loss: {1}".format(epoch, loss))


    # input the test data in the form of matrix [[],[],[]]
    def predict(self,x):
        x_test = np.c_[np.ones((x.shape[0])), x]
        return np.sign(np.dot(x_test, self.w))