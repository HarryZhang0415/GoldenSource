### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
import pandas
import numpy
from typing import List, Union
from annotated_types import Ge, Gt
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs

from datamart_core.provider.abstract.data import Data


class ROUTER_quantitative_rolling(Container):
    """/quantitative/rolling
    kurtosis
    mean
    quantile
    skew
    stdev
    variance
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def kurtosis(
        self,
        data: Union[
            list,
            dict,
            pandas.DataFrame,
            List[pandas.DataFrame],
            pandas.core.series.Series,
            List[pandas.core.series.Series],
            numpy.ndarray,
            Data,
            List[Data],
        ],
        target: str,
        window: Annotated[int, Gt(gt=0)] = 21,
        index: str = "date",
    ) -> OBBject:
        """
        Calculate the rolling kurtosis of a target column within a given window size.

        Kurtosis measures the "tailedness" of the probability distribution of a real-valued random variable.
        High kurtosis indicates a distribution with heavy tails (outliers), suggesting a higher risk of extreme outcomes.
        Low kurtosis indicates a distribution with lighter tails (less outliers), suggesting less risk of extreme outcomes.
        This function helps in assessing the risk of outliers in financial returns or other time series data over a specified
        rolling window.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate kurtosis.
        window: PositiveInt
            The number of observations used for calculating the rolling measure.
        index: str, optional
            The name of the index column, default is "date".

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling kurtosis values.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Kurtosis.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.rolling.kurtosis(data=returns, target="close", window=252)
        >>> market.quantitative.rolling.kurtosis(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/rolling/kurtosis",
            **filter_inputs(
                data=data,
                target=target,
                window=window,
                index=index,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def mean(
        self,
        data: Union[
            list,
            dict,
            pandas.DataFrame,
            List[pandas.DataFrame],
            pandas.core.series.Series,
            List[pandas.core.series.Series],
            numpy.ndarray,
            Data,
            List[Data],
        ],
        target: str,
        window: Annotated[int, Gt(gt=0)] = 21,
        index: str = "date",
    ) -> OBBject:
        """
        Calculate the rolling mean (average) of a target column within a given window size.

        The rolling mean is a simple moving average that calculates the average of a target variable over a specified window.
        This function is widely used in financial analysis to smooth short-term fluctuations and highlight longer-term trends
        or cycles in time series data.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate the mean.
        window: PositiveInt
            The number of observations used for calculating the rolling measure.
        index: str, optional
            The name of the index column, default is "date".

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling mean values.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Mean.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.rolling.mean(data=returns, target="close", window=252)
        >>> market.quantitative.rolling.mean(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/rolling/mean",
            **filter_inputs(
                data=data,
                target=target,
                window=window,
                index=index,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def quantile(
        self,
        data: Union[
            list,
            dict,
            pandas.DataFrame,
            List[pandas.DataFrame],
            pandas.core.series.Series,
            List[pandas.core.series.Series],
            numpy.ndarray,
            Data,
            List[Data],
        ],
        target: str,
        window: Annotated[int, Gt(gt=0)] = 21,
        quantile_pct: Annotated[float, Ge(ge=0)] = 0.5,
        index: str = "date",
    ) -> OBBject:
        """
        Calculate the rolling quantile of a target column within a given window size at a specified quantile percentage.

        Quantiles are points dividing the range of a probability distribution into  intervals with equal probabilities,
        or dividing the  sample in the same way. This function is useful for understanding the distribution of data
        within a specified window, allowing for analysis of trends, identification of outliers, and assessment of risk.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate the quantile.
        window: PositiveInt
            The number of observations used for calculating the rolling measure.
        quantile_pct: NonNegativeFloat, optional
            The quantile percentage to calculate (e.g., 0.5 for median), default is 0.5.
        index: str, optional
            The name of the index column, default is "date".

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling quantile values with the median.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Quantile.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.rolling.quantile(data=returns, target="close", window=252, quantile_pct=0.25)
        >>> market.quantitative.rolling.quantile(data=returns, target="close", window=252, quantile_pct=0.75)
        >>> market.quantitative.rolling.quantile(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/rolling/quantile",
            **filter_inputs(
                data=data,
                target=target,
                window=window,
                quantile_pct=quantile_pct,
                index=index,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def skew(
        self,
        data: Union[
            list,
            dict,
            pandas.DataFrame,
            List[pandas.DataFrame],
            pandas.core.series.Series,
            List[pandas.core.series.Series],
            numpy.ndarray,
            Data,
            List[Data],
        ],
        target: str,
        window: Annotated[int, Gt(gt=0)] = 21,
        index: str = "date",
    ) -> OBBject:
        """Get Rolling Skew.

        Skew is a statistical measure that reveals the degree of asymmetry of a distribution around its mean.
        Positive skewness indicates a distribution with an extended tail to the right, while negative skewness shows a tail
        that stretches left. Understanding skewness can provide insights into potential biases in data and help anticipate
        the nature of future data points. It's particularly useful for identifying the likelihood of extreme outcomes in
        financial returns, enabling more informed decision-making based on the distribution's shape over a specified period.

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.
        window : PositiveInt
            Window size.
        index : str, optional
            Index column name, by default "date"

        Returns
        -------
        OBBject[List[Data]]
            Rolling skew.


        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Mean.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.rolling.skew(data=returns, target="close")
        >>> market.quantitative.rolling.skew(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/rolling/skew",
            **filter_inputs(
                data=data,
                target=target,
                window=window,
                index=index,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def stdev(
        self,
        data: Union[
            list,
            dict,
            pandas.DataFrame,
            List[pandas.DataFrame],
            pandas.core.series.Series,
            List[pandas.core.series.Series],
            numpy.ndarray,
            Data,
            List[Data],
        ],
        target: str,
        window: Annotated[int, Gt(gt=0)] = 21,
        index: str = "date",
    ) -> OBBject:
        """
        Calculate the rolling standard deviation of a target column within a given window size.

        Standard deviation is a measure of the amount of variation or dispersion of a set of values.
        It is widely used to assess the risk and volatility of financial returns or other time series data
        over a specified rolling window.  It is the square root of the variance.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate standard deviation.
        window: PositiveInt
            The number of observations used for calculating the rolling measure.
        index: str, optional
            The name of the index column, default is "date".

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling standard deviation values.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Standard Deviation.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.rolling.stdev(data=returns, target="close", window=252)
        >>> market.quantitative.rolling.stdev(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/rolling/stdev",
            **filter_inputs(
                data=data,
                target=target,
                window=window,
                index=index,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def variance(
        self,
        data: Union[
            list,
            dict,
            pandas.DataFrame,
            List[pandas.DataFrame],
            pandas.core.series.Series,
            List[pandas.core.series.Series],
            numpy.ndarray,
            Data,
            List[Data],
        ],
        target: str,
        window: Annotated[int, Gt(gt=0)] = 21,
        index: str = "date",
    ) -> OBBject:
        """
        Calculate the rolling variance of a target column within a given window size.

        Variance measures the dispersion of a set of data points around their mean. It is a key metric for
        assessing the volatility and stability of financial returns or other time series data over a specified rolling window.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate variance.
        window: PositiveInt
            The number of observations used for calculating the rolling measure.
        index: str, optional
            The name of the index column, default is "date".

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling variance values.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Variance.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.rolling.variance(data=returns, target="close", window=252)
        >>> market.quantitative.rolling.variance(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/rolling/variance",
            **filter_inputs(
                data=data,
                target=target,
                window=window,
                index=index,
                data_processing=True,
            )
        )