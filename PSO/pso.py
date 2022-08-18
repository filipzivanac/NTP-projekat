from functools import partial
from turtle import position
import numpy as np
from multiprocessing import Process, Queue, Value, Pool, cpu_count


class Particle:
    def __init__(self, lb, ub, dim):
        self.pozicija = np.random.uniform(low=lb, high=ub, size=dim)
        self.brzina = np.full(dim, 0, dtype=np.dtype("Float64"))
        self.y = np.Inf
        self.najbolji_X = self.pozicija
        self.najbolji_y = self.y


def particle_swarm_optimisation(funkcija, lowerb, upperb, maxiter=20, npart=50, dim=60, tol=10**-15, printData=False):
    w = 1
    dmp = 0.99
    c1 = 2.5
    c2 = 0.5
    # Inicijalizacija
    particles = []
    globalno_najbolji_X = "Neka najbolji pobedi"
    globalno_najbolji_y = np.Inf
    for k in range(npart):
        p = Particle(lowerb, upperb, dim)
        p.y = funkcija(p.pozicija)
        particles.append(p)
        if p.y < globalno_najbolji_y:
            globalno_najbolji_X = p.pozicija
            globalno_najbolji_y = p.y

    # glavna petlja
    file = open("res.txt", "w+")
    for i in range(maxiter):
        for j in range(len(particles)):
            particles[j].brzina = w * particles[j].brzina + c1 * np.random.uniform(size=dim) * (
                particles[j].najbolji_X - particles[j].pozicija) + c2 * np.random.uniform(size=dim) * (
                globalno_najbolji_X - particles[j].pozicija)

            particles[j].pozicija = particles[j].pozicija + particles[j].brzina

            particles[j].y = funkcija(particles[j].pozicija)

            if particles[j].y < particles[j].najbolji_y:
                particles[j].najbolji_X = particles[j].pozicija
                particles[j].najbolji_y = particles[j].y
                if particles[j].y < globalno_najbolji_y:
                    globalno_najbolji_X = particles[j].pozicija
                    if abs(globalno_najbolji_y - particles[j].y) < tol:
                        print("Izlaz! Razbijen kriterijum tolerancije")
                        file.close()
                        return globalno_najbolji_X
                    globalno_najbolji_y = particles[j].y

        w = w * dmp
        c1 = c1 - 2 / (maxiter*(maxiter-i))
        c2 = c2 + 2 / (maxiter*(maxiter-i))
        if printData:
            print(str(i) + ". Globalno " + str(globalno_najbolji_y))
            file.write("Iteracija: "+str(i) + ". Najbolji y: " +
                       str(globalno_najbolji_y)+" najbolji X: "+str(globalno_najbolji_X)+" \n")
    file.close()
    return globalno_najbolji_X


def parallel_particle_swarm_optimisation2(funkcija, lowerb, upperb, maxiter=20, npart=50, dim=60, tol=10**-15, printData=False):

    w = 1
    dmp = 0.99
    c1 = 2.5
    c2 = 0.5
    # Inicijalizacija
    particles = []
    globalno_najbolji_X = "Neka najbolji pobedi"
    globalno_najbolji_y = np.Inf
    for k in range(npart):
        p = Particle(lowerb, upperb, dim)
        p.y = funkcija(p.pozicija)
        particles.append(p)
        if p.y < globalno_najbolji_y:
            globalno_najbolji_X = p.pozicija
            globalno_najbolji_y = p.y

    # glavna petlja
    file = open("res.txt", "w+")

    print("oids")
    for i in range(maxiter):
        localqueue = Queue(maxsize=100)
        globalqueue = Queue(maxsize=100)
        processes = []
        for j in range(len(particles)):
            p = Process(target=update_particle, args=(localqueue, globalqueue,
                        particles[j], j, globalno_najbolji_X, globalno_najbolji_y, dim, funkcija, w, c1, c2))
           # print("proces: "+str(j))
            processes.append(p)
        for p in processes:
            p.start()
        print("all started " + str(i))
        while localqueue.empty() is False:
            lres = localqueue.get()
            particles[lres[0]] = lres[1]
        while globalqueue.empty() is False:
            gres = globalqueue.get()
            if(gres[1] < globalno_najbolji_y):
                globalno_najbolji_X = gres[0]
                globalno_najbolji_y = gres[1]
        for p in processes:

            p.join()
        print("all joined " + str(i))

        w = w * dmp
        c1 = c1 - 2 / (maxiter*(maxiter-i))
        c2 = c2 + 2 / (maxiter*(maxiter-i))
        if printData:
            print(str(i) + ". Globalno " + str(globalno_najbolji_y))
            file.write("Iteracija: "+str(i) + ". Najbolji y: " +
                       str(globalno_najbolji_y)+" najbolji X: "+str(globalno_najbolji_X)+" \n")
    file.close()

    return globalno_najbolji_X


def update_particle(localqueue, globalqueue, particle, index, globalno_najbolji_X, globalno_najbolji_y, dim, funkcija, w, c1, c2):
    particle.brzina = w * particle.brzina + c1 * np.random.uniform(size=dim) * (
        particle.najbolji_X - particle.pozicija) + c2 * np.random.uniform(size=dim) * (
        globalno_najbolji_X - particle.pozicija)

    particle.pozicija = particle.pozicija + particle.brzina

    particle.y = funkcija(particle.pozicija)
    # print("part"+str(index))
    if particle.y < particle.najbolji_y:
        particle.najbolji_X = particle.pozicija
        particle.najbolji_y = particle.y
        localqueue.put([index, particle])
        if particle.y < globalno_najbolji_y:
            globalqueue.put([particle.pozicija, particle.y])
            globalno_najbolji_X = particle.pozicija
            globalno_najbolji_y = particle.y
    return


def evaluate(result, position, function):
    result.value = function(position)
    return


def parallel_particle_swarm_optimisation(funkcija, lowerb, upperb, maxiter=20, npart=50, dim=60, tol=10**-15, printData=False):
    w = 1
    dmp = 0.99
    c1 = 2.5
    c2 = 0.5
    # Inicijalizacija
    particles = []
    globalno_najbolji_X = "Neka najbolji pobedi"
    globalno_najbolji_y = np.Inf
    for k in range(npart):
        p = Particle(lowerb, upperb, dim)
        p.y = funkcija(p.pozicija)
        particles.append(p)
        if p.y < globalno_najbolji_y:
            globalno_najbolji_X = p.pozicija
            globalno_najbolji_y = p.y

    # glavna petlja
    file = open("res.txt", "w+")
    for i in range(maxiter):
        processes = []
        results = []
        for j in range(len(particles)):
            particles[j].brzina = w * particles[j].brzina + c1 * np.random.uniform(size=dim) * (
                particles[j].najbolji_X - particles[j].pozicija) + c2 * np.random.uniform(size=dim) * (
                globalno_najbolji_X - particles[j].pozicija)

            particles[j].pozicija = particles[j].pozicija + particles[j].brzina
            res = Value('d', 0.0)
            p = Process(target=evaluate, args=(
                res, particles[j].pozicija, funkcija))
            processes.append(p)
            results.append(res)

        for p in processes:
            p.start()
        for p in processes:
            p.join()

        for j in range(len(particles)):
            particles[j].y = results[j].value
            if particles[j].y < particles[j].najbolji_y:
                particles[j].najbolji_X = particles[j].pozicija
                particles[j].najbolji_y = particles[j].y
                if particles[j].y < globalno_najbolji_y:
                    globalno_najbolji_X = particles[j].pozicija
                    if abs(globalno_najbolji_y - particles[j].y) < tol:
                        print("Izlaz! Razbijen kriterijum tolerancije")
                        file.close()
                        return globalno_najbolji_X
                    globalno_najbolji_y = particles[j].y

        w = w * dmp
        c1 = c1 - 2 / (maxiter*(maxiter-i))
        c2 = c2 + 2 / (maxiter*(maxiter-i))
        if printData:
            print(str(i) + ". Globalno " + str(globalno_najbolji_y))
            file.write("Iteracija: "+str(i) + ". Najbolji y: " +
                       str(globalno_najbolji_y)+" najbolji X: "+str(globalno_najbolji_X)+" \n")
    file.close()
    return globalno_najbolji_X


def parallel_particle_swarm_optimisation3(funkcija, lowerb, upperb, maxiter=20, npart=50, dim=60, tol=10**-15, printData=False):

    w = 1
    dmp = 0.99
    c1 = 2.5
    c2 = 0.5
    # Inicijalizacija
    particles = []
    globalno_najbolji_X = "Neka najbolji pobedi"
    globalno_najbolji_y = np.Inf
    for k in range(npart):
        p = Particle(lowerb, upperb, dim)
        p.y = funkcija(p.pozicija)
        particles.append(p)
        if p.y < globalno_najbolji_y:
            globalno_najbolji_X = p.pozicija
            globalno_najbolji_y = p.y

    # glavna petlja
    file = open("res.txt", "w+")

    print("oids")
    for i in range(maxiter):
        p = Pool(processes=10)
        results = p.map(partial(update_particle_pool, globalno_najbolji_X=globalno_najbolji_X,
                        dim=dim, funkcija=funkcija, w=w, c1=c1, c2=c2), particles)
        particles = results
        p.close()
        p.join()
        for j in range(len(particles)):
            if particles[j].y < globalno_najbolji_y:
                globalno_najbolji_X = particles[j].pozicija
                if abs(globalno_najbolji_y - particles[j].y) < tol:
                    print("Izlaz! Razbijen kriterijum tolerancije")
                    file.close()
                    return globalno_najbolji_X
                globalno_najbolji_y = particles[j].y

        w = w * dmp
        c1 = c1 - 2 / (maxiter*(maxiter-i))
        c2 = c2 + 2 / (maxiter*(maxiter-i))
        if printData:
            print(str(i) + ". Globalno " + str(globalno_najbolji_y))
            file.write("Iteracija: "+str(i) + ". Najbolji y: " +
                       str(globalno_najbolji_y)+" najbolji X: "+str(globalno_najbolji_X)+" \n")
    file.close()

    return globalno_najbolji_X


def update_particle_pool(particle, globalno_najbolji_X, dim, funkcija, w, c1, c2):
    particle.brzina = w * particle.brzina + c1 * np.random.uniform(size=dim) * (
        particle.najbolji_X - particle.pozicija) + c2 * np.random.uniform(size=dim) * (
        globalno_najbolji_X - particle.pozicija)

    particle.pozicija = particle.pozicija + particle.brzina

    particle.y = funkcija(particle.pozicija)
    # print("part"+str(index))
    if particle.y < particle.najbolji_y:
        particle.najbolji_X = particle.pozicija
        particle.najbolji_y = particle.y
    return particle
