# -*- coding: utf-8 -*-

__author__ = 'Minmin Chen'
__date__ = '06/29/2018, 1:17 PM'

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='Songti.ttc', size=8)


class FeatureCorr():
    def __init__(self, Address, YearRange, Threshold, TargetFeature):
        self.Address = Address
        self.YearRange = YearRange
        self.threshold = Threshold
        self.TargetFeature = TargetFeature
        pass

    def DataPre(self):

        # -------------Data Preprocessing------------------------------------------------------------
        Data = pd.read_csv(self.Address).dropna(axis=1, how='all')
        Data = Data.fillna(0)  # fill nan with 0

        # select data by year from 2007 to 2015
        self.YearData = []
        for year in range(self.YearRange[0], self.YearRange[1]):
            Data1 = Data[Data['年份'] == year]
            self.YearData.append(Data1)

    def FeatureFilter(self):

        # --------------Correlation Calculation------------------------------------------------------
        # calculate all correlation value from 2007 to 2015
        YearCorr = []
        for i in range(len(self.YearData)):
            corr = self.YearData[i].corr(method='spearman')  # correlation between migrant and other features
            YearCorr.append(corr)

        # find all features that have correlation with '流动人口' larger than threshold
        FeatureList = []
        for df in YearCorr:
            FeatureList.append(df.columns[(abs(corr.loc[self.TargetFeature]) > self.threshold[0]) & (
                    abs(corr.loc[self.TargetFeature]) < self.threshold[1])].values.tolist())

        # find intersection between multiple list
        Feature = list(set(FeatureList[0]).intersection(*FeatureList))

        # select value corresponding to certain feature from comprehensive correlation dataframe
        self.NewCorr = []
        for df in YearCorr:
            self.NewCorr.append(df[Feature].loc[self.TargetFeature][
                                    np.isfinite(
                                        df[Feature].loc[
                                            self.TargetFeature])])  # .drop([TargetFeature])) # drop nan value

        self.LeftFeature = list(self.NewCorr[0].index)

    def MeanStdOutput(self):

        # all corr corresponding to features
        self.MigrantAll = {}
        for i, feature in enumerate(self.LeftFeature):
            all1 = []
            for df in self.NewCorr:
                all1.append(df[i])
            key = feature
            value = all1
            self.MigrantAll[key] = value

        # mean of corr
        MeanDict = {}
        for key, value in self.MigrantAll.items():
            Key = key
            Value = np.mean(value)
            MeanDict[Key] = Value

        # standard deviation of corr
        StdDict = {}
        for key, value in self.MigrantAll.items():
            Key = key
            Value = np.std(value)
            StdDict[Key] = Value

        # output
        AllDF = pd.DataFrame([MeanDict, StdDict]).T
        AllDF.to_csv('关联系数导出表.csv', header=['均值(cor)', '标准差(cor)'])

        # --------------------Plot--------------------------------------------------------------

    def PlotKernelTime(self):
        # auto generate numbers
        NewNum = []
        for i in range(len(self.LeftFeature)):
            if i % 10 == 0:
                NewNum.append(i)
            else:
                pass

        if len(self.LeftFeature) - 1 == NewNum[-1]:
            pass
        else:
            NewNum.append(len(self.LeftFeature) - 1)

        # plot kernel density and time series
        for n in range(len(NewNum) - 1):
            # plt.figure(1)
            name = self.LeftFeature[NewNum[n]:NewNum[n + 1]]  # feature names
            ListPart = [value for key, value in self.MigrantAll.items()][NewNum[n]:NewNum[n + 1]]  # list slice of corr
            time = np.array([x for x in range(self.YearRange[0], self.YearRange[1])])

            fig, axes = plt.subplots(len(name), 2)  # fig use for saving, axes use for editing, array, not matrix
            if len(axes.shape) == 1:
                axes = axes.reshape((1, -1))  # only one list left, reshape to 1 row n columns
            # plot kernel density function
            for i, ax in enumerate(axes[:, 0].flatten()):  # .flatten() is like .reshape(), since axes can be n*n matrix
                # ax.set_title([i])

                ax.set_xlim(-1, 1)
                ax.set_ylim(0, 6)
                sns.kdeplot(ListPart[i], ax=ax, shade=True, color=plt.cm.Paired(i / 10.),
                            label=name[i])  # plot on ax(object)
                ax.legend(prop=font)

            # plot time series
            for i, ax in enumerate(axes[:, 1].flatten()):
                # ax.set_title([i])
                ax.plot(time, ListPart[i], color=plt.cm.Paired(i / 10.))  # ,label=name[i]
                # ax.text()

            axes[0, 0].set_title(u'与' + self.TargetFeature + '指标 各年度相关系数分布图',
                                 fontproperties=font)  # set title for the first column
            axes[0, 1].set_title(u'与' + self.TargetFeature + '指标 各年度相关系数时序图',
                                 fontproperties=font)  # set title for the second column

            plt.savefig('MeanStd' + str(NewNum[n]) + '.png')

    def RunAll(self):
        self.DataPre()
        self.FeatureFilter()
        self.MeanStdOutput()
        self.PlotKernelTime()


#####################################################################################################


###########Input#####################################################################################
# input: file, threshold, target feature
'''Address = '0605钢铁侠更新第一部分C.csv'  # Address, str
YearRange = [2007, 2017]  # YearRange, list
 Threshold = [0.8, 0.99]  # Threshold, int
TargetFeature = '流动人口'  # TargetFeature, str
'''

'''Example = FeatureCorr('0605钢铁侠更新第一部分C.csv', [2007, 2017], [0.8, 0.99], '流动人口')
Example.RunAll()'''
