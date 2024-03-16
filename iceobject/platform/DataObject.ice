#pragma once

#include <SingleGen.ice>
#include <Enums.ice>
#include <InstrEnum.ice>

module GS {
    module instrument {
        struct Identifier {
            long instId = 0;
            string symbol = "";
            GS::enums::instr::InstrumentType type;
            int expiryDate = 0;
            GS::dataobjects::IFixed Strike;
            GS::enums::instr::CallPut optType;
            string rootSymbolList = "";
            long secId = 0;
        };
    };
};