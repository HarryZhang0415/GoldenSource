#pragma once

module GS {
    module dataobject{
        struct IFixed{
            long val;
        };

        struct IDateTime{
            long val;
        };
        sequence<IDateTime> IDateTimeSeq;

        struct IDate {
            int yyyyMMdd;
        };
        sequence<IDate> IDateSeq;
        dictionary<string, IFixed> NamedValueDict;
    };
    

    module exceptions {

        sequence<string> StackTrace;
        class Error {
            string type = "";
            string message = "";
            StackTrace trace;
        };

        exception ValidateException {
            Object invalid_object;
            string reason = "";
        }; 

    };

};