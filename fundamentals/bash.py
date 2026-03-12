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
import re
import socket
import subprocess
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


def is_tool_installed(name: str, version: str=None, exact_version: bool =False) -> bool:
    """
    Check if the tool is installed.
    :param name: name of the tool
    :param version: optional version to check
    :param exact_version: if true, then the exact version is checked, otherwise later versions are OK
    :return: True, if tool is installed, False otherwise
    """
    # First check if tool exists
    if which(name) is None:
        return False
    
    # If no version specified, just return True (tool exists)
    if version is None:
        return True
    
    # Try to get the installed version
    installed_version = _get_tool_version(name)
    if installed_version is None:
        return False
    
    # Compare versions
    return _compare_versions(installed_version, version, exact_version)


def _get_tool_version(name: str) -> str | None:
    """
    Get the version of a tool by executing it with common version flags.
    :param name: name of the tool
    :return: version string if found, None otherwise
    """
    # Common version flags to try
    version_flags = ['--version', '-v', '-V', 'version']
    
    for flag in version_flags:
        try:
            # Execute the tool with version flag
            result = subprocess.run([name, flag], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            
            if result.returncode == 0:
                output = result.stdout.strip() or result.stderr.strip()
                if output:
                    # Extract version using regex patterns
                    version = _extract_version_from_output(output)
                    if version:
                        return version
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            continue
    
    return None


def _extract_version_from_output(output: str) -> str | None:
    """
    Extract version number from command output using common patterns.
    :param output: command output string
    :return: version string if found, None otherwise
    """
    # Common version patterns
    patterns = [
        r'version\s*[:\s]*([0-9]+\.[0-9]+(?:\.[0-9]+)*)',  # version 1.2.3
        r'([0-9]+\.[0-9]+(?:\.[0-9]+)*)',                   # standalone version
        r'v([0-9]+\.[0-9]+(?:\.[0-9]+)*)',                  # v1.2.3
        r'Version\s*[:\s]*([0-9]+\.[0-9]+(?:\.[0-9]+)*)',  # Version 1.2.3
    ]
    
    for pattern in patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None


def _compare_versions(installed: str, required: str, exact: bool) -> bool:
    """
    Compare installed version with required version.
    :param installed: installed version string
    :param required: required version string
    :param exact: if True, check for exact match, otherwise check if installed >= required
    :return: True if version requirement is satisfied
    """
    try:
        # Split versions into components
        installed_parts = [int(x) for x in installed.split('.')]
        required_parts = [int(x) for x in required.split('.')]
        
        # Pad shorter version with zeros
        max_len = max(len(installed_parts), len(required_parts))
        installed_parts.extend([0] * (max_len - len(installed_parts)))
        required_parts.extend([0] * (max_len - len(required_parts)))
        
        if exact:
            # Exact version match
            return installed_parts == required_parts
        else:
            # Installed version should be >= required version
            return installed_parts >= required_parts
            
    except (ValueError, AttributeError):
        # If version parsing fails, assume version check cannot be performed
        return False


def assert_tools_installed(tools: (str | list[str])):
    """
    Assert that the whole list of tools is installed
    :param tools: all the tools to check (can be strings or tuples of (tool_name, version, exact_version))
    :raises SystemExit:
    """
    if isinstance(tools, str):
        tools = [tools]
    
    missing_tools = []
    for tool in tools:
        if isinstance(tool, tuple):
            # Tool with version specification: (name, version, exact_version)
            name, version, exact_version = tool
            if not is_tool_installed(name, version, exact_version):
                if version:
                    version_str = f" (version {version}" + (" exact" if exact_version else " or later") + ")"
                else:
                    version_str = ""
                missing_tools.append(f"{name}{version_str}")
        else:
            # Simple tool name
            if not is_tool_installed(tool):
                missing_tools.append(tool)
    
    if len(missing_tools) > 0:
        print(f"Please install the following tools {missing_tools} ",
              "to run this script (or add location to PATH variable)")
        raise SystemExit(f"The following tools are not installed: {missing_tools}.")
