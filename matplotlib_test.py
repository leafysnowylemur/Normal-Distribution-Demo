import matplotlib.pyplot as plt
import random
import time
import multiprocessing
import numpy as np
from math import *

# how many times to simulate the rolling of the dice
n = 100000
# how many dice to roll
j = 10

# Define the simulate_dice_roll function here
def simulate_dice_roll(_):
    total = 0
    for x in range(0, j):
        total += random.randint(1, 6)
    return total

if __name__ == '__main__':
    print("Simulating", j, "die rolls", n, "times")
    
    # Single-threaded version
    def single_threaded():
        start_time = time.time()

        total_single = 0
        values_single = []
        unique_values_single = []
        occurances_single = []
        
        for i in range(1, n):
            for x in range(0, j):
                total_single += random.randint(1, 6)
            values_single.append(total_single)
            total_single = 0

        unique_values_single = list(set(values_single))

        for value_single in unique_values_single:
            occur_num_single = values_single.count(value_single)
            occurances_single.append(occur_num_single)

        end_time = time.time()
        print("Single-threaded version took:", end_time - start_time, "seconds")
        return unique_values_single, occurances_single
    
    # Multi-threaded version
    def multi_threaded():  
        values_double = []
        unique_values_double = []
        occurances_double = []
            
        start_time = time.time()

        pool = multiprocessing.Pool()
        values_double = pool.map(simulate_dice_roll, range(1, n))
        unique_values_double = list(set(values_double))
        occurances_double = [values_double.count(value_double) for value_double in unique_values_double]

        end_time = time.time()
        print("Multi-threaded version took:", end_time - start_time, "seconds")
        return unique_values_double, occurances_double
    
    single = single_threaded()
    double = multi_threaded()
    
    
    
    unique_values = single[0] + double[0]
    occurances = single[1] + double[1]
    
    y = []
    for x in occurances:
        y.append(x/n)
    
    # Normal Distribution Equation
    # calculate the mean of the values
    mean = np.average(unique_values, weights=occurances)

    # calculate the variance of the values
    variance = np.average((unique_values-mean)**2, weights=occurances)

    # calculate the standard deviation of the values
    std_dev = np.sqrt(variance)
    
    def normal_distribution(input, m, std):
        exponent = -1/2 * ((input - m)/std)**2
        coefficient = 1/(std*sqrt(2*pi))
        return coefficient * exp(exponent)
    
    n_dist_x = []
    n_dist_y = []
    
    for x in np.arange(mean-4*std_dev, mean+4*std_dev, .1):
        n_dist_x.append(x)
        n_dist_y.append(normal_distribution(x, mean, std_dev))
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.bar(unique_values, y)
    ax1.set_xlabel('Unique Values')
    ax1.set_ylabel('Percentage of Occurrences')
    ax1.set_title('Simulated Dice Rolls')
    
    ax2.plot(n_dist_x, n_dist_y)
    ax2.set_xlabel('Values')
    ax2.set_ylabel('Predicted Probability')
    ax2.set_title("Calculated Normal Distribution")
    
    text = str("Simulating the distribution of the sum of " + str(j) + " dice " + str(n) + " times")
    print(text)
    plt.annotate(text, xy=(0, -.138), xycoords='axes fraction', ha='center')

    plt.show()