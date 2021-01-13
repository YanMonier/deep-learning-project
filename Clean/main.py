import time
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np
import scipy.sparse as sc
from scipy.stats import multivariate_normal
import cma
import utils.network
import utils.game
import sys
import os




def typedevice(tensor,typ,devi):
    return tensor.to(device=devi,dtype=typ)


def progtot():
    global dtype
    global mu
    CMA=cma.evolution_strategy
    sol,es=CMA.fmin2(utils.game.launch_scenarios,mu,0.01,options={'ftarget':-50000,'maxiter':10,'popsize':2})
    print(sol,es)
    return(es)

if __name__ == "__main__":
    torch.cuda.set_device(torch.device('cuda:0'))
    dtype = torch.long
    #dtype = torch.cuda.FloatTensor
    device = torch.device('cpu')
    #device= torch.device('cuda')
    env = gym.make('CarRacing-v0')
    try:
        W=np.load('W.npy',allow_pickle=True)
        print('loaded W')
    except FileNotFoundError:
        print('not found creating W')
        Nr,D=512,15
        W=sc.random(Nr,Nr,density=float(D/Nr))
        W=0.9/max(abs(np.linalg.eigvals(W.A)))*W
        W=(2*W-(W!=0))
        W=W.A
        np.save('W.npy',W)
    utils.network.dtype=dtype
    utils.game.dtype=dtype
    utils.network.W=W
    utils.network.device=device
    utils.game.device=device
    try :
        net = torch.load('model.pt')
        net.eval()
        print('loaded net')
    except FileNotFoundError:
        print('creating net')
        net=utils.network.initnet(0.9,dtype,W)
        torch.save(net, 'model.pt')
    try:
        mu=np.load('mu.npy',allow_pickle=True)
        print('loaded mu')
    except FileNotFoundError:
        print('not found creating mu')
        mu=np.zeros(3*1025)
        np.save('mu.npy',mu)
		
    utils.network.W=W
    #utils.game.env=env
    utils.game.net=net
    progtot()


