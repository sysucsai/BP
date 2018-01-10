import random
import numpy as np
import bp_mnist_loader


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
        random.shuffle(training_data)
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
        return np.argmax(self.feedforward(training_inputs))

    def update_values(self, new_train_data):
        #更新权重及阈值函数
        nabla_t = [np.zeros(t.shape) for t in self.thresholds]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in new_train_data:
            delta_nabla_t, delta_nabla_w = self.backprop(x, y)
            nabla_t = [nb + dnb for nb, dnb in zip(nabla_t, delta_nabla_t)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w - (self.eta / len(new_train_data)) * nw for w, nw in zip(self.weights, nabla_w)]
        self.thresholds = [t - (self.eta / len(new_train_data)) * nt for t, nt in zip(self.thresholds, nabla_t)]

    def backprop(self, x, y):
        #根据输入输出返回与预期的差
        nabla_t = [np.zeros(t.shape) for t in self.thresholds]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        activation = x
        activations = [x]
        outputs = []
        for t, w in zip(self.thresholds, self.weights):
            output = np.dot(w, activation) + t
            outputs.append(output)
            activation = sigmoid(output)
            activations.append(activation)

        delta = self.cost_derivative(activations[-1], y) * \
                sigmoid_prime(outputs[-1])
        nabla_t[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())

        for l in range(2, self.num_of_layers):
            output = outputs[-l]
            sp = sigmoid_prime(output)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_t[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
        return (nabla_t, nabla_w)

    def cost_derivative(self, output_activations, y):
        return (output_activations - y)

    def feedforward(self, a):
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
