from pso import particle_swarm_optimisation, parallel_particle_swarm_optimisation
from time import time
import math


def Ackley(X):
    firstSum = 0.0
    secondSum = 0.0
    for x in X:
        firstSum += x**2.0
        secondSum += math.cos(2.0*math.pi*x)
    n = float(len(X))
    return -20.0*math.exp(-0.2*math.sqrt(firstSum/n)) - math.exp(secondSum/n) + 20 + math.e


if __name__ == "__main__":
    t1 = time()
    X = parallel_particle_swarm_optimisation(
        Ackley, -100, 100, maxiter=100, npart=1000, printData=True, dim=10)
    y = Ackley(X)
    t2 = time()
    print(X)
    print(y)
    print("Potrebno vreme: " + str(t2 - t1))
