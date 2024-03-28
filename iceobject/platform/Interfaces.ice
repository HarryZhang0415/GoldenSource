#pragma once

#include <Ice/Identity.ice>
#include <SingleGen.ice>
#include <DataObjects.ice>

module GS {
    module dataobjects {
        class MuxKey {
        };

        class Allocation {
        };

        class UniverseElement {
        };

        sequence<UniverseElement> Universe;

        class OnDemandAllocation extends Allocation {
            Universe universe;
        };
    };

    module interfaces {
        interface IServer {
            ["amd"] void register(Ice::Identity ident);
            ["amd"] void unregister(Ice::Identity ident);
            void eventRecv(GS::enums::AdminEvent event, string msg);
            idempotent string ping();
        };

        interface Multiplexer {
            ["amd"] void registerDestination(Ice::Identity ident, GS::dataobjects::MuxKey key);
            ["amd"] void unregisterDestination(Ice::Identity ident, GS::dataobjects::MuxKey key);
        };

        interface Allocator {
            /**
            * Registers teh node <identifier> to the allocator.
            */
            ["amd"] void register(string identifier);

            /**
            * Returns the allocation for the node <identifier>
            */
            ["amd"] GS::dataobjects::Allocation getAllocation(string identifier);

            /**
            * Returns all allocations (stored in cache)
            */
            ["amd"] GS::dataobjects::Allocation getAllAllocations();
        };

        interface OnDemandAllocator extends Allocator {
            /**
            * Adds elements to the universe
            */
            ["amd"] void add(string identifier, GS::dataobjects::Universe elements) throws GS::exceptions::ValidateException;

            /**
            * Removes elements from the universe
            */
            ["amd"] void remove(string identifier, GS::dataobjects::Universe elements) throws GS::exceptions::ValidateException;
            
            /**
            * Clears the universe
            */
            ["amd"] void clear();

            /**
            * Runs a one-off cycle of a given element
            */
            ["amd"] void runElement(string identifier, GS::dataobjects::UniverseElement element) throws GS::exceptions::ValidateException;

            /**
            * Returns the current universe
            */
            ["amd"] GS::dataobjects::Universe getUniverse();

        };

    };

};