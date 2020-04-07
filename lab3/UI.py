from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from UI_MainWindow import Ui_MainWindow

import numpy as np
import sys
import threading
import copy
from math import sqrt
import matplotlib.pyplot as plt

from evolution import population, iteration, format_individual, individual, fitness
from hillclimbing import generateNextBestNeighbor

class UI(QtWidgets.QMainWindow):
    # Signals
    changed_individual = pyqtSignal(list)
    changed_individual_hc = pyqtSignal(list)
    threadevo_finished = pyqtSignal(str)
    threadhc_finished = pyqtSignal(str)
    threadstat_finished = pyqtSignal(list)

    # Threads
    ThreadEVO = None
    ThreadHC = None
    ThreadStatistics = None

    # Thread Flags
    threadevo_interrupt = False
    threadhc_interrupt = False
    
    # Result of preious Evolutionary alg
    evo_res = None

    # Statistics
    fitness_array = None

    def __init__(self):
        super(UI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonShowStats.setEnabled(False)

        self.changed_individual.connect(self.changeIndividual)
        self.changed_individual_hc.connect(self.changeIndividualHC)
        self.threadevo_finished.connect(self.threadEvoFinished)
        self.threadhc_finished.connect(self.threadHCFinished)
        self.threadstat_finished.connect(self.statisticsFinished)

        self.ui.buttonStart.clicked.connect(self.onClickButtonStart)
        self.ui.buttonStop.clicked.connect(self.onClickButtonStop)
        self.ui.startHCdef.clicked.connect(self.onClickButtonStartHCdef)
        self.ui.startHCevo.clicked.connect(self.onClickButtonStartHCevo)
        self.ui.buttonStopHC.clicked.connect(self.onClickButtonStopHC)
        self.ui.buttonStatistics.clicked.connect(self.onClickButtonStatistics)
        self.ui.buttonShowStats.clicked.connect(self.showStatistics)


    def onClickButtonStart(self):
        individualsize = int(self.ui.individualSize.text())
        noIterations = int(self.ui.noIterations.text())
        probability = float(self.ui.mutationProb.text())
        popsize = int(self.ui.populationSize.text())
        reprate = float(self.ui.reproductionRate.text())
        #evolutionary(noIterations, individualsize, popsize, probability, reprate, self.ui)

        self.ThreadEVO = threading.Thread(target=self.evolutionaryThread, \
        args=[noIterations, individualsize, popsize, probability, reprate])

        self.ui.statusEvo.setText("Running")
        self.threadevo_interrupt = False
        self.ui.buttonStart.setEnabled(False)
        self.ThreadEVO.start()


    def onClickButtonStop(self):
        self.threadevo_interrupt = True


    def onClickButtonStartHCdef(self):
        individualsize = int(self.ui.individualSizeHC.text())

        self.ThreadHC = threading.Thread(target=self.hillClimbingThread, \
        args=[individualsize])

        self.ui.statusHC.setText("Running")
        self.threadhc_interrupt = False
        self.ui.startHCdef.setEnabled(False)
        self.ui.startHCevo.setEnabled(False)

        self.ThreadHC.start()


    def onClickButtonStartHCevo(self):
        if self.evo_res is None:
            self.ui.statusHC.setText("ERROR: No evolution result, run evolution")
            return

        self.ThreadHC = threading.Thread(target=self.hillClimbingThread, args=[None])

        self.ui.statusHC.setText("Running")
        self.threadhc_interrupt = False
        self.ui.startHCdef.setEnabled(False)
        self.ui.startHCevo.setEnabled(False)

        self.ThreadHC.start()


    def onClickButtonStopHC(self):
        self.threadhc_interrupt = True


    def changeIndividual(self, l):
        self.ui.displayCurrent.setText(format_individual(l[1]))
        self.ui.lineFitness.setText(str(l[0]))
        self.evo_res = l


    def changeIndividualHC(self, l):
        self.ui.displayCurrentHC.setText(format_individual(l[1]))
        self.ui.lineFitnessHC.setText(str(l[0]))


    def threadEvoFinished(self, status):
        self.ui.statusEvo.setText(status)
        self.ui.buttonStart.setEnabled(True)


    def threadHCFinished(self, status):
        self.ui.statusHC.setText(status)
        self.ui.startHCdef.setEnabled(True)
        self.ui.startHCevo.setEnabled(True)


    def evolutionaryThread(self, noIterations, individualsize, popsize, probability, reprate):
        p = population(popsize, individualsize)

        cur = p[0]
        for _ in range(noIterations):
            if self.threadevo_interrupt is True:
                self.threadevo_finished.emit("Stopped")
                return

            p = iteration(p, probability, reprate)
            
            if p[0][0] == 0:
                break

            if cur != p[0]:
                cur = p[0]
                self.changed_individual.emit(cur)

        graded = sorted(p, key = lambda x: x[0])
        
        best = graded[0]

        self.changed_individual.emit(best)
        self.threadevo_finished.emit("Finished")


    def hillClimbingThread(self, size):

        if size is None:
            start = copy.deepcopy(self.evo_res[1])
        else:
            start = individual(size)

        (curFit, curNode) = generateNextBestNeighbor(start)

        while True:
            if self.threadhc_interrupt is True:
                self.threadhc_finished.emit("Stopped")
                return

            if curFit == 0:
                self.changed_individual_hc.emit([fitness(curNode), curNode])
                self.threadhc_finished.emit("Finished")
                return curNode

            (newFit, newNode) = generateNextBestNeighbor(curNode)

            self.changed_individual_hc.emit([newFit, newNode])
            if newFit == curFit:
                self.threadhc_finished.emit("Finished")
                return newNode

            curFit = newFit
            curNode = newNode


    def statisticsFinished(self, array):
        self.fitness_array = array
        self.ui.buttonStatistics.setEnabled(True)
        self.ui.buttonShowStats.setEnabled(True)
        self.ui.buttonStatistics.setText("Recalculate Statistics")


    def calculateStatistics(self):
        fitness = list()

        for _ in range(30):
            fitness.append(self.statistics())

        self.threadstat_finished.emit(fitness)


    def onClickButtonStatistics(self):
        self.ui.buttonStatistics.setEnabled(False)
        self.ui.buttonShowStats.setEnabled(False)
        self.ui.buttonStatistics.setText("Calculating...")
        self.ThreadStatistics = threading.Thread(target=self.calculateStatistics)
        self.ThreadStatistics.start()


    def showStatistics(self):
        mean = np.mean(self.fitness_array)
        std = sqrt(np.var(self.fitness_array))

        plt.plot(self.fitness_array)
        plt.xlabel("mean: " + str(mean) + "; std deviation: " + str(std))
        plt.show()
        


    def statistics(self):
        """
        Statistics of the fitness function with: populationsize = 40, individualsize = 4,
        noiterations = 1000, mutationProb = reproductionRate = 0.5
        """

        p = population(40, 5)

        for _ in range(1000):
            p = iteration(p, 0.5, 0.5)
            
            if p[0][0] == 0:
                break

        return p[0][0]
