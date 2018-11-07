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


def remove_value_by_header(content1, content2, headers, remove_header):
    remove_value = remove_header
    new_content1 = []
    new_content2 = []
    l = len(headers)
    for index in range(0, l):
        exist = False
        for x in remove_value:
            if x in headers[index]:
                exist = True
            if not exist:
                new_content1.append(content1[index])
                new_content2.append(content2[index])
    return content1, content2


