import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Our "real" population and parameter-of-interest stats:
true_mean = 0
true_sd = 1
total_pop = 1000

# Generating a normally distributed array of total_pop elements
fake_data = np.random.normal(true_mean, true_sd, total_pop)

# Our "observed" data:
n = 30  # Play with this number to see how 95% CI can change.
samplings = 100
replicates = 3  # To generate a mean over the each set of 100 samplings' false positives.
all_samplings = []

for replicate in range(replicates):
    samples = set()  # To avoid duplicate resamplings.
    while len(samples) < samplings:
        samples.add(tuple(np.random.choice(fake_data, n, replace=False)))
    all_samplings.append(samples)

sample_means_list = []
sample_ses_list = []

for sampling_group in all_samplings:
    sample_means = []
    sample_ses = []
    for data_set in sampling_group:
        sample_means.append(np.mean(data_set))
        sample_ses.append(stats.sem(data_set))
    sample_means_list.append(sample_means)
    sample_ses_list.append(sample_ses)

all_misses = []
for i in range(replicates):
    misses = 0
    for j in range(samplings):
        upper = sample_means_list[i][j] + 1.96 * sample_ses_list[i][j]
        lower = sample_means_list[i][j] - 1.96 * sample_ses_list[i][j]
        if upper < true_mean or lower > true_mean:
            misses += 1
    all_misses.append(misses)

mean_misses = np.mean(all_misses)
# print('List of misses: {0}'.format(all_misses))
print('Average misses: {0:.2f}'.format(mean_misses))



# PLOTTING THE RESULTS FOR A GIVEN ROUND OF SAMPLING

sample_means = sample_means_list[0]  # The y-axis
sample_ses = sample_ses_list[0]
sample_cis = [se * 1.96 for se in sample_ses]  # The error bar input - 95% CI's
num = [i for i in range(1, len(sample_means) + 1)]  # The x-axis

out_of_range = []
out_of_range_num = []
out_of_range_ci = []
in_range = []
in_range_num = []
in_range_ci = []
for i, mean in enumerate(sample_means):
    upper = mean + sample_cis[i]
    lower = mean - sample_cis[i]
    if upper < true_mean or lower > true_mean:
        out_of_range.append(mean)
        out_of_range_num.append(num[i])
        out_of_range_ci.append(sample_cis[i])
    else:
        in_range.append(mean)
        in_range_num.append(num[i])
        in_range_ci.append(sample_cis[i])

plt.figure()
plt.title("95% CI Replicates for Ideal (Fake) Data (n = {0})".format(n))
plt.xlabel("Replicate of Sampling")
plt.ylabel("Value of Population Metric")

plt.errorbar(in_range_num, in_range, yerr=in_range_ci, fmt='o', color='k')
plt.errorbar(out_of_range_num, out_of_range, yerr=out_of_range_ci, fmt='o', color='r')
plt.axhline(color='g')
plt.yticks((-1, 0, 1), ('-1', '0', '1'))
plt.xlim(0, len(sample_means) + 1)

plt.show()
