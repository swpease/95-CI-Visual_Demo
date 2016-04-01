#import itertools  # Don't need if just taking a subset of possible combos
import numpy as np
from scipy import stats
import random
import matplotlib as plt
"""
There doesn't appear to be any way to get around just having to go through
a ton of calculations by cheating using generators or something -- at some
point, you have to bite the bullet, so just do it up front.
"""

#np.random.seed(0)
#random.seed(0)

true_mean = 0
true_sd = 1
total_pop = 1000
n = 5  # Play with this number to see how 95% CI can change.

fake_data = np.random.normal(true_mean, true_sd, total_pop)
random.shuffle(fake_data)
# I made a list b/c ndarray is not hashable (for the set() below)

# Getting the random "n = 5" selections from the population (fake_data) [currently seeded]

combos_list = []
cycles = 100
samplings = 100

for run in range(cycles):
    combos = set()
    while len(combos) < samplings:
        combos.add(tuple(fake_data[:n]))
        random.shuffle(fake_data)  # A slow part of this process: O(total_pop * samplings)
    combos_list.append(combos)


sample_means_list = []
sample_ses_list = []

for combo in combos_list:
    sample_means = []
    sample_ses = []
    for i in combo:
        sample_means.append(np.mean(i))
        sample_ses.append(stats.sem(i))
    sample_means_list.append(sample_means)
    sample_ses_list.append(sample_ses)

all_misses = []
for i in range(cycles):
    misses = 0
    for j in range(samplings):
        upper = sample_means_list[i][j] + 1.96 * sample_ses_list[i][j]
        lower = sample_means_list[i][j] - 1.96 * sample_ses_list[i][j]
        if upper < true_mean or lower > true_mean:
            misses += 1
    all_misses.append(misses)

mean_misses = np.mean(all_misses)
print('List of misses: {0}'.format(all_misses))
print('Average misses: {0:.2f}'.format(mean_misses))

# Let's try where n = 5
# perms = set()
# while len(perms) < 100:
#     perms.add(list(itertools.combinations(fake_data, 5)))
#     random.shuffle(fake_data)
#
# print(perms)

#
# all_combos = []
# for i in range(1, len(fake_data) + 1):
#     perms = (np.array(x) for x in itertools.combinations(fake_data, i))
#     all_combos.append(perms)
#
#
# test_of_se = []
# n = 1
# for gen in all_combos:
#     means = (np.mean(i) for i in gen)
#     test_of_se.append((means, n))
#     n += 1
#
# x = 0
# for i in test_of_se[3][0]:
#     x += i
#
# print(x)
# # new_sd = np.std(test_of_se)
# # print(new_sd)
