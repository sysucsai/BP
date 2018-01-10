import bp_mnist_loader
import numpy as np


class Network(object):
    def __init__(self, sizes=[784, 30, 10]):
        # 神经网络层数
        self.num_of_layers = 3
        # 神经网络每层的神经元数量
        self.sizes = sizes
        # 阈值相反数与权重，则输出Output = wjxj之和 + thrsholds
        self.thresholds = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        # 每次训练数据重复次数
        self.epochs = 10
        # 学习速率
        self.eta = 3.0

    def begin_train(self):
        # 导入mnist训练集，这里只读取trainging_data
        init_training_data, useless_data_1, useless_data_2 = bp_mnist_loader.load_data_wrapper()
        training_data = list(init_training_data)
        # 初始化训练
        n = len(training_data)
        new_train_datas = [training_data[k:k + 1] for k in range(0, n, 1)]
        for new_train_data in new_train_datas:
            # 每个训练数据训练一次，更新权重及阈值
            #print(new_train_data)
            self.update_values(new_train_data)
        #print("Intializing complete")

    def start_single_training(self, training_map, training_number):
        #对传入的数据训练十次，加强交互训练的强度
        for j in range(self.epochs):
            training_inputs = [np.reshape(training_map, (784, 1))]
            training_results = [vectorized_result(training_number)]
            training_data = zip(training_inputs, training_results)
            self.update_values(list(training_data))

    def start_single_test(self, test_data):
        #对传入的测试数据进行测试，返回识别值
        training_inputs = np.reshape(test_data, (784, 1))
        return np.argmax(self.value_to_next(training_inputs))

    def update_values(self, new_train_data):
        #更新权重及阈值函数
        temp_t = [np.zeros(t.shape) for t in self.thresholds]
        temp_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in new_train_data:
            changes_temp_t, changes_temp_w = self.value_to_back(x, y)
            temp_t = [nb + dnb for nb, dnb in zip(temp_t, changes_temp_t)]
            temp_w = [nw + dnw for nw, dnw in zip(temp_w, changes_temp_w)]
        self.weights = [w - (self.eta / len(new_train_data)) * nw for w, nw in zip(self.weights, temp_w)]
        self.thresholds = [t - (self.eta / len(new_train_data)) * nt for t, nt in zip(self.thresholds, temp_t)]

    def value_to_back(self, x, y):
        #根据输入输出返回与预期的差
        temp_t = [np.zeros(t.shape) for t in self.thresholds]
        temp_w = [np.zeros(w.shape) for w in self.weights]

        func_result = x
        func_results = [x]
        outputs = []
        for t, w in zip(self.thresholds, self.weights):
            output = np.dot(w, func_result) + t
            outputs.append(output)
            func_result = sigmoid(output)
            func_results.append(func_result)

        changes = self.dx(func_results[-1], y) * \
                sigmoid_prime(outputs[-1])
        temp_t[-1] = changes
        temp_w[-1] = np.dot(changes, func_results[-2].transpose())

        for l in range(2, self.num_of_layers):
            output = outputs[-l]
            sp = sigmoid_prime(output)
            changes = np.dot(self.weights[-l + 1].transpose(), changes) * sp
            temp_t[-l] = changes
            temp_w[-l] = np.dot(changes, func_results[-l - 1].transpose())
        return (temp_t, temp_w)

    def dx(self, output_func_results, y):
        return (output_func_results - y)

    def value_to_next(self, a):
        #由输入得出输出的过程
        for t, w in zip(self.thresholds, self.weights):
            a = sigmoid(np.dot(w, a) + t)
        return a

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))

def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

if __name__ == "__main__":
    net = Network([784, 30, 10])
    net.begin_train()
