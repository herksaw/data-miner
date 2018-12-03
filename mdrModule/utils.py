# -*- coding: utf-8 -*-
import re
import itertools

def find_continous_subsequence(iterable, predicate):
    """
    find the continuous subsequence with predicate function return true

    >>> find_continous_subsequence([2, 1, 2, 4], lambda x: x % 2 == 0)
    [[2], [2, 4]]

    >>> find_continous_subsequence([2, 1, 2, 4], lambda x: x % 2 != 0)
    [[1]]
    """
    seqs = []
    for key, values in itertools.groupby(iterable, key=predicate):
        if key == True:
            seqs.append(list(values))
    return seqs

def split_sequence(seq, predicate):
    """
    split the sequence at the position when predicate return true

    >>> list(split_sequence([0, 1, 2, 1, 2], lambda x: x == 1))
    [[0], [1, 2], [1, 2]]

    >>> list(split_sequence([0, 1, 2, 1, 2, 1], lambda x: x == 2))
    [[0, 1], [2, 1], [2, 1]]

    >>> list(split_sequence([('a', 1), ('b', 2), ('c', 1)], lambda x: x[1] == 1))
    [[('a', 1), ('b', 2)], [('c', 1)]]
    """
    seqs = []
    for s in seq:
        if predicate(s):
            if seqs:
                yield seqs
            seqs = [s]
        else:
            seqs.append(s)
    if seqs:
        yield seqs

def reverse_dict(d):
    return dict(reversed(item) for item in d.items())

def common_prefix(*sequences):
    """determine the common prefix of all sequences passed

    For example:
    >>> common_prefix('abcdef', 'abc', 'abac')
    ['a', 'b']
    """
    prefix = []
    for sample in itertools.izip(*sequences):
        first = sample[0]
        if all([x == first for x in sample[1:]]):
            prefix.append(first)
        else:
            break
    return prefix

def simplify_xpath(xpath):
    return re.sub('\[\d+\]', '', xpath)

def cmp_elements(e1, e2):    # Compare if two elements are the same instance
    if e1 == None or e2 == None:
        return False
    if e1.tag != e2.tag:
        return False
    if e1.text != e2.text:
        return False
    if e1.tail != e2.tail:
        return False
    if e1.attrib != e2.attrib:
        return False
    if len(e1) != len(e2):
        return False

    return all(cmp_elements(c1, c2) for c1, c2 in zip(e1, e2))

# def attach_dyn_prop(instance, prop_name, prop):
#     """Attach property proper to instance with name prop_name.

#     Reference: 
#       * https://stackoverflow.com/a/1355444/509706
#       * https://stackoverflow.com/questions/48448074
#     """
#     class_name = instance.__class__.__name__ + 'Node'
#     child_class = type(class_name, (instance.__class__,), {prop_name: prop})

#     instance.__class__ = child_class
