#1(a)
import yfinance as yf
import QuantLib as ql
import numpy as np
import statistics as st
from scipy.optimize import newton
from scipy.stats import multivariate_normal
from scipy.stats import norm
import pandas as pd

sp500 = yf.download('^SPX', start='2013-12-31',end='2023-12-31')['Close'].values
log_returns_sp500 = np.diff(np.log(sp500))

sigma = np.std(log_returns_sp500)
sigma=sigma*np.sqrt(252)
print("Sigma:", sigma)


S0= sp500[len(sp500)-1]
T=3
r=0.0401 #2024/01/02
#%%
#1(b)
import numpy as np
import scipy.stats as st
from scipy.optimize import minimize
def BS_Call(S0, K, T, sigma, r):
  N = st.norm.cdf
  d1 = (np.log(S0/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
  d2 = d1 - sigma* np.sqrt(T)
  return S0*N(d1)-np.exp(-r*T)*K*N(d2), N(d1)

def calculate_G(S0, T, sigma, r, g_values):
    G_values=[]
    for g in g_values:
        strike_g = S0*(1+g)**T
        call_g = BS_Call(S0, strike_g, T, sigma, r)[0]
        call_G = call_g- S0 + np.exp(-r*T) * (1+g)**T * S0
        initial_K = strike_g
        result = minimize(lambda K: abs(BS_Call(S0, K, T, sigma, r)[0] - call_G), initial_K)
        G=(result.x[0]/S0)**(1/T)-1
        G_values.append(G)
    return G_values

g_values=np.linspace(-0.2, 0, 21)
S0 = sp500[len(sp500)-1]
T = 3
L = 200000
sigma = 0.17
r = 0.0401

G_values = calculate_G(S0, T, sigma, r, g_values)
for g, G in zip(g_values, G_values):
    df = pd.DataFrame({'g': g_values, 'G': G_values})
    print(df)

#%%
#1(C)
def calculate_G_g0(S0, T, sigma, r, g_values):
    strike_g = S0*(1+g_values)**T
    call_g = BS_Call(S0, strike_g, T, sigma, r)[0]
    call_G = call_g- S0 + np.exp(-r*T) * (1+g)**T * S0
    initial_K = strike_g
    result = minimize(lambda K: abs(BS_Call(S0, K, T, sigma, r)[0] - call_G), initial_K)
    G_values=(result.x[0]/S0)**(1/T)-1
    return G_values

St = yf.download('^SPX', start='2021-01-01',end='2023-12-31')['Close'].values
sp500 = yf.download('^SPX', start='2013-12-31',end='2020-12-31')['Close'].values
log_returns_sp500 = np.diff(np.log(sp500))

sigma = np.std(log_returns_sp500)
sigma=sigma*np.sqrt(252)
S0= sp500[-1]
T=3
r=0.0017
n=1 #daily adjust
time=np.linspace(0,3,num=754, endpoint=True)
dt=1/252
L=200000

g_values=0
G_values = calculate_G_g0(S0, T, sigma, r, g_values)
S_G=S0*(1+G_values)**T
S_g=S0*(1+g_values)**T

def Delta_Hedge(St, S_G, S_g, dt, sigma, r, T):
    D0_g = BS_Call(S0, S_g, T, sigma, r)[1]
    D0_G = BS_Call(S0, S_G, T, sigma, r)[1]
    Fund = [L]
    Delta = [D0_g - D0_G]
    Bond = S_g/(1+r)**T * L/S0
    Bank = [L - (D0_g - D0_G) * S0 * L/S0 - Bond ]

    for i in range(1, 753):
        Fund = np.append(Fund,
                         Bank[i - 1] * np.exp(r * dt) + Delta[i - 1] * St[i - 1]*L/S0 + Bond )
        Delta = np.append(Delta,
                              BS_Call(St[i - 1], S_g, T - time[i], sigma, r)[1] - BS_Call(S0, S_G, T, sigma, r)[1])

        Bank = np.append(Bank, Fund[i] - Delta[i] * St[i - 1]*L/S0 - Bond)
    Fund_T = Bank[-1] * np.exp(r * dt) + Delta[-1] * St[-1]*L/S0 + S_g * L/S0
    return (Fund_T - max(min((1 + G_values) ** T * L, St[-1] / S0 * L), (1 + g_values) ** T * L),Delta)

results = pd.DataFrame({'Rebalance freq n':[1],'Balance':[Delta_Hedge(St, S_G, S_g, dt, sigma, r, T)]})

print(results)

#%%

