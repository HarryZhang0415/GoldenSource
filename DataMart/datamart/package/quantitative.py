### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
import pandas
import numpy
from typing import List, Union, Literal
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs

from datamart_core.provider.abstract.data import Data


class ROUTER_quantitative(Container):
    """/quantitative
    capm
    normality
    /performance
    /rolling
    /stats
    summary
    unitroot_test
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def capm(
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
        """Get Capital Asset Pricing Model (CAPM).

        CAPM offers a streamlined way to assess the expected return on an investment while accounting for its risk relative
        to the market. It's a cornerstone of modern financial theory that helps investors understand the trade-off between
        risk and return, guiding more informed investment choices.

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.

        Returns
        -------
        OBBject[CAPMModel]
            CAPM model summary.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Capital Asset Pricing Model (CAPM).
        >>> stock_data = market.equity.price.historical(symbol='TSLA', start_date='2023-01-01', provider='fmp').to_df()
        >>> market.quantitative.capm(data=stock_data, target='close')
        >>> market.quantitative.capm(target='close', data=[{'date': '2023-01-02', 'open': 110.0, 'high': 120.0, 'low': 100.0, 'close': 115.0, 'volume': 10000.0}, {'date': '2023-01-03', 'open': 165.0, 'high': 180.0, 'low': 150.0, 'close': 172.5, 'volume': 15000.0}, {'date': '2023-01-04', 'open': 146.67, 'high': 160.0, 'low': 133.33, 'close': 153.33, 'volume': 13333.33}, {'date': '2023-01-05', 'open': 137.5, 'high': 150.0, 'low': 125.0, 'close': 143.75, 'volume': 12500.0}, {'date': '2023-01-06', 'open': 132.0, 'high': 144.0, 'low': 120.0, 'close': 138.0, 'volume': 12000.0}, {'date': '2023-01-07', 'open': 128.33, 'high': 140.0, 'low': 116.67, 'close': 134.17, 'volume': 11666.67}, {'date': '2023-01-08', 'open': 125.71, 'high': 137.14, 'low': 114.29, 'close': 131.43, 'volume': 11428.57}, {'date': '2023-01-09', 'open': 123.75, 'high': 135.0, 'low': 112.5, 'close': 129.38, 'volume': 11250.0}, {'date': '2023-01-10', 'open': 122.22, 'high': 133.33, 'low': 111.11, 'close': 127.78, 'volume': 11111.11}, {'date': '2023-01-11', 'open': 121.0, 'high': 132.0, 'low': 110.0, 'close': 126.5, 'volume': 11000.0}, {'date': '2023-01-12', 'open': 120.0, 'high': 130.91, 'low': 109.09, 'close': 125.45, 'volume': 10909.09}, {'date': '2023-01-13', 'open': 119.17, 'high': 130.0, 'low': 108.33, 'close': 124.58, 'volume': 10833.33}, {'date': '2023-01-14', 'open': 118.46, 'high': 129.23, 'low': 107.69, 'close': 123.85, 'volume': 10769.23}, {'date': '2023-01-15', 'open': 117.86, 'high': 128.57, 'low': 107.14, 'close': 123.21, 'volume': 10714.29}, {'date': '2023-01-16', 'open': 117.33, 'high': 128.0, 'low': 106.67, 'close': 122.67, 'volume': 10666.67}, {'date': '2023-01-17', 'open': 116.88, 'high': 127.5, 'low': 106.25, 'close': 122.19, 'volume': 10625.0}, {'date': '2023-01-18', 'open': 116.47, 'high': 127.06, 'low': 105.88, 'close': 121.76, 'volume': 10588.24}, {'date': '2023-01-19', 'open': 116.11, 'high': 126.67, 'low': 105.56, 'close': 121.39, 'volume': 10555.56}, {'date': '2023-01-20', 'open': 115.79, 'high': 126.32, 'low': 105.26, 'close': 121.05, 'volume': 10526.32}, {'date': '2023-01-21', 'open': 115.5, 'high': 126.0, 'low': 105.0, 'close': 120.75, 'volume': 10500.0}, {'date': '2023-01-22', 'open': 115.24, 'high': 125.71, 'low': 104.76, 'close': 120.48, 'volume': 10476.19}, {'date': '2023-01-23', 'open': 115.0, 'high': 125.45, 'low': 104.55, 'close': 120.23, 'volume': 10454.55}, {'date': '2023-01-24', 'open': 114.78, 'high': 125.22, 'low': 104.35, 'close': 120.0, 'volume': 10434.78}, {'date': '2023-01-25', 'open': 114.58, 'high': 125.0, 'low': 104.17, 'close': 119.79, 'volume': 10416.67}, {'date': '2023-01-26', 'open': 114.4, 'high': 124.8, 'low': 104.0, 'close': 119.6, 'volume': 10400.0}, {'date': '2023-01-27', 'open': 114.23, 'high': 124.62, 'low': 103.85, 'close': 119.42, 'volume': 10384.62}, {'date': '2023-01-28', 'open': 114.07, 'high': 124.44, 'low': 103.7, 'close': 119.26, 'volume': 10370.37}, {'date': '2023-01-29', 'open': 113.93, 'high': 124.29, 'low': 103.57, 'close': 119.11, 'volume': 10357.14}, {'date': '2023-01-30', 'open': 113.79, 'high': 124.14, 'low': 103.45, 'close': 118.97, 'volume': 10344.83}, {'date': '2023-01-31', 'open': 113.67, 'high': 124.0, 'low': 103.33, 'close': 118.83, 'volume': 10333.33}, {'date': '2023-02-01', 'open': 113.55, 'high': 123.87, 'low': 103.23, 'close': 118.71, 'volume': 10322.58}])
        """  # noqa: E501

        return self._run(
            "/quantitative/capm",
            **filter_inputs(
                data=data,
                target=target,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def normality(
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
        """Get Normality Statistics.

        - **Kurtosis**: whether the kurtosis of a sample differs from the normal distribution.
        - **Skewness**: whether the skewness of a sample differs from the normal distribution.
        - **Jarque-Bera**: whether the sample data has the skewness and kurtosis matching a normal distribution.
        - **Shapiro-Wilk**: whether a random sample comes from a normal distribution.
        - **Kolmogorov-Smirnov**: whether two underlying one-dimensional probability distributions differ.

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.

        Returns
        -------
        OBBject[NormalityModel]
            Normality tests summary. See qa_models.NormalityModel for details.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Normality Statistics.
        >>> stock_data = market.equity.price.historical(symbol='TSLA', start_date='2023-01-01', provider='fmp').to_df()
        >>> market.quantitative.normality(data=stock_data, target='close')
        >>> market.quantitative.normality(target='close', data=[{'date': '2023-01-02', 'open': 110.0, 'high': 120.0, 'low': 100.0, 'close': 115.0, 'volume': 10000.0}, {'date': '2023-01-03', 'open': 165.0, 'high': 180.0, 'low': 150.0, 'close': 172.5, 'volume': 15000.0}, {'date': '2023-01-04', 'open': 146.67, 'high': 160.0, 'low': 133.33, 'close': 153.33, 'volume': 13333.33}, {'date': '2023-01-05', 'open': 137.5, 'high': 150.0, 'low': 125.0, 'close': 143.75, 'volume': 12500.0}, {'date': '2023-01-06', 'open': 132.0, 'high': 144.0, 'low': 120.0, 'close': 138.0, 'volume': 12000.0}, {'date': '2023-01-07', 'open': 128.33, 'high': 140.0, 'low': 116.67, 'close': 134.17, 'volume': 11666.67}, {'date': '2023-01-08', 'open': 125.71, 'high': 137.14, 'low': 114.29, 'close': 131.43, 'volume': 11428.57}, {'date': '2023-01-09', 'open': 123.75, 'high': 135.0, 'low': 112.5, 'close': 129.38, 'volume': 11250.0}])
        """  # noqa: E501

        return self._run(
            "/quantitative/normality",
            **filter_inputs(
                data=data,
                target=target,
                data_processing=True,
            )
        )

    @property
    def performance(self):
        # pylint: disable=import-outside-toplevel
        from . import quantitative_performance

        return quantitative_performance.ROUTER_quantitative_performance(
            command_runner=self._command_runner
        )

    @property
    def rolling(self):
        # pylint: disable=import-outside-toplevel
        from . import quantitative_rolling

        return quantitative_rolling.ROUTER_quantitative_rolling(
            command_runner=self._command_runner
        )

    @property
    def stats(self):
        # pylint: disable=import-outside-toplevel
        from . import quantitative_stats

        return quantitative_stats.ROUTER_quantitative_stats(
            command_runner=self._command_runner
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def summary(
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
        """Get Summary Statistics.

        The summary that offers a snapshot of its central tendencies, variability, and distribution.
        This command calculates essential statistics, including mean, standard deviation, variance,
        and specific percentiles, to provide a detailed profile of your target column. B
        y examining these metrics, you gain insights into the data's overall behavior, helping to identify patterns,
        outliers, or anomalies. The summary table is an invaluable tool for initial data exploration,
        ensuring you have a solid foundation for further analysis or reporting.

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.

        Returns
        -------
        OBBject[SummaryModel]
            Summary table.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Summary Statistics.
        >>> stock_data = market.equity.price.historical(symbol='TSLA', start_date='2023-01-01', provider='fmp').to_df()
        >>> market.quantitative.summary(data=stock_data, target='close')
        >>> market.quantitative.summary(target='close', data=[{'date': '2023-01-02', 'open': 110.0, 'high': 120.0, 'low': 100.0, 'close': 115.0, 'volume': 10000.0}, {'date': '2023-01-03', 'open': 165.0, 'high': 180.0, 'low': 150.0, 'close': 172.5, 'volume': 15000.0}, {'date': '2023-01-04', 'open': 146.67, 'high': 160.0, 'low': 133.33, 'close': 153.33, 'volume': 13333.33}, {'date': '2023-01-05', 'open': 137.5, 'high': 150.0, 'low': 125.0, 'close': 143.75, 'volume': 12500.0}, {'date': '2023-01-06', 'open': 132.0, 'high': 144.0, 'low': 120.0, 'close': 138.0, 'volume': 12000.0}])
        """  # noqa: E501

        return self._run(
            "/quantitative/summary",
            **filter_inputs(
                data=data,
                target=target,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def unitroot_test(
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
        fuller_reg: Literal["c", "ct", "ctt", "nc"] = "c",
        kpss_reg: Literal["c", "ct"] = "c",
    ) -> OBBject:
        """Get Unit Root Test.

        This function applies two renowned tests to assess whether your data series is stationary or if it contains a unit
        root, indicating it may be influenced by time-based trends or seasonality. The Augmented Dickey-Fuller (ADF) test
        helps identify the presence of a unit root, suggesting that the series could be non-stationary and potentially
        unpredictable over time. On the other hand, the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test checks for the
        stationarity of the series, where failing to reject the null hypothesis indicates a stable, stationary series.
        Together, these tests provide a comprehensive view of your data's time series properties, essential for
        accurate modeling and forecasting.

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.
        fuller_reg : Literal["c", "ct", "ctt", "nc", "c"]
            Regression type for ADF test.
        kpss_reg : Literal["c", "ct"]
            Regression type for KPSS test.

        Returns
        -------
        OBBject[UnitRootModel]
            Unit root tests summary.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Unit Root Test.
        >>> stock_data = market.equity.price.historical(symbol='TSLA', start_date='2023-01-01', provider='fmp').to_df()
        >>> market.quantitative.unitroot_test(data=stock_data, target='close')
        >>> market.quantitative.unitroot_test(target='close', data=[{'date': '2023-01-02', 'open': 110.0, 'high': 120.0, 'low': 100.0, 'close': 115.0, 'volume': 10000.0}, {'date': '2023-01-03', 'open': 165.0, 'high': 180.0, 'low': 150.0, 'close': 172.5, 'volume': 15000.0}, {'date': '2023-01-04', 'open': 146.67, 'high': 160.0, 'low': 133.33, 'close': 153.33, 'volume': 13333.33}, {'date': '2023-01-05', 'open': 137.5, 'high': 150.0, 'low': 125.0, 'close': 143.75, 'volume': 12500.0}, {'date': '2023-01-06', 'open': 132.0, 'high': 144.0, 'low': 120.0, 'close': 138.0, 'volume': 12000.0}])
        """  # noqa: E501

        return self._run(
            "/quantitative/unitroot_test",
            **filter_inputs(
                data=data,
                target=target,
                fuller_reg=fuller_reg,
                kpss_reg=kpss_reg,
                data_processing=True,
            )
        )