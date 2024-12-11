#pragma once

module GS{
    module enums{
        enum AdminEvent {aeInstrReload, aeShutdown, aeRefresh, aeDumpData};
        enum SubscriptionType {RealTime, Periodic, Snapshot, SnapshotWithUL, SnapshotOnlyUL, SnapshotWithRepricing};

        module mktdata {
            enum MarketDataType {
                mdtNone,
                mdtValue,
                mdtVolatility,
                mdtBorrowRate,
                mdtInterestRate,
                mdtDividend,
                mdtMark,
                mdtRateCurve,
                mdtOptionPricingArgs,
                mdtFICurveInput,
                mdtSize
            };
        };    
    };

    module fixings {
        enum FixingType {
            ftNone,
            ftDaily,
            ftOpen,
            ftClose,
            ftSpecialQuotation
        };
    };

    enum RiskMeasure {
        DollarPrice,
        PrevDollarPrice,
        LocalPrice,
        PrevLocalPrice,
        ExtrinsicValue,
        PnlOwned,

        // Equity Measure
        EqDelta,
        EqDeltaUSD,
        EqGamma,
        EqGammaUSD,
        EqCharm,
        EqCharmUSD,
        EqCorrelDelta,
        EqCorrelDeltaUSD,
        EqVega,
        EqWgtVega,
        EqVegaUSD,
        EqAdjVega,
        EqAdjVegaUSD,
        EqVegaVanillaUSD,
        EqWgtVegaUSD,
        EqVolWgtVega,
        EqVolWgtVegaUSD,
        EqVolTimeWgtVega,
        EqVolTimeWgtVegaUSD,
        EqBasketVega,
        EqBasketVegaUSD,
        EqVanna,
        EqVannaUSD,
        EqVolga,
        EqVolgaUSD,
        EqThetaUSD,
        EqVolThetaUSD,
        EqRebalanceDelta,
        EqRebalanceDeltaUSD,
        EqRebalanceGamma,
        EqRebalanceGammaUSD,
        EqSkewDelta,
        EqSkewDeltaUSD,
        EqSkewGamma,
        EqSkewGammaUSD,
        EqRhoBorrow,
        EqRhoBorrowUSD,

        FxDelta,
        FxDeltaUSD,
        FxGamma,
        FxGammaUSD,
        FxCharm,
        FxCharmUSD,
        FxVega,
        FxWgtVega,
        FxVegaUSD,
        FxWgtVegaUSD,
        FxVolWgtVega,
        FxVolWgtVegaUSD,
        FxVanna,
        FxVannaUSD,
        FxVolga,
        FxVolgaUSD,
        FxTheta,
        FxCorrelDeltaUSD,

        //Sticky Fixed Strike Forex measures
        SFK_FxDelta,
        SFK_FxDeltaUSD,
        SFK_FxGamma,
        SFK_FxGammaUSD,
        SFK_FxCharm,
        SFK_FxCharmUSD,
        SFK_FxVanna,
        SFK_FxVannaUSD,

        //Sticky Fixed Delta Forex measures
        SFD_FxDelta,
        SFD_FxDeltaUSD,
        SFD_FxGamma,
        SFD_FxGammaUSD,
        SFD_FxCharm,
        SFD_FxCharmUSD,
        SFD_FxVanna,
        SFD_FxVannaUSD,

        //Sticky Fixed Strike Equity measures
        SFK_EqDelta,
        SFK_EqDeltaUSD,
        SFK_EqGamma,
        SFK_EqGammaUSD,
        SFK_EqCharm,
        SFK_EqCharmUSD,
        SFK_EqVanna,
        SFK_EqVannaUSD,

        //Sticky Fixed Delta Equity measures
        SFD_EqDelta,
        SFD_EqDeltaUSD,
        SFD_EqGamma,
        SFD_EqGammaUSD,
        SFD_EqCharm,
        SFD_EqCharmUSD,
        SFD_EqVanna,
        SFD_EqVannaUSD,

        //Greeks scaled in units of the market convention's hedge contract
        HedgeDelta,
        HedgeGamma,
        HedgeCharm,
        HedgeVanna,
        HedgeSkewDelta,
        HedgeSkewGamma
    };
    dictionary<RiskMeasure, double> RiskMeasures;
    dictionary<long, RiskMeasures> RiskMeasuresById;

    enum TradableAttribute {
        QuotedPrice,
        PrevQuotedPrice,
        UlSpotRef,
        PrevUlSpotRef,
        UlFwdRef,
        PrevUlFwdRef,
        VolRef,
        ImpliedVolRef,
        InputVolRef,
        PrevVolRef,
        BizDaysToExp,
        CalDaysToExp,
        TimeToExp,
        
        // Variance Swap specific fields
        CapAdjustment,
        VarianceVolRef,
        AccruedVol,
        LastFixingValue,
        RemainingFixings,
        TotalFixings,
        
        InterestRateRef,
        BorrowRateRef,
        Fugit,
        BidPriceRef,
        MidPriceRef,
        AskPriceRef,
        LastPriceRef,
        SettlePriceRef
    };
    dictionary<TradableAttribute, double> TradableAttributes;
    dictionary<long, TradableAttributes> TradableAttributesById;

    enum DataStatus {
        dsNone,
        dsEstimated,
        dsUpdated,
        dsOverwritten,
        dsSize,
        dsDeleted
    };

    enum MarketType {
        //Spot Markets
        EquityMarket,
        ForexMarket,
        RateMarket,

        //Derivative Markets
        CreditMarket,
        CreditIndexVolatilityMarket,
        ForexVolatilityMarket,
        EquityVolatilityMarket,
        FuturesVolatilityMarket,
        ForexForwardMarket,

        CommodityMarket,
        CommodityVolatilityMarket,
        CommodityFuturesMarket,
        EquityIndexFuturesMarket,
        EquityIndexFuturesVolatilityMarket,

        //vix type markets
        VolIndexMarket,
        VolIndexFuturesMarket,
        VolIndexVolatilityMarket,

        //Correlation shifts
        EquityCorrelationMarket,
        GlobalCorrelationMarket,
        CrossCorrelationMarket
    };

    enum FitSource {
        fsNone,
        fsAuto,
        fsManual,
        fsSize
    };
};