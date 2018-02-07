import matplotlib.pyplot as plt
import parameterStudy
import eventPoints
import numpy as np
import platform
import os


class Plots:
    def __init__(self, ResultFile, MinValue, MaxValue, StartVehicle, xlabel):
        self.ResultFile = ResultFile
        self.MinValue = MinValue
        self.MaxValue = MaxValue
        self.StartVehicle = StartVehicle
        self.xlabel = xlabel
        
    def ShowPlots(self):
        #open file with event results
        
        cwd = os.getcwd()
        if('Windows' in platform.platform()):
            file = cwd + '\\' + self.ResultFile
        else:
            cwd = cwd.replace('\\', '/')
            file = cwd + '/' + self.ResultFile
        
        f = open(file, 'r')
        
        EndurancePar = []   #lists for values from file
        EnduranceTime = []
        EnduranceScore = []
        AutoXPar = []
        AutoXTime = []
        AutoXSccore = []
        SkidpadPar = []
        SkidpadTime = []
        SkidpadScore = []
        AccelPar = []
        AccelTime = []
        AccelScore = []
        EfficiencyPar = []
        EfficiencyTime = []
        EfficiencyScore = []
        OverallPar = []
        OverallScore = []
        
        #sort event results and save them in arrays
        for lines in f:
            if('Endurance' in lines):
                new = np.array(lines.split('|'))
                par = new[3]
                time = new[5]    #time in min
                score = new[7]
                EndurancePar.append(par)
                EnduranceTime.append(time)
                EnduranceScore.append(score)
            elif('AutoX' in lines):
                new = np.array(lines.split('|'))
                par = new[3]
                time = new[5]    #time in min
                score = new[7]
                AutoXPar.append(par)
                AutoXTime.append(time)
                AutoXSccore.append(score)
            elif('Skidpad' in lines):
                new = np.array(lines.split('|'))
                par = new[3]
                time = new[5]   #time in s
                score = new[7]
                SkidpadPar.append(par)
                SkidpadTime.append(time)
                SkidpadScore.append(score)
            elif('Acceleration' in lines):
                new = np.array(lines.split('|'))
                par = new[3]
                time = new[5]   #time in s
                score = new[7]
                AccelPar.append(par)
                AccelTime.append(time)
                AccelScore.append(score)
            elif('Efficiency' in lines):
                new = np.array(lines.split('|'))
                par = new[3]
                time = new[5]    #time in min
                score = new[7]
                EfficiencyPar.append(par)
                EfficiencyTime.append(time)
                EfficiencyScore.append(score)
            elif('Overall' in lines):
                new = np.array(lines.split('|'))
                par = new[3]
                score = new[7]
                OverallPar.append(par)
                OverallScore.append(score)

        #plot scored points over the parameters
        fig1 = plt.figure()
        ax = fig1.add_axes([0.1, 0.1, 0.6, 0.75])
        ax.axis([self.MinValue-50, self.MaxValue+100, 0, 700])
        ax.set_title(self.StartVehicle.CarName)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel('Scoring')
        ax.plot(EndurancePar, EnduranceScore, 'bo', label = 'Endurance')
        ax.plot(AutoXPar, AutoXSccore, 'rv', label = 'AutoX')
        ax.plot(SkidpadPar, SkidpadScore, 'g^', label = 'Skidpad')
        ax.plot(AccelPar, AccelScore, 'y<', label = 'Acceleration')
        ax.plot(EfficiencyPar, EfficiencyScore, 'c>', label = 'Efficiency')
        ax.plot(OverallPar, OverallScore, 'ks', label = 'Overall')
        ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)     
        ax.grid(True)
        
        #plot scored time on two axes over the parameters
        fig2 = plt.figure()
        ay = fig2.add_axes([0.1, 0.1, 0.55, 0.75])
        ay.axis([self.MinValue-50, self.MaxValue+100, 0, 35])
        ay.set_title(self.StartVehicle.CarName)
        ay.set_xlabel(self.xlabel)
        ay.set_ylabel('Scored time [min]')
        ay.plot(EndurancePar, EnduranceTime, 'bo', label = 'Endurance/\nEfficiency [min]')
        ay.plot(AutoXPar, AutoXTime, 'rv', label = 'AutoX [min]')
        ay.legend(bbox_to_anchor=(1.1, 1), loc=2, borderaxespad=0.)
        ay1 = ay.twinx()
        ay1.axis([self.MinValue-50, self.MaxValue+100, 0, 40])
        ay1.set_ylabel('Scored time [s]')
        ay1.plot(SkidpadPar, SkidpadTime, 'g^', label = 'Skidpad [s]')
        ay1.plot(AccelPar, AccelTime, 'y<', label = 'Acceleration [s]')
        ay1.legend(bbox_to_anchor=(1.1, 0.8), loc=2, borderaxespad=0.)      
        ay.grid(True)
        
        plt.show()

        