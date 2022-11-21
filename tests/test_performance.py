import time

from serenipy.ms2 import from_ms2

if __name__ == '__main__':
    start_time = time.time()

    with open("C://data//169.ms2", 'r') as file:
    #with open("data/sample.ms2", 'r') as file:

        header, ms2_spectras = from_ms2(file.read(), processes=5)
        print(len(ms2_spectras))
        print(ms2_spectras[-1])

    print(time.time() - start_time)

# 2021806_ANL-1
# multi_process=1: 19s
# multi_process=5: 26s

# 169
# multi_process=1: 30s (48009)
# multi_process=5: 32s (48009)
# multi_process=10: 30s (48009)


