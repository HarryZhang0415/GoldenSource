#pragma once

#include <Ice/Identity.ice>
#include <SingleGen.ice>
#include <EventEnum.ice>

module GS {
    module dataobject {
        module event_scanner {

            class EventTrigger {
                string m_desc;
                GS::dataobject::IDateTime m_time;
            };
            sequence<EventTrigger> EventTriggerSequence;
        };

        module event {
            ///////////////////////////////////////////////////////
            // Event Stuff
            ///////////////////////////////////////////////////////

            class EventInfo {
                GS::dataobject::IDateTime m_timestamp;
                GS::enums::event::EventType m_type = GS::enums::event::EventType::etChanged;
                GS::enums::event::EventLevel m_level = GS::enums::event::EventLevel::elDebug2;
                string m_msg = "";
                long m_seqnum = -1;
                string m_topic = "";
                string m_ticker = "";
                string m_underlyingTicker = "";
            };
            sequence<EventInfo> EventInfoSeq;
            dictionary<string, EventInfoSeq> EventInfoTopicMap;

            sequence<string>    EventTopicSeq;
            sequence<GS::enums::event::EventLevel> EventLevelSeq;
            sequence<string>    EventTickerSeq;

        };
    };
};