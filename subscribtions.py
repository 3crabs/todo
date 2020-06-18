from threading import Thread
from time import sleep


def f():
    while True:
        sleep(5 * 60 * 60)


t = Thread(target=f)
t.start()
