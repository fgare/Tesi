from typing import List
from datetime import datetime
import os

FILENAME = "recordedTimes.csv"


class Stopwatch:
    def __init__(self, steps:int):
        self._STEPS = steps
        self._times = [] * self._STEPS
        self._i: int = 0

    def lap(self, position=None):
        if isinstance(position,int):
            self._times.insert(position, datetime.now())
        else:
            self._times.insert(self._i, datetime.now())
            self._i += 1

    def reset(self):
        self._i = 0

    def get_intervals(self):
        intervals = []
        for j in range(self._STEPS-1):
            intervals.append(self._times[j+1] - self._times[j])
        return intervals

    def save(self):
        current_folder = os.getcwd()
        print("Current folder = ", current_folder)
        complete_path = os.path.join(current_folder, FILENAME)

        try:
            with open(complete_path, 'a+') as file:
                for j in range(self._STEPS):
                    file.write(f"{self._times[j]}")  # scrive elemento j-esimo della lista
                    if j < self._STEPS-1:
                        file.write(";")
                file.write("\n")
        except Exception as e:
            print("Exception during the opening of file")
        finally:
            file.close()
