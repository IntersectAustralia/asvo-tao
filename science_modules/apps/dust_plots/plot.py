import math
import pylab

pylab.figure(figsize=(14,8))

# x = []
# y = []
# with open('log') as inf:
#     for line in inf:
#         words = line.split(',')
#         x.append(math.log10(float(words[0].strip())))
#         y.append(float(words[1].strip()))
# pylab.plot(x, y)
# pylab.tight_layout()
# pylab.savefig('fesc_vs_lambda.png', dpi=300)

x = [0.005 + ii*0.01 for ii in xrange(100)]
y = []
with open('log') as inf:
    for line in inf:
        y.append(float(line.strip()))
pylab.bar(x, y, 0.01)
pylab.tight_layout()
pylab.savefig('histogram.png', dpi=300)

# x = []
# y = []
# with open('log') as inf:
#     for line in inf:
#         words = line.split(',')
#         x.append(float(words[0].strip()))
#         y.append(float(words[1].strip()))
# pylab.scatter(x, y)
# pylab.xlim([-1, 19])
# pylab.ylim([-0.05, 1.05])
# pylab.tight_layout()
# pylab.savefig('scatter.png', dpi=300)
