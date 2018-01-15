import time
class Timer:
    def __init__(self, tracker):
        print('started ' + tracker)
        self.t0 = time.time()
        self.tracker = tracker
    def stop(self):
        print('finished ' + self.tracker + ' in ' + time.now() - self.t0 + ' seconds.')
