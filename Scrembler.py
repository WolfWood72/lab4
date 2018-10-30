from collections import deque
from scipy.stats import chisquare

class Scrembler:
    def __init__(self, init_value, polynom):
        self.init_value = init_value
        self.poly = polynom

    def MakePolyArr(self):
        arr = [0]*self.poly[-1]
        for i in self.poly[:-1]:
            arr[i] = 1
        return arr

    def IntToBitArray(self,n):
        return [int(digit) for digit in bin(n)[2:]]



    def is_balanced(self, interval_len , seq):
        zeros = seq[:interval_len].count(0)
        units = interval_len - zeros
        n = len(seq)
        for i in range(interval_len, n):
            if abs(zeros - units) / interval_len > 0.05:
                return False

            if seq[i] == 1:
                units += 1
            else:
                zeros += 1

            if seq[i - interval_len] == 1:
                units -= 1
            else:
                zeros -= 1
        return True

    def is_cycled(self, seq):

        n = len(seq)

        max_cycle_len = n // 2

        for cycle_len in reversed(range(2, max_cycle_len + 1)):
            interval_num = n // cycle_len
            interval_example = seq[:cycle_len]
            cycled = True
            for i in range(interval_num):
                cur_interval = seq[i * cycle_len: (i + 1) * cycle_len]
                m = len(cur_interval)
                if cur_interval != interval_example[:m]:
                    cycled = False
                    break

            if cycled:
                return cycle_len

        return 0

    def correlation(self, shift, seq):
        shifted_seq =seq[-shift:] + seq[:-shift]
        equal = 0
        for i in range(len(seq)):
            if seq[i] == shifted_seq[i]:
                equal += 1
        if (equal / len(seq)) > 0.95:
            return True
        else:
            return False

    def ChiCquare(self, seq):
        z = seq.count(0) / len(seq)
        o = seq.count(1) / len(seq)
        return chisquare(seq)

    def ChiCquareManual(self, seq):
        z = seq.count(0) / len(seq)
        o = seq.count(1) / len(seq)
        return chisquare([z, o])


    def GetSequence(self, N):
        Seq = []
        poly_bit = list(reversed(self.MakePolyArr()))
        val = deque(self.init_value)
        if len(val) > len(poly_bit):
            poly_bit+= [0]*( len(val) - len(poly_bit))
        while len(val) != len(poly_bit):
            val.appendleft(0)
        for i in range(N):
            v = val[0] & poly_bit[0]
            for s in range(1,len(poly_bit)-1):
                v^=val[s] & poly_bit[s]
            val.appendleft(v)
            Seq.append(val.pop())


     #  print("Сгенерирована последовательность: " + "".join(str(e) for e in Seq))
     #  sb = True
     #  for i in range(1, len(Seq)):
     #      if self.is_balanced(i,Seq):
     #          sb = False
     #          print('Сбалансированность при длинне интервала ' + str(i))
     #          break
     #  if sb:
     #      print('Последовательность не сбалансированна')

     #  if self.is_cycled(Seq) == 0:
     #      print("Цикличность отсутствует")
     #  else:
     #      print("Цикличность присутствует")

     #  for i in range(1,10):
     #      if self.correlation(i,Seq) is False:
     #          print("Корреляция порядка {} отсутствует".format(i))
     #      else:
     #          print("Корреляция порядка {} присутствует".format(i))

     #  print(self.ChiCquareManual(Seq))
        return Seq
