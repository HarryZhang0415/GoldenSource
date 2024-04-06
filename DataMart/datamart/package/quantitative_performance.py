### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from datamart_core.app.static.container import Container
from datamart_core.app.model.obbject import OBBject
import pandas
import numpy
from typing import List, Union
from annotated_types import Gt
from typing_extensions import Annotated
from datamart_core.app.static.utils.decorators import exception_handler, validate

from datamart_core.app.static.utils.filters import filter_inputs

from datamart_core.provider.abstract.data import Data


class ROUTER_quantitative_performance(Container):
    """/quantitative/performance
    omega_ratio
    sharpe_ratio
    sortino_ratio
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def omega_ratio(
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
        threshold_start: float = 0.0,
        threshold_end: float = 1.5,
    ) -> OBBject:
        """Calculate the Omega Ratio.

        The Omega Ratio is a sophisticated metric that goes beyond traditional performance measures by considering the
        probability of achieving returns above a given threshold. It offers a more nuanced view of risk and reward,
        focusing on the likelihood of success rather than just average outcomes.

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.
        threshold_start : float, optional
            Start threshold, by default 0.0
        threshold_end : float, optional
            End threshold, by default 1.5

        Returns
        -------
        OBBject[List[OmegaModel]]
            Omega ratios.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Omega Ratio.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.performance.omega_ratio(data=returns, target="close")
        >>> market.quantitative.performance.omega_ratio(target='close', data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/performance/omega_ratio",
            **filter_inputs(
                data=data,
                target=target,
                threshold_start=threshold_start,
                threshold_end=threshold_end,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def sharpe_ratio(
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
        rfr: float = 0.0,
        window: Annotated[int, Gt(gt=0)] = 252,
        index: str = "date",
    ) -> OBBject:
        """Get Rolling Sharpe Ratio.

        This function calculates the Sharpe Ratio, a metric used to assess the return of an investment compared to its risk.
        By factoring in the risk-free rate, it helps you understand how much extra return you're getting for the extra
        volatility that you endure by holding a riskier asset. The Sharpe Ratio is essential for investors looking to
        compare the efficiency of different investments, providing a clear picture of potential rewards in relation to their
        risks over a specified period. Ideal for gauging the effectiveness of investment strategies, it offers insights into
        optimizing your portfolio for maximum return on risk.

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.
        rfr : float, optional
            Risk-free rate, by default 0.0
        window : PositiveInt, optional
            Window size, by default 252
        index : str, optional

        Returns
        -------
        OBBject[List[Data]]
            Sharpe ratio.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Sharpe Ratio.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.performance.sharpe_ratio(data=returns, target="close")
        >>> market.quantitative.performance.sharpe_ratio(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/performance/sharpe_ratio",
            **filter_inputs(
                data=data,
                target=target,
                rfr=rfr,
                window=window,
                index=index,
                data_processing=True,
            )
        )

    @exception_handler
    @validate(config=dict(arbitrary_types_allowed=True))
    def sortino_ratio(
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
        target_return: float = 0.0,
        window: Annotated[int, Gt(gt=0)] = 252,
        adjusted: bool = False,
        index: str = "date",
    ) -> OBBject:
        """Get rolling Sortino Ratio.

        The Sortino Ratio enhances the evaluation of investment returns by distinguishing harmful volatility
        from total volatility. Unlike other metrics that treat all volatility as risk, this command specifically assesses
        the volatility of negative returns relative to a target or desired return.
        It's particularly useful for investors who are more concerned with downside risk than with overall volatility.
        By calculating the Sortino Ratio, investors can better understand the risk-adjusted return of their investments,
        focusing on the likelihood and impact of negative returns.
        This approach offers a more nuanced tool for portfolio optimization, especially in strategies aiming
        to minimize the downside.

        For method & terminology see:
        http://www.redrockcapital.com/Sortino__A__Sharper__Ratio_Red_Rock_Capital.pdf

        Parameters
        ----------
        data : List[Data]
            Time series data.
        target : str
            Target column name.
        target_return : float, optional
            Target return, by default 0.0
        window : PositiveInt, optional
            Window size, by default 252
        adjusted : bool, optional
            Adjust sortino ratio to compare it to sharpe ratio, by default False
        index:str
            Index column for input data
        Returns
        -------
        OBBject[List[Data]]
            Sortino ratio.

        Examples
        --------
        >>> from datamart import market
        >>> # Get Rolling Sortino Ratio.
        >>> stock_data = market.equity.price.historical(symbol="TSLA", start_date="2023-01-01", provider="fmp").to_df()
        >>> returns = stock_data["close"].pct_change().dropna()
        >>> market.quantitative.performance.sortino_ratio(data=stock_data, target="close")
        >>> market.quantitative.performance.sortino_ratio(data=stock_data, target="close", target_return=0.01, window=126, adjusted=True)
        >>> market.quantitative.performance.sortino_ratio(target='close', window=2, data=[{'date': '2023-01-02', 'close': 0.05}, {'date': '2023-01-03', 'close': 0.08}, {'date': '2023-01-04', 'close': 0.07}, {'date': '2023-01-05', 'close': 0.06}, {'date': '2023-01-06', 'close': 0.06}])
        """  # noqa: E501

        return self._run(
            "/quantitative/performance/sortino_ratio",
            **filter_inputs(
                data=data,
                target=target,
                target_return=target_return,
                window=window,
                adjusted=adjusted,
                index=index,
                data_processing=True,
            )
        )