import time


# print(time.strftime('%l:%M%p %z on %b %d, %Y')) # ' 1:36PM EST on Oct 18, 2010'


print(time.strftime('%X-%x'))



tijd = time.strftime('%X-%x')

iets = "Experiment_{}_"


print(iets.format(tijd))