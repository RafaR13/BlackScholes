# BlackScholes


Improvements / Variations:
- Stochastic Volatility: Standard BS assumes constant volatility. Heston Model implements stochastic volatility
add a second state variable (for volatility) and adjust your finite difference scheme to handle both the asset price and volatility dynamics.
- Jump Diffusion: add a jump term to the stock price process and adjust the boundary conditions and grid update logic to handle jumps.
- Local Volatility: Modify finite difference solver to use a volatility function that depends on both the asset price and time.
- Dividend Yield: Modify the drift term in the finite difference scheme to include the dividend yield.
- American Option: At each time step, take the maximum of the value from the finite difference solution and the intrinsic value.