# GoldenSource Platform

[![Downloads](https://static.pepy.tech/badge/datamart)](https://pepy.tech/project/datamart)
[![LatestRelease](https://badge.fury.io/py/datamart.svg)](https://github.com/GoldenSource-finance/GoldenSourceTerminal)

| GoldenSource is committed to build the future of investment research by focusing on an open source infrastructure accessible to everyone, everywhere. |
| :---------------------------------------------------------------------------------------------------------------------------------------------: |
|              ![GoldenSourceLogo](https://user-images.githubusercontent.com/25267873/218899768-1f0964b8-326c-4f35-af6f-ea0946ac970b.png)               |
|                                                 Check our website at [datamart.co](www.datamart.co)                                                 |

## Overview

The GoldenSource Platform provides a convenient way to access raw financial data from multiple data providers. The package comes with a ready to use REST API - this allows developers from any language to easily create applications on top of GoldenSource Platform.

## Installation

The command below provides access to the core functionalities behind the GoldenSource Platform.

```bash
pip install datamart
```

This will install the following data providers:

| Extension Name          | Description                                                               | Installation Command                | Minimum Subscription Type Required |
| ----------------------- | ------------------------------------------------------------------------- | ----------------------------------- | ---------------------------------- |
| datamart-benzinga         | [Benzinga](https://www.benzinga.com/apis/en-ca/) data connector           | pip install datamart-benzinga         | Paid                               |
| datamart-federal-reserve  | [FederalReserve](https://www.federalreserve.gov/data.html) data connector | pip install datamart-federal-reserve  | Free                               |
| datamart-fmp              | [FMP](https://site.financialmodelingprep.com/developer/) data connector   | pip install datamart-fmp              | Free                               |
| datamart-fred             | [FRED](https://fred.stlouisfed.org/) data connector                       | pip install datamart-fred             | Free                               |
| datamart-intrinio         | [Intrinio](https://intrinio.com/pricing) data connector                   | pip install datamart-intrinio         | Paid                               |
| datamart-oecd             | [OECD](https://data.oecd.org/) data connector                             | pip install datamart-oecd             | Free                               |
| datamart-polygon          | [Polygon](https://polygon.io/) data connector                             | pip install datamart-polygon          | Free                               |
| datamart-sec              | [SEC](https://www.sec.gov/edgar/sec-api-documentation) data connector     | pip install datamart-sec              | Free                               |
| datamart-tiingo           | [Tiingo](https://www.tiingo.com/about/pricing) data connector             | pip install datamart-tiingo           | Free                               |
| datamart-tradingeconomics | [TradingEconomics](https://tradingeconomics.com/api) data connector       | pip install datamart-tradingeconomics | Paid                               |
| datamart-yahoo-finance    | [Yahoo Finance](https://finance.yahoo.com/) data connector                | pip install datamart-yfinance         | Free                               |

To install extensions that expand the core functionalities specify the extension name or use `all` to install all.

```bash
# Install a single extension, e.g. datamart-charting and yahoo finance
pip install datamart[charting]
pip install datamart-yfinance
```

Alternatively, you can install all extensions at once.

```bash
pip install datamart[all]
```

> Note: These instruction are specific to v4. For installation instructions and documentation for v3 go to our [website](https://docs.datamart.co/sdk).

## Python

```python
>>> from datamart import market
>>> output = market.equity.price.historical("AAPL")
>>> df = output.to_dataframe()
>>> df.head()
              open    high     low  ...  change_percent             label  change_over_time
date                                ...
2022-09-19  149.31  154.56  149.10  ...         3.46000  September 19, 22          0.034600
2022-09-20  153.40  158.08  153.08  ...         2.28000  September 20, 22          0.022800
2022-09-21  157.34  158.74  153.60  ...        -2.30000  September 21, 22         -0.023000
2022-09-22  152.38  154.47  150.91  ...         0.23625  September 22, 22          0.002363
2022-09-23  151.19  151.47  148.56  ...        -0.50268  September 23, 22         -0.005027

[5 rows x 12 columns]
```

## API keys

To fully leverage the GoldenSource Platform you need to get some API keys to connect with data providers. Here are the 3 options on where to set them:

1. GoldenSource Hub
2. Runtime
3. Local file

### 1. GoldenSource Hub

Set your keys at [GoldenSource Hub](https://my.datamart.co/app/sdk/api-keys) and get your personal access token from <https://my.datamart.co/app/sdk/pat> to connect with your account.

```python
>>> from datamart import market
>>> datamart.account.login(pat="OPENBB_PAT")

>>> # Persist changes in GoldenSource Hub
>>> market.account.save()
```

### 2. Runtime

```python
>>> from datamart import market
>>> market.user.credentials.fmp_api_key = "REPLACE_ME"
>>> market.user.credentials.polygon_api_key = "REPLACE_ME"

>>> # Persist changes in ~/.datamart_platform/user_settings.json
>>> market.account.save()
```

### 3. Local file

You can specify the keys directly in the `~/.datamart_platform/user_settings.json` file.

Populate this file with the following template and replace the values with your keys:

```json
{
  "credentials": {
    "fmp_api_key": "REPLACE_ME",
    "polygon_api_key": "REPLACE_ME",
    "benzinga_api_key": "REPLACE_ME",
    "fred_api_key": "REPLACE_ME"
  }
}
```

## REST API

The GoldenSource Platform comes with a ready to use REST API built with FastAPI. Start the application using this command:

```bash
uvicorn market_core.api.rest_api:app --host 0.0.0.0 --port 8000 --reload
```

Check `datamart-core` [README](https://pypi.org/project/datamart-core/) for additional info.

## Install for development

To develop the GoldenSource Platform you need to have the following:

- Git
- Python 3.8 or higher
- Virtual Environment with `poetry` and `toml` packages installed
  - To install these packages activate your virtual environment and run `pip install poetry toml`

How to install the platform in editable mode?

  1. Activate your virtual environment
  1. Navigate into the `datamart_platform` folder
  1. Run `python dev_install.py` to install the packages in editable mode
