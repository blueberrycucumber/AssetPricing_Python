from scipy.stats import norm
from math import log, sqrt, exp
import matplotlib.pyplot as plt

# # 1、利率上限/下限单元定价
def caplet_value(tk, tk1, Fk, RK, L, sigmak, Pk1, cap=True):
    # Parameters instruction
    # tk: float,在tk时刻观察tk和tk+1之间的LIBOR利率Rk
    # tk1: float,期权的收益发生在tk+1时刻
    # Fk: float,在0时刻上观察到的tk和tk+1之间的远期利率
    # RK: float,上限/下限利率
    # L: float,利率上限/下限合约本金
    # Pk1：float,贴现因子,将发生在tk+1时刻的收益贴现到0时刻
    # cap:T or F,利率上限or利率下限
    Fk = float(Fk)
    deltak = tk1-tk
    d1 = (log(Fk / RK) + (0.5 * sigmak ** 2) * tk) / (sigmak * sqrt(tk))
    d2 = d1 - sigmak * sqrt(tk)
    if cap:
        value = L * deltak * Pk1 * (Fk * norm.cdf(d1) - RK * norm.cdf(d2))
    else:
        value = L * deltak * Pk1 * (RK * norm.cdf(-d2) - Fk * norm.cdf(-d1))
    return value


# # 2、利率双限单元定价
def collar_caplet_value(tk, tk1, Fk, RK_c, RK_f, L, sigmak, Pk1):
    # Parameters instruction
    # tk: float,在tk时刻观察tk和tk+1之间的LIBOR利率Rk
    # tk1: float,期权的收益发生在tk+1时刻
    # Fk: float,在0时刻上观察到的tk和tk+1之间的远期利率
    # RK_c: float,上限利率
    # RK_f: float,下限利率
    # L: float,利率双限合约本金
    # sigmak：float,在0时刻上观察到的tk和tk+1之间的远期利率的波动率
    # Pk1：float,贴现因子,将发生在tk+1时刻的收益贴现到0时刻
    value = caplet_value(tk, tk1, Fk, RK_c, L, sigmak, Pk1, cap=True) - caplet_value(tk, tk1, Fk, RK_f, L, sigmak, Pk1, cap=False)
    return value


# # 3、利率上限/下限合约定价
def contract_value(t, F, RK, L, sigma, P, cap=True):
    # Parameters instruction
    # t: list, t1, t2, t3, ..., tn+1
    # F: list, F1, F2, F3, ..., Fn
    # RK: float, 上限/下限利率
    # L: float, 利率上限/下限合约本金
    # sigma：list, sigma1, sigma2, ..., sigman
    # P：list, P2, P3, ..., Pn+1
    # cap: T or F,利率上限or利率下限
    n = len(t) - 1
    sum = 0
    for i in range(n):
        sum = sum + caplet_value(t[i], t[i+1], F[i], RK, L, sigma[i], P[i], cap)
    return sum


# # 4、利率双限合约定价
def collar_value(t, F, RK_c, RK_f, L, sigma, P):
    # Parameters instruction
    # t: list, t1, t2, t3, ..., tn+1
    # F: list, F1, F2, F3, ..., Fn
    # RK_c: float,上限利率
    # RK_f: float,下限利率
    # L: float, 利率双限合约本金
    # sigma：list, sigma1, sigma2, ..., sigman
    # P：list, P2, P3, ..., Pn+1
    n = len(t) - 1
    sum = 0
    for i in range(n):
        sum = sum + collar_caplet_value(t[i], t[i + 1], F[i], RK_c, RK_f, L, sigma[i], P[i])
    return sum


# #——————————————————————————————————————————————————————————————
# # 实例检验
# 例29-3 利率上限单元定价
tk = 1.0
tk1 = 1.25
Fk = 0.07
RK = 0.08
L = 10
sigmak = 0.2
Pk1 = 0.9169
price = caplet_value(tk, tk1, Fk, RK, L, sigmak, Pk1, cap=True)
print(price)   # 0.00516


# 练习题29.5 利率上限单元定价
tk = 1.25
tk1 = 1.5
Fk = 0.12
RK = 0.13
L = 1000
sigmak = 0.12
Pk1 = exp(-0.115*1.5)
price = caplet_value(tk, tk1, Fk, RK, L, sigmak, Pk1, cap=True)
print(price)   # 0.5972


# 练习题29.22 利率上限单元定价
tk = 0.75
tk1 = 1.0
Fk = 0.08
RK = 0.08
L = 1000
sigmak = 0.15
Pk1 = exp(-0.075*1.0)
price = caplet_value(tk, tk1, Fk, RK, L, sigmak, Pk1, cap=True)
print(price)   # 0.96


# # 练习题29.24 利率双限合约定价
# t = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0]
# F = [0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.06]
# sigma = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
# P = [0.9714164644666048, 0.957432554090967, 0.9436499474367985, 0.9300657466602784, 0.9166770956331523, 0.9034811793422207, 0.8904752232974726, 0.8776564929487385, 0.8650222931107413, 0.8525699673964233, 0.8402968976584314, 0.828200503438642, 0.8162782414256099, 0.8045276049198279, 0.7929461233066837, 0.7815313615370046, 0.7702809196150792, 0.759192432094049, 0.7482635675785652]
# RK_c = 0.07
# RK_f = 0.05
# L = 100
# price = collar_value(t, F, RK_c, RK_f, L, sigma, P)
# price2 = contract_value(t, F, RK_c, L, sigma, P, cap=True)
# price3 = contract_value(t, F, RK_f, L, sigma, P, cap=False)
# print(price)   # 双限合约价格：0.398
# print(price2)  # 上限合约价格：1.514
# print(price3)  # 下限合约价格：1.116


# #——————————————————————————————————————————————————————————————
# 给本组设计的合约定价
t = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
F = [0.02094206, 0.023600826, 0.02592609, 0.024529337, 0.025367757]
sigma = [0.047936755, 0.036596858, 0.03554074, 0.036129492, 0.036705145]
P = [0.980195157, 0.968763349, 0.956365935, 0.944778539, 0.932945176]
RK_c = 0.024
RK_f = 0.023
L = 1000
price = collar_value(t, F, RK_c, RK_f, L, sigma, P)
price2 = contract_value(t, F, RK_c, L, sigma, P, cap=True)
price3 = contract_value(t, F, RK_f, L, sigma, P, cap=False)
print(price)   # 双限合约价格：0.9876
print(price2)  # 上限合约价格：2.0962
print(price3)  # 下限合约价格：1.1086

# #——————————————————————————————————————————————————————————————
# # 敏感性检验
# 远期利率(F)变化时，利率期权合约价格：
F1 = []
pricex = []
pricex2 = []
pricex3 = []
n = len(F)
for j in range(-20, 21):
    for i in range(n):
        F1.append(F[i]+F[i]*j/100)
    pricex.append(collar_value(t, F1, RK_c, RK_f, L, sigma, P))
    pricex2.append(contract_value(t, F1, RK_c, L, sigma, P, cap=True))
    pricex3.append(contract_value(t, F1, RK_f, L, sigma, P, cap=False))
    F1 = []

percentage = range(-20, 21)
fig = plt.figure(figsize=(15, 8))
plt.plot(percentage, pricex, label='collar')
plt.plot(percentage, pricex2, label='cap')
plt.plot(percentage, pricex3, label='floor')
plt.title("change in option value over forward rate")
plt.xlabel("percentage change in the forward rate (%)")
plt.ylabel("option value")
plt.grid()
plt.legend()
plt.legend(fontsize=18)
plt.tick_params(labelsize=15)
plt.show()

# 当远期利率波动率(sigma)变化时，利率期权合约价格：
sigma1 = []
sigmax = []
pricex = []
pricex2 = []
pricex3 = []
n = len(F)
for j in range(-90, 91):
    for i in range(n):
        sigma1.append(sigma[i]+sigma[i]*j/100)
    pricex.append(collar_value(t, F, RK_c, RK_f, L, sigma1, P))
    pricex2.append(contract_value(t, F, RK_c, L, sigma1, P, cap=True))
    pricex3.append(contract_value(t, F, RK_f, L, sigma1, P, cap=False))
    sigma1 = []

percentage = range(-90, 91)
fig = plt.figure(figsize=(15, 8))
plt.plot(percentage, pricex, label='collar')
plt.plot(percentage, pricex2, label='cap')
plt.plot(percentage, pricex3, label='floor')
plt.title("change in option value over forward rate")
plt.xlabel("percentage change in the volatility of the forward rate (%)")
plt.ylabel("option value")
plt.grid()
plt.legend()
plt.legend(fontsize=18)
plt.tick_params(labelsize=15)
plt.show()

# #——————————————————————————————————————————————————————————————
# 探究利率上下限变化与合约价格的关系
# 当利率上限、下限变化时，利率期权合约价格：
RK_c1 = RK_c
RK_f1 = RK_f
pricex = []
pricex2 = []
pricex3 = []
n = len(F)
for j in range(-10, 11):
    for i in range(n):
        RK_c1 = RK_c1 + RK_c1 * j / 100
        RK_f1 = RK_f1 + RK_f1 * j / 100
    pricex.append(collar_value(t, F, RK_c1, RK_f1, L, sigma, P))
    pricex2.append(contract_value(t, F, RK_c1, L, sigma, P, cap=True))
    pricex3.append(contract_value(t, F, RK_f1, L, sigma, P, cap=False))
    RK_c1 = RK_c
    RK_f1 = RK_f

percentage = range(-10, 11)
fig = plt.figure(figsize=(15, 8))
plt.plot(percentage, pricex, label='collar')
plt.plot(percentage, pricex2, label='cap')
plt.plot(percentage, pricex3, label='floor')
plt.title("change in option value over cap/floor")
plt.xlabel("percentage change in the cap/floor (%)")
plt.ylabel("option value")
plt.grid()
plt.legend()
plt.legend(fontsize=18)
plt.tick_params(labelsize=15)
plt.show()
