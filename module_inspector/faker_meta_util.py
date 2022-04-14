import json
import logging
import pathlib
import traceback
from typing import Any, Dict, Optional

import faker

# Initialize logger
from app.proj_zorua.module_inspector import Inspector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize faker object
fake = faker.Faker()
faker.Faker.seed()

# Load list of excluded providers
EXCLUDED_LIST_FILE = 'excluded_providers.json'
input_file = pathlib.Path(__file__).resolve().parent.joinpath(EXCLUDED_LIST_FILE)
with open(input_file) as f:
    d = json.loads(f.read())
    EXCLUDED_MODULES = d['modules']
    EXCLUDED_CLASSES = d['classes']
    EXCLUDED_FUNCTIONS = d['functions']


def list_faker_standard_providers(excluded=EXCLUDED_MODULES):
    main_module = faker.providers
    module_list = Inspector.list_sub_modules(main_module)
    module_list[main_module.__name__] = main_module

    # Exclude Providers
    for m in excluded:
        print(f'Removing provider {m}')
        module_list.pop(m, None)

    return module_list


def list_faker_provider_classes(module_list, excluded=EXCLUDED_CLASSES):
    class_list = {}
    for name, m in module_list.items():
        result = Inspector.list_classes_in_module(m)
        class_list.update(result)

    # Exclude Classes
    for m in excluded:
        print(f'Removing class {m}')
        class_list.pop(m, None)

    return class_list


def list_faker_class_meta(class_list, excluded=EXCLUDED_FUNCTIONS):
    method_list = {}
    for name, c in class_list.items():
        result = Inspector.list_class_meta(c)
        method_list.update(result)

    # Exclude Classes
    for m in excluded:
        print(f'Removing function {m}')
        method_list.pop(m, None)

    return method_list


def get_faker_func_signature(function_name: str):
    try:
        f = getattr(fake, function_name)
        meta = Inspector.get_function_metadata(f)
        return meta
    except Exception as e:
        error_msg = (
            f"Error in getting function signature: {function_name}):"
            f"{str(e)}: {traceback.format_exc()}"
        )
        logger.error(error_msg)
        logger.exception(e)


if __name__ == '__main__':
    # module_list = list_faker_standard_providers()
    # print(module_list)
    #
    # # class_list = list_faker_provider_classes(module_list)
    # class_list = list_faker_provider_classes({'faker.providers': module_list['faker.providers']})
    # print(class_list)

    # other_classes = {
    # }
    # class_list.update(other_classes)
    #

    # meta_list = list_faker_class_meta(class_list)
    # print(str(meta_list))

    input = {
        "module": "faker.providers",
        "function": "random_int",
        "args": {
            "min": 5,
            "max": 20,
            "step": 5
        }
    }
    result = gen_fake_data(input['function'], input['args'])
    print(result)

    # input = {
    #     "function": "address",
    #     "args": {
    #     }
    # }
    # result = gen_fake_data(input['function'], input['args'])
    # print(result)
    #
    # input = {
    #     "function": "date_this_century",
    #     "args": {
    #         "before_today": "true"
    #     }
    # }
    # result = gen_fake_data(input['function'], input['args'])
    # print(result)
