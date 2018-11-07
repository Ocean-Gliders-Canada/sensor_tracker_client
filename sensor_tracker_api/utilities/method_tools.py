def call_method(name, o, param=None):
    """
    Call the method by provide the function name, and obj instance,
    if method accept para, then accept param.
    if only kwargs use dict, if only one simple arg or one array, just use it
    and if it is complex use tuple
    return value return from the specific method
    """

    obj = o
    if o:
        obj = o
    if param:
        if type(param) is tuple:
            res = getattr(obj, name)(*param)
        elif type(param) is dict:
            res = getattr(obj, name)(**param)
        else:
            res = getattr(obj, name)(param)
    else:
        res = getattr(obj, name)()

    return res



