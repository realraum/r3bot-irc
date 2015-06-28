###
# Copyright (c) 2015, verr
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

from supybot.test import *


class RealRaumTestCase(PluginTestCase):
    plugins = ('RealRaum',)

    def tearDown(self):
        conf.supybot.plugins.RealRaum.food.listeners.setValue([])
        PluginTestCase.tearDown(self)

    def testRoomstatus1(self):
        self.assertNotError('roomstatus')

    def testFood1(self):
        self.assertNotError('food')

    def testTschunk1(self):
        self.assertNotError('tschunk')

    def testIsPeter(self):
        self.assertNotError('ispetertheonealreadyrealraummember')

    def testSender1(self):
        self.assertNotError('sender')

    def testSender2(self):
        self.assertError('sender me')

    def testFoodlisteners(self):
        self.assertNotError('foodlisteners register')
        self.assertNotError('foodlisteners unregister')
        self.assertNotError('foodlisteners deregister')

    def testFoodlistenersRegister(self):
        listenersBefore = conf.supybot.plugins.RealRaum.food.listeners()[:]
        self.assertRegexp('foodlisteners register', '.*you are registered!')
        listenersAfter = conf.supybot.plugins.RealRaum.food.listeners()[:]
        self.failIf(listenersBefore == listenersAfter, 'failed to add nick to listeners')

        self.assertRegexp('foodlisteners register', '.*you are already registered!')

    def testFoodlistenersUnregister(self):
        self.assertNotError('foodlisteners register')
        self.assertRegexp('foodlisteners unregister', '.*you are unregistered!')
        self.assertNotError('foodlisteners register')
        self.assertRegexp('foodlisteners deregister', '.*you are unregistered!')

        self.assertRegexp('foodlisteners unregister', '.*you were not registered.')
        self.assertRegexp('foodlisteners deregister', '.*you were not registered.')


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
