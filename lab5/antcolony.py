from ant import Ant
import copy

def epoca(noAnts, n, trace, alpha, beta, q0, rho):

    antSet=[Ant(n) for i in range(noAnts)]
    for _ in range(n):
        dTrace={}

        for x in antSet:
            x.addMove(q0, trace, alpha, beta)
        for ant in antSet:
            if ant.path[-1] not in dTrace:
                dTrace[ant.path[-1]] = 1.0 / ant.fitness
            else:
                dTrace[ant.path[-1]] = dTrace[(ant.lastPosition,ant.lastMove)]+1.0 / ant.fitness

    for move in trace:
        trace[move] = (1 - rho) * trace[move]
    for move in dTrace:
        if move not in trace:
            trace[move]=dTrace[move]
        else:
            trace[move]=trace[move] + dTrace[move]
    return sorted(antSet, key=lambda x:x.fitness)[0]


def execute(iterations, noAnts, n, alpha, beta, q0, rho):
    trace={}
    sol = copy.deepcopy(epoca(noAnts, n, trace, alpha, beta, q0, rho))
    bestSol = copy.deepcopy(sol)

    for _ in range(iterations):
        sol = copy.deepcopy(epoca(noAnts, n, trace, alpha, beta, q0, rho))
        if sol.fitness < bestSol.fitness:
            bestSol = copy.deepcopy(sol)

    return bestSol


def main():
    n = 4
    iterations = 100
    noAnts = 3
    alpha = 1.9
    beta = 0.9
    rho = 0.05
    q0 = 0.5

    print(execute(iterations, noAnts, n, alpha, beta, q0, rho))


main()