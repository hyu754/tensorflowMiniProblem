import h5py
import numpy as np
try:
    import tensorflow as tf
    from tensorflow.examples.tutorials.mnist import input_data
except:
    print ("TF does not exist")
import math

import csv

#loads data in csv format, one_hot_true = True : if the data is in one hot format
def load_csv(file_name,delimiter_string,one_hot_true,num_category ,randomly_assign_train_test = True):
    data_container = []
    with open(file_name, 'rt',encoding='ascii') as csvfile:
        data = csv.reader(csvfile, delimiter=delimiter_string)
        print (data)
        for row_ in data:
            data_container.append(row_)
    #print (data_container)
    data_container = np.array(data_container)
    
    rows,cols = data_container.shape

    Y = data_container[:,cols-num_category:cols]
    Y = np.array(Y)

    X = data_container[:,0:cols-num_category]

    train_X=[]
    train_Y=[]
    test_X=[]
    test_Y=[]

    for i in range(0,rows):
        if(np.random.rand()<0.8):
            train_X.append(X[i,:])
            train_Y.append(Y[i])
        else:
            test_X.append(X[i,:])
            test_Y.append(Y[i])
    classes=np.array(range(num_category)) 

    train_X = np.array(train_X)
    train_Y = np.array(train_Y)
    test_X = np.array(test_X)
    test_Y = np.array(test_Y)
    print(train_X.shape)
    print(test_X.shape)
    train_X = train_X.T
    train_Y = train_Y.T
    test_X = test_X.T
    test_Y = test_Y.T
    return train_X, train_Y, test_X, test_Y, classes


def load_dataset_mnist(flatten):

    mnist = input_data.read_data_sets('dataset_mnist', one_hot=True)
    #return mnist
    train_set_x_orig=mnist.train.images
    train_set_y_orig=mnist.train.labels
    test_set_x_orig= mnist.test.images
    test_set_y_orig=mnist.test.labels 
    classes=np.array(range(10))

    #transpose everything
    train_set_x_orig = np.transpose(train_set_x_orig)
    train_set_y_orig = np.transpose(train_set_y_orig)
    test_set_x_orig = np.transpose(test_set_x_orig)
    test_set_y_orig= np.transpose(test_set_y_orig)

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes
    #'images, labels = mndata.load_testing()

def load_dataset_sign_language(flatten):
    train_dataset = h5py.File('datasets/train_signs.h5', "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:]) # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) # your train set labels

    test_dataset = h5py.File('datasets/test_signs.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:]) # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your test set labels

    classes = np.array(test_dataset["list_classes"][:]) # the list of classes
    X_train = train_set_x_orig/255
    X_test = test_set_x_orig/255
    #Y_train = train_set_y_orig
    #Y_test = test_set_y_orig
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    Y_train = convert_to_one_hot(train_set_y_orig, 6)
    Y_test = convert_to_one_hot(test_set_y_orig, 6)
    Y_train= np.transpose(Y_train)
    Y_test = np.transpose(Y_test)
    if(flatten== True):
        train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
        test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
        
        X_train_flatten = train_set_x_orig.reshape(train_set_x_orig.shape[0], -1).T
        X_test_flatten = test_set_x_orig.reshape(test_set_x_orig.shape[0], -1).T
        # Normalize image vectors
        X_train = X_train_flatten/255.
        X_test = X_test_flatten/255.
        # Convert training and test labels to one hot matrices
        Y_train = convert_to_one_hot(train_set_y_orig, 6)
        Y_test = convert_to_one_hot(test_set_y_orig, 6)
    return X_train, Y_train, X_test, Y_test, classes


def random_mini_batches_NN(X, Y, mini_batch_size = 64, seed = 0):
    """
    Creates a list of random minibatches from (X, Y)
    
    Arguments:
    X -- input data, of shape (input size, number of examples)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples)
    mini_batch_size - size of the mini-batches, integer
    seed -- this is only for the purpose of grading, so that you're "random minibatches are the same as ours.
    
    Returns:
    mini_batches -- list of synchronous (mini_batch_X, mini_batch_Y)
    """
    
    m = X.shape[1]                  # number of training examples
    mini_batches = []
    np.random.seed(seed)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation].reshape((Y.shape[0],m))

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, k * mini_batch_size : k * mini_batch_size + mini_batch_size]
        mini_batch_Y = shuffled_Y[:, k * mini_batch_size : k * mini_batch_size + mini_batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[:, num_complete_minibatches * mini_batch_size : m]
        mini_batch_Y = shuffled_Y[:, num_complete_minibatches * mini_batch_size : m]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches



def random_mini_batches_CNN(X, Y,c, mini_batch_size = 64, seed = 0):
    """
    Creates a list of random minibatches from (X, Y)
    
    Arguments:
    X -- input data, of shape (input size, number of examples) (m, Hi, Wi, Ci)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples) (m, n_y)
    mini_batch_size - size of the mini-batches, integer
    seed -- this is only for the purpose of grading, so that you're "random minibatches are the same as ours.
    
    Returns:
    mini_batches -- list of synchronous (mini_batch_X, mini_batch_Y)
    """
    
    m = X.shape[0]                  # number of training examples
    #c = X.shape[3]                  #number of channels
    mini_batches = []
    np.random.seed(seed)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    if(c == 3):
        shuffled_X = X[permutation,:,:,:]
    elif(c==1):
        shuffled_X = X[permutation,:]
    shuffled_Y = Y[permutation,:]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        if(c==3):
            mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:,:,:]
        elif(c==1):
            mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        if(c==3):
            mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:,:,:]
        elif(c==1):
            mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches
def convert_to_one_hot(Y, C):
    Y = np.eye(C)[Y.reshape(-1)].T
    return Y


def sigmoid(z):
    
    x = tf.placeholder(tf.float32,name = "x")

    # compute sigmoid(x)
    sigmoid = tf.sigmoid(x)

    with tf.Session() as sess:
        
        result = sess.run(sigmoid,feed_dict = {x:z})
    
    
    return result




def one_hot_matrix(labels, C):
    """
    Creates a matrix where the i-th row corresponds to the ith class number and the jth column
                     corresponds to the jth training example. So if example j had a label i. Then entry (i,j) 
                     will be 1. 
                     
    Arguments:
    labels -- vector containing the labels 
    C -- number of classes, the depth of the one hot dimension
    
    Returns: 
    one_hot -- one hot matrix
    """
    
    ### START CODE HERE ###
    
    # Create a tf.constant equal to C (depth), name it 'C'. (approx. 1 line)
    C = tf.constant(C,name= "C");
    
    # Use tf.one_hot, be careful with the axis (approx. 1 line)
    one_hot_matrix = tf.one_hot(labels,C,axis = 0)
    
    # Create the session (approx. 1 line)
    sess = tf.Session()
    
    # Run the session (approx. 1 line)
    one_hot = sess.run(one_hot_matrix)
    
    # Close the session (approx. 1 line). See method 1 above.
    sess.close()
    
    ### END CODE HERE ###
    
    return one_hot


def ones(shape):
    """
    Creates an array of ones of dimension shape
    
    Arguments:
    shape -- shape of the array you want to create
        
    Returns: 
    ones -- array containing only ones
    """
    
    ### START CODE HERE ###
    ones = tf.ones(shape)
    
    # Create the session (approx. 1 line)
    sess = tf.Session()
    
    # Run the session to compute 'ones' (approx. 1 line)
    ones = sess.run(ones)
    
    # Close the session (approx. 1 line). See method 1 above.
    sess.close()
    
    ### END CODE HERE ###
    return ones



if __name__ == "__main__":
    load_csv("datasets/sampleMeatData.csv",",",True,3)