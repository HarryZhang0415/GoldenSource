#pragma once

module GS {
    module enums {
        module instr {

    // Day convention
    enum DayConvention {
        dcNone,
        dcActual,
        dcAct365,
        dcAct360
    };

    enum DateGenerationRule {
        dgNone,
        dgBackward,
        dgForward,
        dgZero,
        dgThirdWednesday,
        dgTwentieth,
        dgTwentiethIMM
    };

    enum Venue {
        vNone,
        vActiv,
        vOrc,
        vOTC
    }

    ////////////////////////////////
    // Instrument Stuff
    ////////////////////////////////

    enum InstrumentClass {
        icsNone,
        icsEquity,
        icsIndex,
        icsVix,
        icsFX,
        icsCommodity,
        icsETF,
        icsFund,
        icsRate
    }

    enum InstrumentType {
        itNone,
        itCash,
        itEquity,
        itETF,
        itIndex,
        itOption,
        itOptionOnFuture,
        itFuture,
        itEquitySwap,
        itVarianceSwap,
        itVolSwap,
        itEquityBasket,
        itOTCOption,
        itPreferred,
        itFXForward,
        itFxOption,
        itOTCEquity,
        itFXForwardContract,
        itFXForwardRate,
        itNDF,
        itNDFContract,
        itWarrant,
    };

    enum CallPut {
        cpNone,
        cpCall,
        cpPut,
        cpSize
    };

    enum OptionType {
        otNone,
        otCall,
        otPut,
        otCap,
        otFloor,
        otRec,
        otPay,
        otSize
    };

    enum SettlementStyle {
        ssNone,
        ssPhysical,
        ssCash,
        ssFutureAsCash,
        ssSize
    };

    enum ExerciseStyle {
        esNone,
        esEuropean,
        esAmerican,
        esBermudan,
        esSize
    };

    enum BussinessDayConvention {
        bdcNone,
        bdcFollowing,
        bdcModifiedFollowing,
        bdcPreceding,
        bdcModifiedPreceding,
        bdcUnadjusted,
        bdcSize
    };

    enum QuoteType {
        qtNone,
        qtSpotPremium,
        qtBlackVolSpread,
        qtATM,
        qtButterfly,
        qtRiskReversal,
        qtSize
    };

    enum PriceType {
        ptNone,
        ptAsk,
        ptBid,
        ptClose,
        ptHighe,
        ptLow,
        ptMid,
        ptNAV,
        ptOpen,
        ptAverage,
        ptSize
    };

    enum BarrierType {
        btNone,
        btDownOut,
        btDownIn,
        btUpOut,
        btUpIn,
        btSize
    };

    enum BarrierCategory {
        bcNone,
        bcSingle,
        bcDouble,
        bcSize
    };
};
};
};