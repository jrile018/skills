---
name: quant-research
description: Quantitative finance research, strategy validation, backtesting, and market analysis. Use for trading strategies, statistical testing, futures/options, and market data work.
---

When working on quantitative trading research:

Skepticism First:
- Assume overfitting until proven otherwise
- Flag if number of tested parameters exceeds sqrt(sample size)
- Never present a backtest without out-of-sample validation

Strategy Validation:
- Run permutation tests to detect p-hacking (reference: Bailey et al. CSCV framework)
- Report Sharpe ratios with confidence intervals, not point estimates
- Include transaction cost assumptions in all backtest results
- Separate alpha generation from risk management analysis

Market Data:
- Check for survivorship bias
- Handle corporate actions, splits, and roll logic for futures
- Use point-in-time data — never lookahead bias
- For futures: be explicit about contract specs, margins, and roll dates

Code Style:
- Prefer vectorized numpy/pandas over loops
- Use type hints for all function signatures
- Separate data loading, signal generation, and portfolio construction into distinct modules
