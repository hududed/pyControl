library(mlrMBO)

library(doMC)

setwd('C:\\Users\\UWAdmin\\line stuff\\fluence rds files\\c1')
opt.state=readRDS('opt.state.rds')


se=c()
means=c()

ii=c(1:70)
for (i in ii) {
  sev=opt.state[["opt.path"]][["env"]][["extra"]][[i]][["se"]]
  se=c(se,sev)
  response=opt.state[["opt.path"]][["env"]][["extra"]][[i]][["mean"]]
  means=c(means,response)
}

estimated=means
estimatedUpper=estimated+se
parameters=opt.state[["opt.path"]][["env"]][["path"]]
df=cbind(parameters,estimated,estimatedUpper)

write.csv(df,'data_final.csv',row.names = FALSE)
  

