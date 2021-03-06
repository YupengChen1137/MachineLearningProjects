# -*- coding: utf-8 -*-
"""neural_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Mu7sdhpUWs0ImwzQvIbPdb6U_A-bvm_s

Author Name: Yupeng Chen
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.utils.data import TensorDataset, DataLoader
from PIL import Image

# To add your own Drive Run this cell.
from google.colab import drive
drive.mount('/content/drive')

######################################################################
# OneLayerNetwork
######################################################################

class OneLayerNetwork(torch.nn.Module):
    def __init__(self):
        super(OneLayerNetwork, self).__init__()

        ### ========== TODO : START ========== ###
        ### part d: implement OneLayerNetwork with torch.nn.Linear
        self.linear = torch.nn.Linear(784, 3)
        ### ========== TODO : END ========== ###

    def forward(self, x):
        # x.shape = (n_batch, n_features)

        ### ========== TODO : START ========== ###
        ### part d: implement the foward function
        outputs = self.linear(x)
        ### ========== TODO : END ========== ###
        return outputs

######################################################################
# TwoLayerNetwork
######################################################################

class TwoLayerNetwork(torch.nn.Module):
    def __init__(self):
        super(TwoLayerNetwork, self).__init__()
        ### ========== TODO : START ========== ###
        ### part g: implement TwoLayerNetwork with torch.nn.Linear
        self.layer1 = torch.nn.Linear(784, 400)
        self.layer2 = torch.nn.Linear(400, 3)
        ### ========== TODO : END ========== ###

    def forward(self, x):
        # x.shape = (n_batch, n_features)

        ### ========== TODO : START ========== ###
        ### part g: implement the foward function
        outputs = self.layer1(x)
        sigmoid = torch.nn.Sigmoid()
        outputs = sigmoid(outputs)
        outputs = self.layer2(outputs)
        ### ========== TODO : END ========== ###
        return outputs

# load data from csv
# X.shape = (n_examples, n_features), y.shape = (n_examples, )
def load_data(filename):
    data = np.loadtxt(filename)
    y = data[:, 0].astype(int)
    X = data[:, 1:].astype(np.float32) / 255
    return X, y

# plot one example
# x.shape = (features, )
def plot_img(x):
    x = x.reshape(28, 28)
    img = Image.fromarray(x*255)
    plt.figure()
    plt.imshow(img)
    return

def evaluate_loss(model, criterion, dataloader):
    model.eval()
    total_loss = 0.0
    for batch_X, batch_y in dataloader:
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        total_loss += loss.item()
        
    return total_loss / len(dataloader)

def evaluate_acc(model, dataloader):
    model.eval()
    total_acc = 0.0
    for batch_X, batch_y in dataloader:
        outputs = model(batch_X)
        predictions = torch.argmax(outputs, dim=1)
        total_acc += (predictions==batch_y).sum()
        
    return total_acc / len(dataloader.dataset)

def train(model, criterion, optimizer, train_loader, valid_loader):
    train_loss_list = []
    valid_loss_list = []
    train_acc_list = []
    valid_acc_list = []
    for epoch in range(1, 31):
        model.train()
        for batch_X, batch_y in train_loader:
            ### ========== TODO : START ========== ###
            ### part f: implement the training process
            optimizer.zero_grad()
            outputs = model.forward(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            ### ========== TODO : END ========== ###
            
        train_loss = evaluate_loss(model, criterion, train_loader)
        valid_loss = evaluate_loss(model, criterion, valid_loader)
        train_acc = evaluate_acc(model, train_loader)
        valid_acc = evaluate_acc(model, valid_loader)
        train_loss_list.append(train_loss)
        valid_loss_list.append(valid_loss)
        train_acc_list.append(train_acc)
        valid_acc_list.append(valid_acc)

        print(f"| epoch {epoch:2d} | train loss {train_loss:.6f} | train acc {train_acc:.6f} | valid loss {valid_loss:.6f} | valid acc {valid_acc:.6f} |")

    return train_loss_list, valid_loss_list, train_acc_list, valid_acc_list

######################################################################
# main
######################################################################

def main():

    # fix random seed
    np.random.seed(0)
    torch.manual_seed(0)

    # load data with correct file path

    ### ========== DONE : START ========== ###
    data_directory_path =  "/content/drive/My Drive/CS146-HW3"
    ### ========== DONE : END ========== ###

    # X.shape = (n_examples, n_features)
    # y.shape = (n_examples, )
    X_train, y_train = load_data(os.path.join(data_directory_path, "hw3_train.csv"))
    X_valid, y_valid = load_data(os.path.join(data_directory_path, "hw3_valid.csv"))
    X_test, y_test = load_data(os.path.join(data_directory_path, "hw3_test.csv"))

    ### ========== DONE : START ========== ###
    ### part a: print out three training images with different labels
    for i in range(3):
      plot_img(X_train[y_train == i][np.random.choice(range(100))])
    
    ### ========== DONE : END ========== ###

    print("Data preparation...")

    ### ========== DONE : START ========== ###
    ### part b: convert numpy arrays to tensors
    X_train = torch.stack([torch.from_numpy(np.array(i)) for i in X_train])
    y_train = torch.stack([torch.from_numpy(np.array(i)) for i in y_train])
    X_valid = torch.stack([torch.from_numpy(np.array(i)) for i in X_valid])
    y_valid = torch.stack([torch.from_numpy(np.array(i)) for i in y_valid])
    X_test = torch.stack([torch.from_numpy(np.array(i)) for i in X_test])
    y_test = torch.stack([torch.from_numpy(np.array(i)) for i in y_test])
    ### ========== DONE : END ========== ###

    ### ========== DONE : START ========== ###
    ### part c: prepare dataloaders for training, validation, and testing
    ###         we expect to get a batch of pairs (x_n, y_n) from the dataloader
    train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
    train_loader = torch.utils.data.DataLoader(train_dataset, shuffle = True, batch_size=10)
    valid_dataset = torch.utils.data.TensorDataset(X_valid, y_valid)
    valid_loader = torch.utils.data.DataLoader(valid_dataset, shuffle = True, batch_size=10)
    test_dataset = torch.utils.data.TensorDataset(X_test, y_test)
    test_loader = torch.utils.data.DataLoader(test_dataset, shuffle = False, batch_size=10)
    ### ========== DONE : END ========== ###

    ### ========== DONE : START ========== ###
    ### part e: prepare OneLayerNetwork, criterion, and optimizer
    model_one = OneLayerNetwork()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model_one.parameters(), lr=0.0005)
    ### ========== DONE : END ========== ###

    print("Start training OneLayerNetwork...")
    results_one = train(model_one, criterion, optimizer, train_loader, valid_loader)
    print("Done!")

    ### ========== TODO : START ========== ###
    ### part h: prepare TwoLayerNetwork, criterion, and optimizer
    model_two = TwoLayerNetwork()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model_two.parameters(), lr=0.0005)
    ### ========== TODO : END ========== ###

    print("Start training TwoLayerNetwork...")
    results_two = train(model_two, criterion, optimizer, train_loader, valid_loader)
    print("Done!")

    one_train_loss, one_valid_loss, one_train_acc, one_valid_acc = results_one
    two_train_loss, two_valid_loss, two_train_acc, two_valid_acc = results_two

    ### ========== DONE : START ========== ###
    ### part i: generate a plot to comare one_train_loss, one_valid_loss, two_train_loss, two_valid_loss
    plt.figure()
    fig, ax = plt.subplots()
    x = range(1, 31)
    line1, = ax.plot(x, one_train_loss, label = 'one_train_loss')
    line2, = ax.plot(x, one_valid_loss, label = 'one_valid_loss')
    line3, = ax.plot(x, two_train_loss, label = 'two_train_loss')
    line4, = ax.plot(x, two_valid_loss, label = 'two_valid_loss')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    ax.legend()
    plt.show()
    plt.savefig ('LossComparison_SGD.png')
    ### ========== DONE : END ========== ###

    ### ========== DONE : START ========== ###
    ### part j: generate a plot to comare one_train_acc, one_valid_acc, two_train_acc, two_valid_acc
    plt.figure()
    fig, ax = plt.subplots()
    x = range(1, 31)
    line1, = ax.plot(x, one_train_acc, label = 'one_train_acc')
    line2, = ax.plot(x, one_valid_acc, label = 'one_valid_acc')
    line3, = ax.plot(x, two_train_acc, label = 'two_train_acc')
    line4, = ax.plot(x, two_valid_acc, label = 'two_valid_acc')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    ax.legend()
    plt.show()
    plt.savefig ('AccuracyComparison_SGD.png')
    ### ========== DONE : END ========== ##

    ### ========== TODO : START ========== ###
    ### part k: calculate the test accuracy
    print("One-layer accuracy: ", evaluate_acc(model_one, test_loader))
    print("Two-layer accuracy: ", evaluate_acc(model_two, test_loader))
    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    ### part l: replace the SGD optimizer with the Adam optimizer and do the experiments again
    model_one = OneLayerNetwork()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model_one.parameters(), lr=0.0005)
    print("Start training OneLayerNetwork...")
    results_one = train(model_one, criterion, optimizer, train_loader, valid_loader)
    print("Done!")

    model_two = TwoLayerNetwork()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model_two.parameters(), lr=0.0005)
    print("Start training TwoLayerNetwork...")
    results_two = train(model_two, criterion, optimizer, train_loader, valid_loader)
    print("Done!")

    one_train_loss, one_valid_loss, one_train_acc, one_valid_acc = results_one
    two_train_loss, two_valid_loss, two_train_acc, two_valid_acc = results_two

    plt.figure()
    fig, ax = plt.subplots()
    x = range(1, 31)
    line1, = ax.plot(x, one_train_loss, label = 'one_train_loss')
    line2, = ax.plot(x, one_valid_loss, label = 'one_valid_loss')
    line3, = ax.plot(x, two_train_loss, label = 'two_train_loss')
    line4, = ax.plot(x, two_valid_loss, label = 'two_valid_loss')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    ax.legend()
    plt.show()
    plt.savefig ('LossComparison_Adam.png')

    plt.figure()
    fig, ax = plt.subplots()
    x = range(1, 31)
    line1, = ax.plot(x, one_train_acc, label = 'one_train_acc')
    line2, = ax.plot(x, one_valid_acc, label = 'one_valid_acc')
    line3, = ax.plot(x, two_train_acc, label = 'two_train_acc')
    line4, = ax.plot(x, two_valid_acc, label = 'two_valid_acc')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    ax.legend()
    plt.show()
    plt.savefig ('AccuracyComparison_Adam.png')

    print("One-layer accuracy: ", evaluate_acc(model_one, test_loader))
    print("Two-layer accuracy: ", evaluate_acc(model_two, test_loader))
    ### ========== TODO : END ========== ###



if __name__ == "__main__":
    main()

