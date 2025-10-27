# Repository:   https://github.com/PyFundamentals
# File Name:    fundamentals/thread_with_return.py
# Description:  thread class that can return values from a thread
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
# @date: 2024-07-13
# @author: Dieter J Kybelksties

from threading import Thread

from fundamentals.overrides import overrides


class ReturningThread(Thread):
    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs=None,
                 daemon: bool = False):
        if kwargs is None:
            kwargs = {}
        Thread.__init__(self=self,
                        group=group,
                        target=target,
                        name=name,
                        args=args,
                        kwargs=kwargs,
                        daemon=daemon)
        self.__return__ = None

    @overrides(Thread)
    def run(self):
        if self._target is not None:
            self.__return__ = self._target(*self._args, **self._kwargs)

    @overrides(Thread)
    def join(self, timeout=None) -> object:
        Thread.join(self, timeout)
        return self.__return__
