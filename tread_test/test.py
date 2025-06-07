import threading
import time

done = False

def worker(text):
    counter = 0
    while not done:
        time.sleep(1)
        counter += 1
        print(f"{text}: {counter}")

t1 = threading.Thread(target=worker, daemon=True, args=("ABC",))
t2 = threading.Thread(target=worker, daemon=False, args=("XYZ",))

t1.start()
t2.start()

input('Pres enter to quit')
done = True

#t1.join()
#t2.join()