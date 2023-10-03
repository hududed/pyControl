# %%
import os
os.environ['R_HOME'] = "C:/Program Files/R/R-4.3.1"

# %%
import rpy2.robjects as robjects
import os
import pandas as pd
from write_utils import create_new_path, write_data_files, duplicate_to_dataset

from pathlib import Path

# %%
#Define the file you want to read
path = Path(r'c:\\Users\\UWAdmin\\Desktop\\_pyControl\\campaigns')   #changes directory to new file created in next block. run this, run next block, update campaign_path, and run this again
campaign_path = path / "mlr3-campaigns"
if not os.path.exists(campaign_path):
    os.mkdir(campaign_path)
os.chdir(campaign_path)
os.getcwd()


# %%
#Create new file (only need to run this when starting a new series of experiments)
new_path = create_new_path(campaign_path, series=1, batch=True)
os.chdir(new_path)
write_data_files(new_path, series=1, nr_random_lines=6, \
    power_range=(300,2600), time_range=(2000, 28000), pressure_range=(60,800),passes_range=(1,2),defocus_range=(-2.5,0))

# set passes_range=(1,2) to set number of passes to 1 for all lines
# values here need to be the same as values in red ML section

# %%

# Define the mlr3 R functions
robjects.r('''
library(mlr3mbo)
library(mlr3)
library(mlr3learners)
library(bbotk)
library(data.table)
library(tibble)

# convert real pressure to values applicable to parameter space e.g. 60 psi -> 1 in parameter space
presToR <- function (x) {(x-50)/10}

# convert parameter space pressure to real pressure e.g. 1 -> 60 psi
presToExp <- function (x) {x*10+50}

load_archive <- function() {
  archive = readRDS("archive.rds")
  acq_function = readRDS("acqf.rds")
  acq_optimizer = readRDS("acqopt.rds")
  acq_function$surrogate$archive = archive
  return(list(archive, acq_function, acq_optimizer))
}

save_archive <- function(archive, acq_function, acq_optimizer) {
  saveRDS(archive, "archive.rds")
  saveRDS(acq_function, "acqf.rds")
  saveRDS(acq_optimizer, "acqopt.rds")
}

add_evals_to_archive <- function(archive, acq_function, acq_optimizer, data, q) {
  lie = data.table()
  liar = min
  acq_function$surrogate$update()
  acq_function$update()
  candidate = acq_optimizer$optimize()
  tmp_archive = archive$clone(deep = TRUE)
  acq_function$surrogate$archive = tmp_archive
  lie[, archive$cols_y := liar(archive$data[[archive$cols_y]])]
  candidate_new = candidate
  # loops through batch size q, e.g. q = 6 means batch of 6 lines
  for (i in seq_len(q)[-1L]) {
    tmp_archive$add_evals(xdt = candidate_new, xss_trafoed = transform_xdt_to_xss(candidate_new, tmp_archive$search_space), ydt = lie)
    acq_function$surrogate$update()
    acq_function$update()
    candidate_new = acq_optimizer$optimize()
    candidate = rbind(candidate, candidate_new)
  }
  # convert pressure back to real values
  candidate$pressure <- presToExp(candidate$pressure)
  candidate$defocus <- format(round(candidate$defocus, 2), nsmall = 2)
  save_archive(tmp_archive, acq_function, acq_optimizer)
  return(list(candidate, tmp_archive, acq_function))
}

experiment <- function(s) {
  if(s==1) {
    require(XML)
    set.seed(42)
    data = subset(data.table(read.csv("data.csv")), colClasses = c(NA, NA, NA, NA, "NULL", NA))
    data$pressure <- presToR(data$pressure)
    search_space = ps(power = p_int(lower = 100, upper = 2600),
                      time = p_int(lower = 2000, upper = 28000),
                      pressure = p_int(lower = 1, upper = 75, trafo = function(x) x * 10 + 50),
                      defocus = p_dbl(lower=-3.00, upper = 0.00))
    codomain = ps(resistance = p_dbl(tags = "minimize"))
    archive = Archive$new(search_space = search_space, codomain = codomain)
    archive$add_evals(xdt = data[, c("power", "time", "pressure", "defocus")], ydt = data[, "resistance"])
    print("Model archive so far: ")
    print(archive)
    surrogate = srlrn(lrn("regr.km", control = list(trace = FALSE)), archive = archive)
    acq_function = acqf("ei", surrogate = surrogate)
    acq_optimizer = acqo(opt("random_search", batch_size = 1000),
                         terminator = trm("evals", n_evals = 1000),
                         acq_function = acq_function)
    q = 6
    result = add_evals_to_archive(archive, acq_function, acq_optimizer, data, q)
  } else {
    result = load_archive()
    lines_to_keep <- 6 # should equal q
    num_lines <- countLines("data.csv")
    data <- as.data.table(read.csv("data.csv", header=FALSE, skip = num_lines-lines_to_keep))
    names(data) <- c('power','time','pressure','passes','defocus', 'ratio','resistance')
    data$pressure <- presToR(data$pressure)
    archive = result[[1]]
    acq_function = result[[2]]
    acq_optimizer = result[[3]]
    archive$add_evals(xdt = data[, c("power", "time", "pressure", "defocus")], ydt = data[,"resistance"])
    print("Model archive so far: ")
    print(archive)
    q = 6
    result = add_evals_to_archive(archive, acq_function, acq_optimizer, data, q)
  }
  candidate = result[[1]]
  archive = result[[2]]
  acq_function = result[[3]]
  x2 <- candidate[,c("power","time","pressure", "defocus")]
  x2 <- x2 %>% add_column(passes = 1, .after="pressure")
  print("New candidates: ")
  print(x2)
  print("Writing to data.csv ...")
  write.table(x2, file = "data.csv", sep = ",",
              append = TRUE, quote = FALSE,col.names = FALSE, row.names = FALSE)
  print("WRITE DONE")
}
''')

# %%
#Define running files
import pandas as pd

def _printing_line_count(data:pd.DataFrame, measured_value:str = 'resistance'):
    printed_lines_count = len(data['resistance'].dropna(inplace=False))
    return printed_lines_count

data = pd.read_csv("data.csv")
rsum = robjects.r['experiment']


NR_LINES_IN_SAMPLE = _printing_line_count(data)
_NR_PROPOSED_LINES = 6 # don't change this

NR_LINES_IN_SAMPLE
# %%

# Don't run this section on first sample (iteration) of new campaign

if len(data['resistance']) == NR_LINES_IN_SAMPLE:
    # print(len(d['resistance']))
    print(f"First batch proposal with {NR_LINES_IN_SAMPLE} lines to train")
    rsum((1))
    duplicate_to_dataset(nr_proposed_lines=_NR_PROPOSED_LINES, prepattern=False)

elif len(data['resistance']) < NR_LINES_IN_SAMPLE:
    print ("Not enough data points in dataset. Exiting.")
    exit()

else:
    print(f"Further batch proposals of {NR_LINES_IN_SAMPLE} lines")
    proposed = data['resistance'].iloc[-NR_LINES_IN_SAMPLE:]
    rsum((list(proposed)))
    duplicate_to_dataset(nr_proposed_lines=_NR_PROPOSED_LINES)
# %%
