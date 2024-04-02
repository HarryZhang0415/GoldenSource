import Ice
import GS.dataobjects.reference as do_ref

ice_str_overrides = {
    Ice.Identity: lambda ident: "IDENT({}:{})".format(ident.category, ident.name),
    do_ref.CalendarId: lambda cid: "CID({}.{}.{})".format(cid.exchange_id, cid.calendar_type, cid.country),
    do_ref.Calendar: lambda cal: "CAL({}, [{} holidays])".format(cal.calendar_id, len(cal.holidays))

}

def override_str_repr(ice_type=None):
    if ice_type is None:
        types = ice_str_overrides.keys()
    elif type(ice_type) is list:
        types = ice_type
    else:
        types = [ice_type]

    for t in types:
        if t in ice_str_overrides:
            if '__ice_repr__' not in dir(t):
                t.__ice_repr__ = t.__repr__
            t.__repr__ = ice_str_overrides[t]
        if t in ice_str_overrides:
            if '__ice_str__' not in dir(t):
                t.__ice_str__ = t.__str__
            t.__str__ = ice_str_overrides[t]
