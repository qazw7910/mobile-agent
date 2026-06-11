import re, pytest
import pytest
import re

import logging

def __logic(test_object: str | int | float, logic: str, expect):
    try:
        operations = {
            '==': lambda v, e: v == e,
            '!=': lambda v, e: v != e,
            'in': lambda v, e: v in e, 'i': lambda v, e: v in e,
            'not in': lambda v, e: v not in e, '!i': lambda v, e: v not in e,
            'c': lambda v, e: e in v,
            '!c': lambda v, e: e not in v,
            '>': lambda v, e: v > e,
            '>=': lambda v, e: v >= e,
            '<': lambda v, e: v < e,
            '<=': lambda v, e: v <= e
        }
        logging.info(f'[Assert Action] Target ({test_object}) should {logic} ({expect}).')
        return operations[logic](test_object, expect)
    except KeyError:
        logging.info(f"❌ Invalid logic: {logic}")
        return False
    except Exception as e:
        logging.error(f"❌ Error during logic operation: {e}")
        return False


# def logic(test_object: str | int | float, logic: str, expect):
#     """
#     Legal logic: '==', '!=', 'in', 'not in', 'c', '!c', '>', '>=', '<', '<='
#     """
#     if not __logic(test_object, logic, expect):
#         raise Exception(f"❌ The condition is not satisfied: {test_object} {logic} {expect}")

def logic(test_object: str | int | float | list, logic: str, expect):
    """
    Legal logic:
    '==', '!=', 'in', 'not in', 'c', '!c', '>', '>=', '<', '<='
    """
    pytest.assume(
        __logic(test_object, logic, expect),
        f"❌ The condition is not satisfied: {test_object} {logic} {expect}"
    )


def __pattern(test_object: str, match_pattern):
    logging.info(f'[Assert Action] Target ({test_object}) should match ({match_pattern}).')
    return bool(re.match(match_pattern, test_object))


# def pattern(test_object: str, match_pattern):
#     """
#     match_pattern should be Regular expression.
#     """
#     if not __pattern(test_object, match_pattern):
#         raise Exception(f"❌ The pattern is not matched: {test_object} {match_pattern}")

def pattern(test_object: str, match_pattern):
    """
    Parameter match_pattern should be Regular expression.
    """
    pytest.assume(
        __pattern(test_object, match_pattern),
        f"❌ The pattern is not matched: {test_object} {match_pattern}"
    )


def bool_assert(result: bool, raise_log: str = ''):
    """
    Simply assert special condition.
    """
    assert result, raise_log
