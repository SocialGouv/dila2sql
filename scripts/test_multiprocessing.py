

from multiprocessing import Pool, Queue
import time

def f(q):
    q.put([1])
    return x*x

if __name__ == '__main__':
    q1 = Queue()
    pool = Pool(processes=4)
    res1 = pool.apply_async(f, (q1,))
    res2 = pool.apply_async(f, (q1,))
    pool.close()
    pool.join()
    print(q1.get())
