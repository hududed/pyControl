# %%
import os

os.environ["R_HOME"] = "C:/Program Files/R/R-4.3.1"

# %%
import rpy2.robjects as robjects
import os
import pandas as pd
from write_utils import (
    create_new_path,
    write_data_files,
    write_laser_data_files,
    duplicate_to_dataset,
)

from pathlib import Path

# %%
# Define the file you want to read
path = Path(
    r"c:\\Users\\UWAdmin\\Desktop\\_pyControl\\campaigns"
)  # changes directory to new file created in next block. run this, run next block, update campaign_path, and run this again
campaign_path = path / "mlr3-campaigns"
if not os.path.exists(campaign_path):
    os.mkdir(campaign_path)
os.chdir(campaign_path)
os.getcwd()


# %%
# Create new file (only need to run this when starting a new series of experiments)
new_path = create_new_path(campaign_path, series=1, batch=True)
os.chdir(new_path)
write_data_files(
    campaign_path,
    series=1,
    nr_random_lines=4,
    param1_range=(1, 20),
    param2_range=(1, 10),
    param3_range=(1, 100),
)

# write_laser_data_files(new_path, series=1, nr_random_lines=6, \
#     power_range=(300,2600), time_range=(2000, 28000), pressure_range=(60,800),passes_range=(1,2),defocus_range=(-2.5,0))

# set passes_range=(1,2) to set number of passes to 1 for all lines
# values here need to be the same as values in red ML section

# %%

# Define the mlr3 R functions
robjects.r(
    """
library(mlr3mbo)
library(mlr3)
library(mlr3learners)
library(bbotk)
library(data.table)
library(tibble)
library(R.utils)

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

update_and_optimize <- function(acq_function, acq_optimizer, tmp_archive, candidate_new, lie) {
  acq_function$surrogate$update()
  acq_function$update()
  tmp_archive$add_evals(xdt = candidate_new, xss_trafoed = transform_xdt_to_xss(candidate_new, tmp_archive$search_space), ydt = lie)
  candidate_new = acq_optimizer$optimize()
  return(candidate_new)
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
  # loops through batch size q, e.g. q = 4 -> batch of 4
  for (i in seq_len(q)[-1L]) {
    candidate_new = update_and_optimize(acq_function, acq_optimizer, tmp_archive, candidate_new, lie)
    candidate = rbind(candidate, candidate_new)
  }
  candidate_new = update_and_optimize(acq_function, acq_optimizer, tmp_archive, candidate_new, lie)
  
  save_archive(archive, acq_function, acq_optimizer)
  return(list(candidate, archive, acq_function))
}

experiment <- function(s) {
  if(s==1) { # create init model, and propose first candidates for evaluation
    require(XML)
    set.seed(42)
    data = subset(data.table(read.csv("data.csv")), colClasses = c(NA, NA, NA, NA, "NULL", NA))
    search_space = ps(param1 = p_int(lower = 1, upper = 10),
                      param2 = p_int(lower = 1, upper = 10),
                      param3 = p_int(lower = 1, upper = 100))
    codomain = ps(output = p_dbl(tags = "maximize"))
    archive = Archive$new(search_space = search_space, codomain = codomain)
    archive$add_evals(xdt = data[, c("param1", "param2", "param3")], ydt = data[, "output"])
    print("Model archive so far: ")
    print(archive)
    surrogate = srlrn(lrn("regr.km", control = list(trace = FALSE, nugget.stability=1e-8)), archive = archive)
    acq_function = acqf("ei", surrogate = surrogate)
    acq_optimizer = acqo(opt("random_search", batch_size = 1000),
                         terminator = trm("evals", n_evals = 1000),
                         acq_function = acq_function)
    q = 4
    result = add_evals_to_archive(archive, acq_function, acq_optimizer, data, q)

  } else { # update archive, propose further candidates for evaluation
    result = load_archive()
    lines_to_keep <- 4 # should equal q
    num_lines <- countLines("data.csv")
    data <- as.data.table(read.csv("data.csv", header=FALSE, skip = num_lines-lines_to_keep))
    names(data) <- c('param1','param2','param3','output')
    print("New data: ")
    print(data)
           
    archive = result[[1]]
    acq_function = result[[2]]
    acq_optimizer = result[[3]]
    print(archive)

    archive$add_evals(xdt = data[, c("param1", "param2", "param3")], ydt = data[,"output"])
    print("Model archive so far: ")
    print(archive)
    q = 4
    result = add_evals_to_archive(archive, acq_function, acq_optimizer, data, q)
  }
  candidate = result[[1]]
  archive = result[[2]]
  acq_function = result[[3]]
  x2 <- candidate[,c("param1","param2","param3")]
           
  print("New candidates: ")
  print(x2)
  print("New archive: ")
  print(archive)

  print("Writing to data.csv ...")
  write.table(x2, file = "data.csv", sep = ",",
              append = TRUE, quote = FALSE,col.names = FALSE, row.names = FALSE)
  print("WRITE DONE")
}
"""
)

# %%


def _printing_line_count(data: pd.DataFrame, output: str):
    printed_lines_count = len(data[output].dropna(inplace=False))
    return printed_lines_count


data = pd.read_csv("data.csv")
rsum = robjects.r["experiment"]

OUTPUT = "output"
actual_nr_lines = _printing_line_count(data, output=OUTPUT)
_NR_PROPOSED_LINES = 4  # don't change this

actual_nr_lines
# %%

# Don't run this section on first sample (iteration) of new campaign

if actual_nr_lines == _NR_PROPOSED_LINES:
    # print(len(d['resistance']))
    print(f"First batch proposal with {_NR_PROPOSED_LINES} lines to train")
    rsum((1))
    # duplicate_to_dataset(nr_proposed_lines=_NR_PROPOSED_LINES, prepattern=False)

elif actual_nr_lines < _NR_PROPOSED_LINES:
    print("Not enough data points in dataset. Please complete evaluation.")
    # exit()

else:
    print(f"Further batch proposals of {_NR_PROPOSED_LINES} lines")
    proposed = data[OUTPUT].iloc[-_NR_PROPOSED_LINES:]
    # print(proposed)
    rsum((2))
    # duplicate_to_dataset(nr_proposed_lines=_NR_PROPOSED_LINES)
# %%
