# Dummy Stock Market in 10 lines of Python
import numpy as np
import matplotlib.pyplot as plt
mu = 0.001                          #First variable
sigma = 0.01                        #Second variable
start_price = 5                     #Start Price
np.random.seed(0)                   #Set Seed
returns = np.random.normal(loc=mu, scale=sigma, size=100)
price = start_price*(1+returns).cumprod()
plt.plot(price)