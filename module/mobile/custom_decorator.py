import allure
from functools import wraps


def user_id(case_map):
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            test_name = f.__name__
            if test_name in case_map:
                user_id_value = case_map[test_name]
                if isinstance(user_id_value, list):
                    for user in user_id_value:
                        allure.dynamic.parameter("user", user)
                else:
                    allure.dynamic.parameter("user", user_id_value)

            return f(self, *args, **kwargs)

        return wrapper

    return decorator
