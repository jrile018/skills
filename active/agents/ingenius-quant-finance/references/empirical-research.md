# Empirical Research

## Module contract

- **Purpose:** Design or review regression, time-series, volatility, factor, PCA, and data-driven finance analyses.
- **Load when:** The task uses observed data, estimated relationships, forecasts, latent factors, or ML evaluation.
- **Do not load when:** The task is a purely no-arbitrage derivation with no estimation.
- **Inputs:** Variables, timestamps, frequency, information set, transformations, estimation/evaluation windows, and claimed use.
- **Output invariant:** State transformations, assumptions, diagnostics, baseline, uncertainty, and a time-respecting evaluation.

## Workflow

1. Define response, predictors, units, timestamps, sampling frequency, and information available at each decision time.
2. Inspect missingness, transformations, corporate-action handling, selection, survivorship, and potential leakage.
3. Separate description, forecasting, causal inference, and trading claims. A fitted relation establishes none of the others automatically.
4. Check dependence and stationarity before interpreting standard errors or forecasts. Distinguish levels, returns, differences, and cointegrating combinations.
5. Fit a transparent baseline before adding lags, regularization, latent factors, nonlinear models, or ML.
6. Diagnose residual dependence, heteroskedasticity, influential observations, distributional misspecification, and parameter instability.
7. Evaluate chronologically with only prior information. Report uncertainty and compare with the baseline.

## Method checks

### Regression and time series

State rank and error assumptions for `y = X beta + error`; prefer QR or SVD to an explicit inverse in numerical work. Distinguish Gauss–Markov conditions from stronger normality assumptions. For ARMA/ARIMA, VAR, cointegration, or state-space work, state lag order, stability/root conditions, differencing, innovation assumptions, and selection criterion. Filtering is real-time; smoothing uses later observations.

### Volatility

Name the volatility quantity being estimated and do not transfer conclusions across realized measurements, conditional forecasts, and option-implied quantities. For GARCH-type models, check positivity, persistence, standardized residuals, and squared-residual dependence. Square-root-of-time scaling requires dependence assumptions. High-frequency sampling over a fixed horizon can sharpen volatility estimation without solving drift uncertainty.

### Factors and PCA

State covariance versus correlation input, demeaning/scaling, estimation window, retained dimensions, and out-of-sample stability. Require independent stability or economic evidence before interpreting a high-variance direction as a factor or strategy. For a tradable interpretation, include weight formation, execution delay, financing, leverage, costs, and changing loadings.

### Machine learning

Use train/validation/test separation that respects time, compare with simple models, and report overfitting and regime sensitivity. Course demonstrations of neural pricing approximations, implied-volatility prediction, or reinforcement-learning hedging are teaching examples—not independently validated profitability claims.

## Verification

Use rolling or expanding windows, naive baselines, residual plots/tests, parameter perturbations, reproducible transformations, and held-out periods. For backtests, reconstruct the contemporaneous asset universe and information set before interpreting performance.

## Advanced elective extensions

Use these sources to deepen a decision already owned by this module; they do not create new automatic activation routes.

- [MIT 14.384 Time Series Analysis](https://ocw.mit.edu/courses/14-384-time-series-analysis-fall-2013/) strengthens persistent/non-stationary process, VAR, frequency-domain, and structural-break analysis. For finance use, translate the method but do not transfer macroeconomic application conclusions.
- [MIT 14.387 Applied Econometrics: Mostly Harmless Big Data](https://ocw.mit.edu/courses/14-387-applied-econometrics-mostly-harmless-big-data-fall-2014/) strengthens matching, IV, differences-in-differences, regression discontinuity, dependence-valid standard errors, and high-dimensional analysis. Require an explicit identification argument before using causal language.
- [Stanford MS&E 448 Big Financial Data for Algorithmic Trading](https://web.stanford.edu/class/msande448/info.html) reinforces raw quote/order/trade data work, model plausibility, and realistic project evaluation. Its public page is historically dated and some teaching material is access-restricted.

When the requested output is an execution policy rather than an empirical test, hand off the estimated signal, uncertainty, timestamps, and evaluation result to `market-microstructure-execution`. When the requested output is an optimization formulation, hand off calibrated inputs and uncertainty to `robust-quant-optimization`.
