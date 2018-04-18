import datetime
from random import uniform

def mock_data(variance=5.0):
    while True:
        yield datetime.datetime.now(), 20 + uniform(-variance, variance)



if __name__ == "__main__":
    i = 0
    generator = mock_data(1.0)
    while i < 10:
        print(next(generator))
        i += 1
