import numpy as np


class Sliceable:
    def __getitem__(self, key):
        first = True
        for v in vars(self):
            if first is True:
                s = getattr(self, v)[key].shape
                if np.size(s) == 2:
                    n = s[0]
                else:
                    n = 1

                sliced_state = self.__class__(n)
                first = False

            getattr(sliced_state, v)[:] = getattr(self, v)[key]

        return sliced_state

    def __setitem__(self, sliced, sliced_state):
        for v in vars(self):
            getattr(self, v)[sliced] = getattr(sliced_state, v)
