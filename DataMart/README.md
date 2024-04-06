# GoldenSource Platform

## Overview

The GoldenSource Platform provides a convenient way to access raw financial data from multiple data providers. The package comes with a ready to use REST API - this allows developers from any language to easily create applications on top of GoldenSource Platform.

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

1. Runtime
2. Local file

### 1. Runtime

```python
>>> from datamart import market
>>> market.user.credentials.fmp_api_key = "REPLACE_ME"
>>> market.user.credentials.polygon_api_key = "REPLACE_ME"

>>> # Persist changes in datamart/user_settings.json
>>> market.account.save()
```

### 2. Local file

You can specify the keys directly in the `datamart/user_settings.json` file.

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