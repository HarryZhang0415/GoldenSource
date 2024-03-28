#pragma once

#include <SingleGen.ice>
#include <Exchanges.ice>
#include <DataObjects.ice>
#include <ReferenceEnums.ice>

module GS {
    module dataobjects {
        module reference {

            struct CalendarId {
                GS::enums::ExecExchId exchange_id;
                GS::enums::reference::CalendarType calendar_type;
                string country = "";
            };

            struct Holiday {
                GS::dataobjects::IDate date;
                int day_week = 0;
                string descr = "";
                GS::dataobjects::IFixed open_weight;
            };

            dictionary<GS::dataobjects::IDate, GS::dataobjects::reference::Holiday> HolidayDict;

            class Calendar {
                GS::dataobjects::reference::CalendarId calendar_id;
                GS::dataobjects::reference::HolidayDict holidays;
            };

        };
    };
};