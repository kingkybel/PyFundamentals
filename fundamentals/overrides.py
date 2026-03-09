# Repository:   https://github.com/PyFundamentals
# File Name:    fundamentals/overrides.py
# Description:  interface to formalize overrides
#
# Copyright (C) 2024 Dieter J Kybelksties <github@kybelksties.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# @date: 2026-03-09
# @author: Dieter J Kybelksties

import inspect


class OverrideChecker:
    def __init__(self, method, interface_class=None):
        self.method = method
        self.interface_class = interface_class
        self.name = None
        self.owner = None

    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name

        if not self.interface_class:
            # Find the ABC in owner.__mro__ that has the method
            for cls in owner.__mro__[1:]:  # skip self
                if hasattr(cls, name):
                    self.interface_class = cls
                    break
            else:
                raise AssertionError(f"No interface class found for method {name}")

        assert name in dir(self.interface_class)

        # Check signatures
        interface_method = getattr(self.interface_class, name)
        interface_sig = inspect.signature(interface_method)
        method_sig = inspect.signature(self.method)

        # Check that all parameters in interface_sig are present in method_sig
        for param_name, param in interface_sig.parameters.items():
            if param_name not in method_sig.parameters:
                if param.kind == param.VAR_KEYWORD:
                    # If interface has **kwargs, sub must have it
                    if not any(p.kind == p.VAR_KEYWORD for p in method_sig.parameters.values()):
                        raise AssertionError(f"Method {name} must have **kwargs since interface does")
                else:
                    raise AssertionError(f"Method {name} missing parameter {param_name}")
            else:
                sub_param = method_sig.parameters[param_name]
                # Check parameter kind compatibility
                if param.kind != sub_param.kind:
                    # If interface has KEYWORD_ONLY, implementation must also have KEYWORD_ONLY
                    if param.kind == param.KEYWORD_ONLY:
                        raise AssertionError(f"Parameter {param_name} must be keyword-only in method {name}")
                    # If interface has POSITIONAL_ONLY, implementation must also have POSITIONAL_ONLY
                    if param.kind == param.POSITIONAL_ONLY:
                        raise AssertionError(f"Parameter {param_name} must be positional-only in method {name}")
                    # Allow VAR_POSITIONAL (*args) to be compatible
                    if param.kind == param.VAR_POSITIONAL:
                        if sub_param.kind != param.VAR_POSITIONAL:
                            raise AssertionError(f"Parameter {param_name} must be *args in method {name}")
                    # Allow VAR_KEYWORD (**kwargs) to be compatible
                    if param.kind == param.VAR_KEYWORD:
                        if sub_param.kind != param.VAR_KEYWORD:
                            raise AssertionError(f"Parameter {param_name} must be **kwargs in method {name}")
                    # POSITIONAL_OR_KEYWORD to KEYWORD_ONLY is not allowed ( stricter to looser)
                    if param.kind == param.POSITIONAL_OR_KEYWORD and sub_param.kind == param.KEYWORD_ONLY:
                        raise AssertionError(f"Parameter {param_name} kind mismatch in method {name}")

        # Check for extra parameters in method_sig that are not in interface_sig
        for param_name in method_sig.parameters:
            if param_name not in interface_sig.parameters:
                raise AssertionError(f"Method {name} extra parameter {param_name}")

    def __get__(self, instance, owner):
        if instance is None:
            return self.method
        return self.method.__get__(instance, owner)

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)


class overrides:
    def __init__(self, interface_class=None):
        self.interface_class = interface_class

    def __call__(self, method):
        result = OverrideChecker(method, self.interface_class)
        return result

    def __new__(cls, arg=None):
        if callable(arg) and not isinstance(arg, type):
            # @overrides (no parens), arg is the method
            result = OverrideChecker(arg, None)
            return result
        return super().__new__(cls)
