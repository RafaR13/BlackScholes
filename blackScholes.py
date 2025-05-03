import numpy as np

class BlackScholesFD:
    def __init__(self, strike=100, rate=0.05, sigma=0.2, T=0, S_max=200, S_min=0, nS=21, nt=36*(2**12), call=True):
        self.call = call # true for call, false for put
        self.strike = strike
        self.rate = rate
        self.sigma = sigma
        self.T = T
        
        self.S_max = S_max
        self.S_min = S_min
        self.nS = nS
        self.nt = nt
        
        self.dS = (S_max - S_min) / (nS - 1)
        self.dt = 1 / nt
        
        # Stock price and time grids
        self.S_grid = np.linspace(0, S_max, nS+1)
        self.time_grid = np.linspace(0, T, nt+1)

        # Initialize solution matrix: rows = time, cols = stock prices
        self.surface = np.zeros((nt+1, nS+1))

        # Set terminal condition (payoff at expiry)
        self.surface[-1] = np.maximum(self.S_grid - self.strike, 0) if call else np.maximum(self.strike - self.S_grid, 0)

        # Boundary conditions
        self.surface[:, 0] = 0  # Call option worthless if S=0
        self.surface[:, -1] = S_max - self.strike * np.exp(-self.rate * (T - self.time_grid))  # Max S
        
    def solve(self):
        for j in reversed(range(self.nt)):
            for i in range(1,self. nS):
                s = self.S_grid[i]

                a = self.calc_a(s)
                b = self.calc_b(s)
                c = self.calc_c(s)

                self.surface[j, i] = ( a * self.surface[j+1, i-1] ) + \
                        ( b * self.surface[j+1, i] ) + \
                        ( c * self.surface[j+1, i+1] )

            # Boundary conditions
            self.surface[j, 0] = 0 if self.call else self.strike * np.exp(-self.rate * (self.T - j * self.dt))
            self.surface[j, -1] = self.S_max - self.strike * np.exp(-self.rate * (self.T - j*self.dt)) if self.call else 0
            #self.surface[j, -1] = 2 * self.surface[j, -2] - self.surface[j, -3]
    
    def calc_a(self, s):
        return 0.5 * self.dt * ((self.sigma * s / self.dS)**2 - self.rate * s / self.dS)

    def calc_b(self, s):
        return 1 - (self.rate + (self.sigma*s/self.dS)**2) * self.dt

    def calc_c(self, s):
        return 0.5 * self.dt * ((self.sigma*s/self.dS)**2 + self.rate * s/self.dS)
    
if __name__ == '__main__':
    bs_fd = BlackScholesFD()
    bs_fd.solve()
    print(bs_fd.surface[0][6:15])