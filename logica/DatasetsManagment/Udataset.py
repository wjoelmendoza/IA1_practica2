import glob
import os
import numpy as np
import h5py

class Udataset:
    origin = ''
    def __init__(selfh):
        pass
        

    def generate_datasets(self,path,flag):
        #creo el dataset de usac
        self.origin = path
        files = os.listdir(self.origin)
        for name in files:
            self.generate_dataset(name,flag)

    def load_dataset(self,path,name,flag):
        print("load_dataset-----------------------------")
        
        train_dataset = h5py.File(path+'/'+name+'.hdf5', "r")
        print(train_dataset)
        print(train_dataset["train_img"])
        print(train_dataset["train_labels"])
        train_set_x_orig = np.array(train_dataset["train_img"][:])  # entradas de entrenamiento
        train_set_y_orig = np.array(train_dataset["train_labels"][:])  # salidas de entrenamiento
        if flag:
            test_dataset = h5py.File(path+'/'+name+'.hdf5', "r")
            test_set_x_orig = np.array(test_dataset["test_img"][:])  # entradas de prueba
            test_set_y_orig = np.array(test_dataset["test_labels"][:])  # salidas de prueba


        train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
        if flag:
            test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
            return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, [name, 'No es '+name]
        return train_set_x_orig, train_set_y_orig, [name, 'No es '+name]

        
    
    
    def generate_dataset_for_prediction(self):
        hdf5_path = os.getcwd()+'/temporales/dataset-test.hdf5'
        origen = os.getcwd()+'/temporales'
        addrs = glob.glob(origen+'/*.jpg')
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(addrs)
        labels = [1 for addr in addrs]
        train_addrs = addrs[0:int(len(addrs))]
        train_labels = labels[0:int(len(labels))]
        #test_addrs = addrs[int(len(addrs)):]
        #test_labels = labels[int(1*len(labels)):]
        ##################### second part: create the h5py object #####################
        train_shape = (len(train_addrs), 128, 128, 3)
        #test_shape = (len(test_addrs), 128, 128, 3)

        # open a hdf5 file and create earrays 
        f = h5py.File(hdf5_path, mode='w')

        # PIL.Image: the pixels range is 0-255,dtype is uint.
        # matplotlib: the pixels range is 0-1,dtype is float.
        f.create_dataset("train_img", train_shape, np.uint8)
        #f.create_dataset("test_img", test_shape, np.uint8)  

        # the ".create_dataset" object is like a dictionary, the "train_labels" is the key. 
        f.create_dataset("train_labels", (len(train_addrs),), np.uint8)
        f["train_labels"][...] = train_labels

        #f.create_dataset("test_labels", (len(test_addrs),), np.uint8)
        #f["test_labels"][...] = test_labels

        ######################## third part: write the images #########################
        # loop over train paths
        for i in range(len(train_addrs)):
        
            if i % 1000 == 0 and i > 1:
                print ('Train data: {}/{}'.format(i, len(train_addrs)) )

            addr = train_addrs[i]
            img = cv2.imread(addr)
            img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)# resize to (128,128)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2 load images as BGR, convert it to RGB
            f["train_img"][i, ...] = img[None] 



        f.close()
        return addrs


    def generate_dataset(self,name,flag):
        hdf5_path = 'Datasets/'+name+'.hdf5'
        files = os.listdir(self.origin)
        addrs = glob.glob(self.origin+'/'+name+'/*.jpg')
        labels = [1 for addr in addrs]
        for namedir in files:
            if namedir != name:
                auxaddrs = glob.glob(self.origin+'/'+namedir+'/*.jpg')
                addrs.extend(auxaddrs)
                labels.extend([0 for addr in auxaddrs])
        # Divide the data into 80% for train and 20% for test
        if flag == None:
            train_addrs = addrs[0:int(1*len(addrs))]
            train_labels = labels[0:int(1*len(labels))]
            test_addrs = addrs[int(1*len(addrs)):]
            test_labels = labels[int(1*len(labels)):]
        
        else:
            train_addrs = addrs[0:int(0.8*len(addrs))]
            train_labels = labels[0:int(0.8*len(labels))]
            test_addrs = addrs[int(0.8*len(addrs)):]
            test_labels = labels[int(0.8*len(labels)):]
        



        
        
        ##################### second part: create the h5py object #####################


        train_shape = (len(train_addrs), 128, 128, 3)
        test_shape = (len(test_addrs), 128, 128, 3)

        # open a hdf5 file and create earrays 
        f = h5py.File(hdf5_path, mode='w')

        # PIL.Image: the pixels range is 0-255,dtype is uint.
        # matplotlib: the pixels range is 0-1,dtype is float.
        f.create_dataset("train_img", train_shape, np.uint8)
        f.create_dataset("test_img", test_shape, np.uint8)  

        # the ".create_dataset" object is like a dictionary, the "train_labels" is the key. 
        f.create_dataset("train_labels", (len(train_addrs),), np.uint8)
        f["train_labels"][...] = train_labels

        f.create_dataset("test_labels", (len(test_addrs),), np.uint8)
        f["test_labels"][...] = test_labels

        ######################## third part: write the images #########################
        # loop over train paths
        for i in range(len(train_addrs)):
        
            if i % 1000 == 0 and i > 1:
                print ('Train data: {}/{}'.format(i, len(train_addrs)) )

            addr = train_addrs[i]
            img = cv2.imread(addr)
            img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)# resize to (128,128)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2 load images as BGR, convert it to RGB
            f["train_img"][i, ...] = img[None] 

        # loop over test paths
        for i in range(len(test_addrs)):

            if i % 1000 == 0 and i > 1:
                print ('Test data: {}/{}'.format(i, len(test_addrs)) )

            addr = test_addrs[i]
            img = cv2.imread(addr)
            img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            f["test_img"][i, ...] = img[None]

        f.close()
