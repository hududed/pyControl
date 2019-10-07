#!/usr/bin/env Rscript

suppressWarnings({suppressMessages({
    library(mlrMBO)
    library(ggplot2)
})})

ps = makeParamSet(
  makeIntegerParam("power", lower = 10, upper = 5555),
  makeIntegerParam("time", lower = 500, upper = 20210),
  makeDiscreteParam("gas", values = c("Nitrogen","Air","Argon")),
  makeIntegerParam("pressure", lower = 0, upper = 100)
)

ctrl = makeMBOControl(y.name = "ratio")
ctrl = setMBOControlInfill(ctrl, opt = "focussearch", opt.focussearch.maxit = 10, opt.focussearch.points = 10000, crit = makeMBOInfillCritEI())

data = read.csv("C:\\Users\\labuser\\Desktop\\data_1\\Vivek\\2019-09-03\\tuning_data_KGO_GD_3.csv")

suppressMessages({opt.state = initSMBO(par.set = ps, design = data, control = ctrl, minimize = FALSE, noisy = TRUE)})


cat("Proposed parameters:\n")
prop = suppressWarnings({proposePoints(opt.state)})
print(prop$prop.points)
cat("Expected value (upper bound):\n")
cat(paste(prop$crit.components$mean, " (", prop$crit.components$mean + prop$crit.components$se, ")\n", sep = ""))

#updateSMBO(opt.state, x = data.frame(power = 100, time = 100), y = 2)
