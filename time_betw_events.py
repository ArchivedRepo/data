import matplotlib.pyplot as plt

import csv

lst_unlock = []
lst_17f = []
lst_22f = []
lst_27f = []

with open('/Users/will/Downloads/399_test/output_150000_cw_aggr_0312.dat') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=']')
    sum_unlock = 0
    sum_17 = 0
    sum_22 = 0
    sum_27 = 0

    for row in csv_reader:
        # print(row)
        pre = row[1].split(' ')
        lst = pre[1].split(':')
        # print(lst)
        value = int(lst[0])
        key = lst[1]

        sum_unlock += value
        sum_17 += value
        sum_22 += value
        sum_27 += value

        if key == '18f':
            lst_unlock.append(sum_unlock)
            sum_unlock = 0
        elif key == '17f':
            lst_17f.append(sum_17)
            sum_17 = 0
        elif key == '22f':
            lst_22f.append(sum_22)
            sum_22 = 0
        elif key == '27f':
            lst_27f.append(sum_27)
            sum_27 = 0

final_unlock = lst_unlock
final_17 = lst_17f
final_22 = lst_22f
final_27 = lst_27f


# print('T:' + str(final_unlock[1]))
# print(final_17)
# print(final_22)
# print(final_27)


# Number of packets per second
def packet_sec(a: list) -> list:
    lst_result = []
    sum_sec = 0
    n = 0
    for element in a:
        s = sum_sec + element
        if s >= 10 ** 6:
            lst_result.append(n)
            sum_sec = 0
            n = 0
        else:
            sum_sec += element
            n += 1

    return lst_result


# print(packet_sec(final_17))
# print(packet_sec(final_22))
# print(packet_sec(final_27))


def timestamp(a: list) -> list:
    lst_ts = []
    s = 0
    for i in a:
        s += i
        lst_ts.append(s)
    return lst_ts


def sending_rate_sec(a: list) -> list:
    return len(a) / timestamp(a)[-1] * 10 ** 6


# print(sending_rate_sec(final_17))
# print(sending_rate_sec(final_27))
# print(sending_rate_sec(final_22))

def plot():
    left = timestamp(final_17).copy()[:500]
    right = timestamp(final_22).copy()[:500]
    mid = timestamp(final_27).copy()[:500]

    index_mid = 0
    for i in range(len(mid)):
        index_mid += 1
        if mid[i] > left[499]:
            break

    mid = mid[:index_mid].copy()

    left_h = [2 for i in range(500)]
    mid_h = [1 for i in range(index_mid)]
    right_h = [0 for i in range(500)]

    l = plt.plot(left, left_h, 'o', 'left', color='r')
    m = plt.plot(mid, mid_h, 'o', 'mid', color='g')
    r = plt.plot(right, right_h, 'o', 'right', color='b')

    for i in timestamp(final_unlock[:50]):
        plt.axvline([i])
    plt.xlabel('time/microsecond')

    plt.show()


plot()


def lst_avg_rate(unlock_cycle: int, a: list) -> list:
    """Return a list of throughput (packets per second) averaged over a window
     of 1/10 unclock-cycle."""
    lst_rate = [[], []]  # x-values for timestamps in micro seconds,
    # y-values for throughput avgs in packets per second
    window_size = 1/10 * unlock_cycle  # in micro seconds
    c = 0
    s = 1  # sum of packets transmission time, <= window_size
    n = 0  # number of packets accumulating within the size of the window
    time = 0
    while c < len(a):
        q = s + a[c]
        if q > window_size:
            lst_rate[1].append(n/(s * 10**(-6)))
            lst_rate[0].append(time)
            s = 1
            n = 0
        s += a[c]
        n += 1
        time += a[c]
        c += 1
    return lst_rate

# print(lst_avg_rate(80000, final_17))

def plot_thru_avg():

    t = final_unlock[1]

    plt.plot(lst_avg_rate(t, final_17)[0],
             lst_avg_rate(t, final_17)[1], 'y-')

    plt.plot(lst_avg_rate(t, final_27)[0],
             lst_avg_rate(t, final_27)[1], 'r-')

    plt.plot(lst_avg_rate(t, final_22)[0],
             lst_avg_rate(t, final_22)[1], 'g-')

    for i in timestamp(final_unlock):
        plt.axvline([i])

    plt.show()


# overall avg thruput
print(len(timestamp(final_17))/timestamp(final_17)[-1] * 10**6)  # mu sec

plt.plot(timestamp(final_17), final_17)
plt.plot(timestamp(final_22), final_22)
plt.plot(timestamp(final_27), final_27)
for sig in timestamp(final_unlock)[:30]:
    plt.axvline(sig)
# plt.ylim(1, 3000)
# plt.xlim(0, 1500)
plt.show()

