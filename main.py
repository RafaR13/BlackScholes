import numpy as np

# input variables
sig = 0.2
rate = 0.05
# mu = 0
strike = 100
expiration = 1
t = 0
nt = 36*(2**12)
max_S = 200
nS = 20 + 1


dt = 1/nt
min_S = 0
ds = (max_S - min_S)/(nS-1)


def calc_a(t,S):
    return 0.5 * dt * ((sig*S/ds)**2 - rate * S/ds)

def calc_b(t,S):
    return 1 - (rate + (sig*S/ds)**2) * dt

def calc_c(t,S):
    return 0.5 * dt * ((sig*S/ds)**2 + rate * S/ds)

if __name__ == '__main__':

    surface = []

    sol = []

    S = min_S

    while S <= max_S:
        sol.append(max(S - strike,0))
        S += ds

    surface.append(sol)

    t_i = 0
    while t + dt <= expiration:
        #print(t)
        t_i += 1
        t += dt

        new_sol = []

        S = min_S
        i = 0

        new_sol.append(0)

        while S + ds < max_S:
            S += ds
            i += 1
            new_sol.append(calc_a(t-dt, S) * surface[t_i-1][i-1] + calc_b(t-dt, S) * surface[t_i-1][i]  + calc_c(t-dt, S) * surface[t_i-1][i+1])

        new_sol.append(2*new_sol[i] - new_sol[i-1])

        surface.append(new_sol)
    #print(t)
    print(surface[-1][6:15])
    #for i in surface:
    #print(i[6:15])