from rpy2.robjects.packages import importr

utils = importr('utils')
base = importr('base')
# import R packages
gg = importr('ggplot2')
mlr = importr('mlrMBO')
# in R, this is automatically loaded with `mlrMBO - here independently
ph = importr('ParamHelpers')  # for parameter setting
smoof = importr('smoof')  #


# set parameter bounds
ps = ph.makeParamSet(ph.makeIntegerParam("power", lower=10, upper=5555),
                     ph.makeIntegerParam("time", lower=500, upper=20210),
                     ph.makeDiscreteParam("gas", values=['Nitrogen', 'Air', 'Argon']),
                     ph.makeIntegerParam("pressure", lower=0, upper=100))
print(ps)

# define model acquaisiton function
ctrl = mlr.makeMBOControl(y_name='ratio')  # `.` in R is replaced with `_` in py
ctrl = mlr.setMBOControlInfill(ctrl, opt='focussearch', opt_focussearch_maxit=10,
                               opt_focussearch_points=10000,
                               crit=mlr.makeMBOInfillCritEI())
print(ctrl)

data = utils.read_csv("C:\\Users\\labuser\\Desktop\\data_1\\Vivek\\2019-09-03\\tuning_data_KGO_GD_3.csv")




