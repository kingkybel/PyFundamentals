# Repository:   https://github.com/PyFundamentals
# File Name:    fundamentals/bash.py
# Description:  bash script-like utilities
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

from __future__ import annotations

import os
import socket
import sys
import urllib.request
from getpass import getuser
from multiprocessing import cpu_count
from shutil import which
from socket import gethostname

from fundamentals.string_utils import squeeze_chars, Encodings


def get_effective_user() -> str:
    """
    Retrieve the user ID of the currently executing user.
    :return: the current user ID
    """
    return getuser()


def get_logged_in_user() -> str:
    """
    Get the currently logged-in user
    :return: the username
    """
    try:
        return os.getlogin()
    except FileNotFoundError:  # happens on WSL
        return squeeze_chars(source=os.popen("whoami").read(), squeeze_set="\n\t\r ")
    except OSError:  # happens on docker
        return squeeze_chars(source=os.popen("whoami").read(), squeeze_set="\n\t\r ")


def assert_is_root():
    """
    Assert that the script is run with root privileges
    :raise SystemExit:
    """
    if get_effective_user() != "root":
        print("This script needs to be run with root privileges.")
        print(f"Try: sudo {which('python')} {' '.join(sys.argv)}")
        raise SystemExit("This script needs to be run with root privileges.")


def number_of_cores() -> int:
    """
    Get the number of available cores
    :return: the number of cores
    """
    return int(cpu_count())


def hostname() -> str:
    """
    Get the hostname.
    :return: the hostname
    """
    return gethostname()


def get_ip() -> str:
    """
    Get the IP address
    :return: the IP address of this machine, if connected, default localhost address otherwise
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't have to be reachable
        s.connect(("10.254.254.254", 1))
        ip = s.getsockname()[0]
    except socket.error:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def get_external_ip() -> str:
    """
    Get the external IP address
    :return: the external IP address, if connected
    """
    return urllib.request.urlopen("https://ident.me").read().decode(str(Encodings.UTF8))


def is_tool_installed(name: str) -> bool:
    """
    Check if the tool is installed.
    :param name: name of the tool
    :return: True, if tool is installed, False otherwise
    """
    return which(name) is not None


def assert_tools_installed(tools: (str | list[str])):
    """
    Assert that the whole list of tools is installed
    :param tools: all the tools to check
    :raises SystemExit:
    """
    if isinstance(tools, str):
        tools = [tools]
    missing_tools = []
    for tool in tools:
        if not is_tool_installed(tool):
            missing_tools.append(tool)
    if len(missing_tools) > 0:
        print(f"Please install the following tools {missing_tools} ",
              "to run this script (or add location to PATH variable)")
        raise SystemExit(f"The following tools are not installed: {missing_tools}.")
