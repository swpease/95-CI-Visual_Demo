# 95-CI-Visual_Demo
Provides some code to give a visual understanding of the meaning behind 95% confidence intervals

I decided to make this little program because I vaguely recall that my intro stats teachers just kind of glossed over what confidence intervals *mean*, while my more advanced stats teacher(s? -- at least one of them) were all finicky about being pinned down to a particular definition.

This demonstration relies on fake data generated using a normal distribution. It provides two possible outputs:

1. A terminal-based result of the average number of samplings across replicates whose 95% CI did not encompass the true mean.
2. A plot of a given set of 100 (or however many you want) samplings with their 95% CI's, with those that do not encompass the true mean highlighted in red.
