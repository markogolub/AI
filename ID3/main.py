from reader import *
from ID3 import *

def main():

    # train_dataset = read_csv("logic_small.csv")
    # test_dataset = read_csv("logic_small_test.csv")
    # train_dataset = read_csv("titanic_train_categorical.csv")
    # test_dataset = read_csv("titanic_test_categorical.csv")
    train_dataset = read_csv("volleyball.csv")
    test_dataset = read_csv("volleyball_test.csv")

    model = ID3()
    model.fit(train_dataset)
    model.predict(test_dataset)

if __name__ == '__main__':
    main()