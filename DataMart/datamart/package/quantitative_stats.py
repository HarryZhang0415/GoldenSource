### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
import pandas
import numpy
from typing import List, Union
from annotated_types import Ge
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs

from datamart_core.provider.abstract.data import Data


class ROUTER_quantitative_stats(Container):
    """/quantitative/stats
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
    ) -> OBBject:
        """
        Calculate the rolling kurtosis of a target column.

        Kurtosis measures the "tailedness" of the probability distribution of a real-valued random variable.
        High kurtosis indicates a distribution with heavy tails (outliers), suggesting a higher risk of extreme outcomes.
        Low kurtosis indicates a distribution with lighter tails (less outliers), suggesting less risk of extreme outcomes.
        This function helps in assessing the risk of outliers in financial returns or other time series data.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate kurtosis.

        Returns
        -------
        OBBject[List[Data]]
            An object containing the kurtosis value

        Examples
        --------
        >>> from datamart import market
        >>> # Get Kurtosis.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.stats.kurtosis(data=returns, target="close")
        >>> market.quantitative.stats.kurtosis(target='close', data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/stats/kurtosis",
            **filter_inputs(
                data=data,
                target=target,
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
    ) -> OBBject:
        """
        Calculate the  mean (average) of a target column.

        The rolling mean is a simple moving average that calculates the average of a target variable.
        This function is widely used in financial analysis to smooth short-term fluctuations and highlight longer-term trends
        or cycles in time series data.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate the mean.

        Returns
        -------
            OBBject[List[Data]]
                An object containing the mean value.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Mean.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.stats.mean(data=returns, target="close")
        >>> market.quantitative.stats.mean(target='close', data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/stats/mean",
            **filter_inputs(
                data=data,
                target=target,
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
        quantile_pct: Annotated[float, Ge(ge=0)] = 0.5,
    ) -> OBBject:
        """
        Calculate the quantile of a target column at a specified quantile percentage.

        Quantiles are points dividing the range of a probability distribution into  intervals with equal probabilities,
        or dividing the  sample in the same way.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate the quantile.
        quantile_pct: NonNegativeFloat, optional
            The quantile percentage to calculate (e.g., 0.5 for median), default is 0.5.

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling quantile values with the median.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Quantile.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.stats.quantile(data=returns, target="close", quantile_pct=0.75)
        >>> market.quantitative.stats.quantile(target='close', data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/stats/quantile",
            **filter_inputs(
                data=data,
                target=target,
                quantile_pct=quantile_pct,
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
    ) -> OBBject:
        """Get the skew of the data set.

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

        Returns
        -------
        OBBject[List[Data]]
            Rolling skew.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Skewness.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.stats.skew(data=returns, target="close")
        >>> market.quantitative.stats.skew(target='close', data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/stats/skew",
            **filter_inputs(
                data=data,
                target=target,
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
    ) -> OBBject:
        """
        Calculate the rolling standard deviation of a target column.

        Standard deviation is a measure of the amount of variation or dispersion of a set of values.
        It is widely used to assess the risk and volatility of financial returns or other time series data
        It is the square root of the variance.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate standard deviation.

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling standard deviation values.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Standard Deviation.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.stats.stdev(data=returns, target="close")
        >>> market.quantitative.stats.stdev(target='close', data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/stats/stdev",
            **filter_inputs(
                data=data,
                target=target,
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
    ) -> OBBject:
        """
        Calculate the  variance of a target column.

        Variance measures the dispersion of a set of data points around their mean. It is a key metric for
        assessing the volatility and stability of financial returns or other time series data.

        Parameters
        ----------
        data: List[Data]
            The time series data as a list of data points.
        target: str
            The name of the column for which to calculate variance.

        Returns
        -------
        OBBject[List[Data]]
            An object containing the rolling variance values.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Variance.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.stats.variance(data=returns, target="close")
        >>> market.quantitative.stats.variance(target='close', data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/stats/variance",
            **filter_inputs(
                data=data,
                target=target,
                data_processing=True,
            )
        )