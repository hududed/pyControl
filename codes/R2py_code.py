from rpy2.robjects.packages import importr

### import R packages ###
gg = importr('ggplot2')
mlr = importr('mlrMBO')
# in R, this is automatically loaded with `mlrMBO - here independently
ph = importr('ParamHelpers')  # for parameter setting
smoof = importr('smoof')  #

ps = ph.makeParamSet(ph.makeIntegerParam("power", lower=10, upper=5555),
                     ph.makeIntegerParam("time", lower=500, upper=20210),
                     ph.makeDiscreteParam("gas", values=['Nitrogen', 'Air', 'Argon']),
                     ph.makeIntegerParam("pressure", lower=0, upper=100))
print(ps)
