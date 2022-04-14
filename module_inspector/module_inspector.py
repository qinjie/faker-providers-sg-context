import collections
import inspect
import json
import typing
from enum import Enum
from types import ModuleType, FunctionType
from typing import Any, Callable, Dict

PRIMITIVE_TYPES = {str, int, float, bool, list}


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


class Inspector:

    @classmethod
    def list_sub_modules(
        cls, input_module: ModuleType
    ) -> Dict[str, Any]:
        """
        Return list of sub-modules in the input module
        """
        module_list = {}
        for name, obj in inspect.getmembers(input_module):
            if inspect.ismodule(obj) and obj.__name__.startswith(input_module.__name__):
                module_list[obj.__name__] = obj
        return module_list

    @classmethod
    def list_classes_in_module(
        cls, input_module: type
    ) -> Dict[str, Any]:
        """
        Return a dictionary of classes in a module
        """
        class_list = {}
        for name, obj in inspect.getmembers(input_module):
            if not inspect.isclass(obj): continue
            if name.startswith('_') or name.startswith('__'): continue
            if inspect.getmodule(obj).__name__ == input_module.__name__:
                class_list[obj.__module__ + '.' + obj.__qualname__] = obj
        return class_list

    @classmethod
    def list_class_meta(
        cls, input_cls: type
    ) -> Dict[str, Any]:
        """
        List type and defaults of all parameters in a class, excluding dunder methods
        """
        functions = cls.list_local_func_in_class(input_cls)
        all_meta = {}
        for name, f in functions.items():
            meta = Inspector.get_function_metadata(f)
            all_meta[name] = meta
        return all_meta

    @classmethod
    def list_local_func_in_class(
        cls, input_cls: type
    ) -> Dict[str, Any]:
        """
        Return a dictionary of functions in a class, excluding dunder functions
        """
        methods = {}
        for name, obj in inspect.getmembers(input_cls):
            # Only need non dunder functions
            if name.startswith('_') or name.startswith('__'):
                continue
            if not isinstance(obj, FunctionType):
                continue
            if inspect.isfunction(obj) and obj.__qualname__.startswith(input_cls.__name__):
                methods[name] = obj
        return methods

    @staticmethod
    def get_param_info(param):
        """
        Get Type and Defaults of a parameter. If the parameter is an Enum, also gets the choices available
        """
        p_type = None
        p_optional = False
        # print(param, param.annotation)
        if param.annotation.__class__ is type and (param.annotation is not inspect._empty):
            p_type = param.annotation
        elif param.annotation is not inspect._empty:
            print(f'{str(param.annotation)}, {typing.get_origin(param.annotation)}')
            if param.annotation is typing.Any:
                print('typing.Any: use str type')
                p_type = str
            elif typing.get_origin(param.annotation) is typing.Union:
                print(f'typing.Union: {typing.get_args(param.annotation)}')
                x = typing.get_args(param.annotation)
                if type(None) in x:
                    p_optional = True
                    print(f'Optional: {x}')
                x = tuple(set(x).intersection(PRIMITIVE_TYPES))
                p_type = x if x else None
            elif typing.get_origin(param.annotation) is collections.abc.Collection:
                print('typing.Collection')
                p_type = list
            elif typing.get_origin(param.annotation) in (tuple, list):
                print('typing.Tuple and typing.List')
                p_type = list
            else:
                print('XXX: ', param.annotation, ' = ', typing.get_args(param.annotation))
                p_type = None
        else:
            print(f'NO TYPE: {param}')

        p_choices = None
        if Enum in param.annotation.__class__.__mro__:
            p_choices = [str(choice) for choice in param.annotation.__members__]
        p_default = param.default
        if p_default is param.empty:
            p_default = None

        print(p_type, p_default, p_choices, p_optional)
        return p_type, p_default, p_choices, p_optional

    @classmethod
    def get_function_metadata(
        cls, input_function: Callable
    ) -> Dict[str, Any]:
        """
            Metadata about arguments documentation and the function itself
        """
        signature: inspect.Signature = inspect.signature(input_function)
        arguments_metadata: Dict[str, Dict[str, Any]] = {}
        for key, parameter in signature.parameters.items():
            if key == 'self': continue
            arguments_metadata[key] = {}
            arg_type, arg_default, arg_choices, arg_optional = cls.get_param_info(parameter)
            if arg_type is not None:
                if type(arg_type) is tuple:
                    arg_type = str if str in arg_type else arg_type[0]
                else:
                    arg_type = arg_type
                print(arg_type, type(arg_type))
                arguments_metadata[key]["type"] = arg_type.__name__
            if arg_choices:
                arguments_metadata[key]["choices"] = arg_choices
            if arg_default:
                arguments_metadata[key]["default"] = arg_default if is_jsonable(arg_default) else str(arg_default)
            if arg_optional:
                arguments_metadata[key]["optional"] = arg_optional

        doc_str = inspect.getdoc(input_function)
        doc_str = doc_str if doc_str else ''
        metadata = {
            "module": input_function.__module__,
            "function": input_function.__name__,
            "args": arguments_metadata,
            "doc": doc_str
        }
        # metadata["doc"] = metadata["doc"].split('\n\n')[0].replace('\n', ' ')

        return metadata
