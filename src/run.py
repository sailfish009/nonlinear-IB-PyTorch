from nonlinearIB import NonlinearIB
from utils import get_data
from utils import get_args
import torch
import os
import datetime
import numpy as np

torch.set_num_threads(16)

# Obtain the arguments
args = get_args()

# Obtain the data
trainset, validationset = get_data()

# Create the folders
os.makedirs(args.logs_dir) if not os.path.exists(args.logs_dir) else None
os.makedirs(args.figs_dir) if not os.path.exists(args.figs_dir) else None

# Train the network
nonlinear_IB = NonlinearIB(n_x = 784, n_y = 10, K = args.K, beta = args.beta,
    logvar_t = args.logvar_t, logvar_kde = args.logvar_kde, train_logvar_t = args.train_logvar_t)
nonlinear_IB.fit(trainset, validationset, n_epochs = args.n_epochs, learning_rate = args.learning_rate,
    learning_rate_drop = args.learning_rate_drop, learning_rate_steps = args.learning_rate_steps, gd_batch_size = args.sgd_batch_size,
    mi_batch_size = args.mi_batch_size, same_batch = args.same_batch, eval_rate = args.eval_rate,
    verbose = args.verbose, visualization = args.visualize, logs_dir = args.logs_dir, figs_dir = args.figs_dir)

# Save the network
name_base = "K-" + str(args.K) + "-B-" + str(round(args.beta,3)).replace('.', '-') \
    + "-Tr-" + str(bool(args.train_logvar_t)) + '-'
torch.save(nonlinear_IB, args.logs_dir + name_base + 'model')
