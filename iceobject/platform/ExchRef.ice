#pragma once

module GS {
    module enums {
        module exchref {
            enum ExchType {
                extNone,
                extEquity,
                extDerivative,
                extComposite,
                extOtc,
                extSize
            };

            enum CalendarType {
                cdtNone,
                cdtExchange,
                cdtCountry,
                cdtMisc,
                cdtCustom,
                cdtSize
            };

        };
    };
};