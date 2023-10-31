import matplotlib.pyplot as plt
import numpy as np

# Given time data
rbt_times = {
    'Initialization': [0.0, 0.0, 0.0009951591491699219, 0.0, 0.000997781753540039, 0.0, 0.0, 0.000997304916381836, 0.0, 0.0009992122650146484, 0.0, 0.000993490219116211, 0.0, 0.0009953975677490234, 0.0009970664978027344, 0.0009963512420654297, 0.0, 0.0009989738464355469, 0.0, 0.0009951591491699219, 0.0, 0.0009961128234863281, 0.0, 0.0009996891021728516, 0.0, 0.0009946823120117188, 0.0, 0.0009953975677490234, 0.0, 0.0009965896606445312, 0.0009965896606445312, 0.0009968280792236328, 0.0009989738464355469],
    'Deletion': [0.0009953975677490234],
    'Insertion': [0.0009622573852539062]
}

bt_times = {
    'Initialization': [0.0009884834289550781, 0.0, 0.0, 0.000993490219116211, 0.0, 0.0, 0.0009965896606445312, 0.0, 0.0, 0.001007080078125, 0.0, 0.0010037422180175781, 0.0, 0.0009818077087402344, 0.0, 0.0009243488311767578, 0.0, 0.0009953975677490234, 0.0, 0.0009968280792236328, 0.0, 0.0010406970977783203, 0.0, 0.0009827613830566406, 0.0, 0.0010504722595214844, 0.0, 0.0009949207305908203, 0.0, 0.0009860992431640625, 0.0, 0.000997304916381836, 0.0],
    'Deletion': [0.0009846687316894531],
    'Insertion': [0.0009152889251708984]
}

# Calculating average times for each operation
avg_rbt_times = {op: np.mean(times) for op, times in rbt_times.items()}
avg_bt_times = {op: np.mean(times) for op, times in bt_times.items()}

print(avg_rbt_times.values())
print(avg_bt_times.values())

# Bar chart
labels = avg_rbt_times.keys()
rbt_means = avg_rbt_times.values()
bt_means = avg_bt_times.values()

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, rbt_means, width, label='RBT')
rects2 = ax.bar(x + width/2, bt_means, width, label='BT')

# Adding text labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Operations')
ax.set_ylabel('Average Time')
ax.set_title('Average Time per Operation by Data Structure')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()
