import argparse
from dataRetriever import DataRetriever
from blackScholes import BlackScholesFD

def main():
    parser = argparse.ArgumentParser(description="Simple Black-Scholes CLI App")
    parser.add_argument("ticker", type=str, help="Stock Ticker (e.g., AAPL, TSLA)")
    parser.add_argument("strike", type=float, help="Strike Price (e.g., 150)")
    parser.add_argument("expiry", type=str, help="Option Expiry Date (YYYY-MM-DD)")
    
    args = parser.parse_args()

    try:
        print("\nFetching market data...")
        retriever = DataRetriever(args.ticker, args.strike, args.expiry)
        retriever.fetch_data()
        stock_price, call_price, risk_free_rate, time_to_expiry = retriever.get_data()

        print(f"\nRetrieved data:")
        print(f"Current Stock Price: {stock_price:.2f}")
        print(f"Strike Price: {args.strike:.2f}")
        print(f"Call Option Price: {call_price:.2f}")
        print(f"Risk-Free Rate: {risk_free_rate*100:.2f}%")
        print(f"Time to Expiry: {time_to_expiry:.2f} years\n")

        print("Running Black-Scholes Finite Difference solver...")
        solver = BlackScholesFD(
            strike=args.strike,
            rate=risk_free_rate,
            sigma=0.2,  # TODO: implement
            T=time_to_expiry,
            S_max=2 * stock_price,  # set S_max dynamic
            nS=100  # TODO: change according to what accuracy we want
        )
        solver.solve()

        # Find the closest stock price index
        idx = (abs(solver.S_grid - stock_price)).argmin()
        option_price_fd = solver.surface[0, idx]

        print(f"\nFinite Difference Approximated Option Price: {option_price_fd:.2f}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
