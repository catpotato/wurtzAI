import time
log = True
class Timer:
    def __init__(self, tracker):
        if log:
            print('started ' + tracker)
        self.t0 = time.time()
        self.tracker = tracker
    def stop(self):
        if log:
            print('finished ' + self.tracker + ' in ' + str(time.time() - self.t0) + ' seconds.')
