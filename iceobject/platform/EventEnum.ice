#pragma once

module GS {
    module enums {
        module event {
            enum EventType {etNone, etChanged, etTweet, etSize};
            enum EventLevel {elNone, elCritical, elError, elWarning, elInfo, elDebug1, elDebug2, elSize};
        };
    };
};