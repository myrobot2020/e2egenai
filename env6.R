Sys.setenv(RETICULATE_PYTHON = "C:/Users/ADMIN/miniconda3/envs/env6/python.exe")
library(reticulate)
use_condaenv("env6", required = TRUE)
# Confirm the configuration
py_config()