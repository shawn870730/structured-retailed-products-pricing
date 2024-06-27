### Structured Retail Products Pricing and Hedging

This project focuses on designing and implementing structured retail products (SRPs) with specific payoff structures, aimed at providing contingent returns based on the performance of underlying financial securities. Utilizing advanced financial models, the project involves deriving optimal contract parameters and developing robust risk management strategies through hedging.

### Key Components

1. **Black-Scholes Model Implementation (Constant Interest Rate, Constant Volatility):**
    - **Objective:** Develop a product that balances potential returns and risk mitigation.
    - **Data:** Historical price data for the S&P 500 index and the prevailing 3-year Treasury rate.
    - **Volatility Estimation:** Standard estimators for realized volatility using normal-distributed log returns.
    - **Model Formulation:** Calculate values for guaranteed minimum return (g) and maximum return cap (G) to ensure the investment’s value at maturity equals the initial capital.
    - **Risk Management:** Implement Delta-Hedging strategy and backtest from January 1, 2021, to December 31, 2023, to demonstrate the effectiveness of daily rebalancing.

2. **Formula Derivation and Contract Parameters:**
    - **Volatility Calculation:** Daily volatility (σ) using log returns, then annualized.
    - **Payoff Replication:** Long a call option at g and short a call option at G.
    - **Strike Price Calculation:** 
        - \( S_g = S_0(1 + g)^T \)
        - \( S_G = S_0(1 + G)^T \)
    - **Backtest Results:** Delta-Hedging strategy indicated potential effectiveness but revealed a final fund deficit, highlighting the need for enhanced risk management strategies.
