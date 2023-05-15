from shopping import *

if __name__ == '__main__':
    data = load_data("shopping.csv")
    print(data[0][:10])
    print(data[1][:10])
    print(len(data[0]), len(data[1]))
