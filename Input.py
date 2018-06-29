from SpearmanCorrelation import FeatureCorr

Input = FeatureCorr('0605钢铁侠更新第一部分C.csv', [2007, 2017], [0.8, 0.99], '流动人口')
Input.RunAll()


'''Address = '0605钢铁侠更新第一部分C.csv'  # Address, str
YearRange = [2007, 2017]  # YearRange, list
 Threshold = [0.8, 0.99]  # Threshold, int
TargetFeature = '流动人口'  # TargetFeature, str
'''