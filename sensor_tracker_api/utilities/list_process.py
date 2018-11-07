import collections


def compare_list(list1, list2):
    """
    No Matter order if list1 and list2 contains same element then return True

    """
    a = list_check(list1)
    b = list_check(list2)
    res = collections.Counter(a) == collections.Counter(b)
    return res


def list_check(list_value):
    if type(list_value) is tuple:
        list_value = list(list_value)
    list_value = ["" if x is None else str(x) for x in list_value]

    return list_value
