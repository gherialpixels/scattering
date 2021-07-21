

if __name__ == '__main__':
    import time

    start1 = time.time()
    x = 5
    for i in range(100000):
        if x > 6:
            pass
    end1 = time.time()
    t1 = end1 - start1
    start2 = time.time()
    y = 5
    for i in range(100000):
        pass
    end2 = time.time()
    t2 = end2 - start2

    print('The time taken by if statement is: ', t1 - t2)
