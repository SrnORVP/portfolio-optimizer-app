This is a project for data app using Python (SciPy, NumPy and Pandas), and Javascript (Svelte).
An containerized (Docker) example is hosted using Google Cloud Service (Google Cloud Run). The hosted version is restricted (in terms of number of runs, stock codes and precisions) to provided an example with reduced computation load.

The project itself performs financial asset allocation and portfolio optimization using Monte Carlo simulation. The business logic (written in Python) includes the following steps:
- Obtain stocks OHLC data (as per user’s specification of stock code and date range),
- Compute portfolio risk and return (NumPy, random number generator, matrix multiplication),
- Generate Efficient Frontier (using a convex hull (Quick Hull) algorithm in SciPy), based on Modern Portfolio Theory
- Presentation of simulation result and the frontier curve, using interactive visual (Plotly).
- Optimize for allocation weight by optimization algorithm available in SciPy (SHGO), solving for bound/ constraint specified (e.g. annualized risk, etc) (not yet available with GUI)
