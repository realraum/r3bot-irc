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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import json
import requests
import time

from .mail import R3Mail

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('RealRaum')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class RealRaum(callbacks.Plugin):

    """realraum related IRC stuff"""

    threaded = True

    def __init__(self, irc):
        self.__parent = super(RealRaum, self)
        self.__parent.__init__(irc)
        self.orderedAt = 0
        self.mjam_url = None

    def roomstatus(self, irc, msg, args):
        """takes no arguments

        Grap the roomstatus from the space-api and display it.
        """
        resp = requests.get(url="http://realraum.at/status.json")
        data = json.loads(resp.text)

        status = str(data['state']['message'])
        lastChange = data['state']['lastchange']

        irc.reply(status)
    roomstatus = wrap(roomstatus)

    def foodreset(self, irc, msg, args):
        """takes no arguments

        Reset an ongoing order.
        """

        self.mjam_url = None

        irc.reply("Ok, done!")
    foodreset = wrap(foodreset)

    def food(self, irc, msg, args, url):
        """[mjam.net url]

        Lets food happen (maybe).
        """

        channel = msg.args[0]
        sender = msg.nick

        text = "Hi,\n\n %s at %s wants some food! Wanna join in?\n\n" % (
            sender, channel)
        text += "If so, check %s @ OFTC" % (channel)

        if url is None or not url.startswith('http'):
            # no url given:
            if self.mjam_url is not None and time.time() - self.orderedAt < 60 * 60 * 2:
                # no url given and old order not old enough:
                irc.reply("ongoing food order: " + self.mjam_url)
                return
            else:
                # no url given and old order already old:
                self.mjam_url = None
                url = ''
                irc.reply(
                    "let food happen! (please give people some time to reply ...)",
                    prefixNick=False)
        else:
            # url given:
            text += ",\nor this link: " + url
            irc.reply(
                "thanks for the link, now let food happen! (please give people some time to reply ...)",
                prefixNick=False)
            self.mjam_url = url
            self.orderedAt = time.time()

        # regardless of url or no url, poke people now:
        plist = filter(
            lambda x: x != sender and x in irc.state.channels[channel].users,
            self.registryValue('food.listeners', channel)
        )
        persons = ", ".join(plist) + ", "

        irc.reply("Yo " + persons + "want some food? " + url, prefixNick=False)

        text += " ...\n\nCheers, \n  r3bot"
        print(text)

        mail = R3Mail()
        if self.registryValue(
            'food.emails',
            channel) is not None and self.registryValue(
            'food.emails',
            channel) is not '' and len(
            self.registryValue(
                'food.emails',
                channel)) != 0:
            print('sending mail to', self.registryValue('food.emails', channel))
            mail.send(
                '[r3bot] Food?',
                text,
                self.registryValue(
                    'food.emails',
                    channel))

    food = wrap(food, [optional('anything')])

    def foodlisteners(self, irc, msg, args, register):
        """takes register argument

        register or unregister for food command
        """

        channel = msg.args[0]

        if register == 'register':
            listeners = self.registryValue('food.listeners', channel)
            if msg.nick in listeners:
                irc.reply("you are already registered!")
            else:
                listeners.append(msg.nick)
                self.setRegistryValue(
                    'food.listeners', value=listeners, channel=channel)
                irc.reply("you are registered!")
        elif register == 'deregister' or register == 'unregister':
            listeners = self.registryValue('food.listeners', channel)
            if msg.nick in listeners:
                listeners.remove(msg.nick)
                irc.reply("you are unregistered!")
            else:
                irc.reply("you were not registered.")
        else:
            irc.reply("please use register or unregister.", prefixNick=False)

    foodlisteners = wrap(foodlisteners, ['text'])

    def tschunk(self, irc, msg, args):
        """takes no arguments

        I say disco, you say party!
        """
        irc.reply("Yo nicoo, let tschunk happen! :)", prefixNick=False)
    tschunk = wrap(tschunk)

    def raspberryjuice(self, irc, msg, args):
        """takes no arguments

        I say disco, you say party!
        """
        irc.reply("Yo nicoo, let some raspberry juice happen! :)",
                  prefixNick=False)
    raspberryjuice = wrap(raspberryjuice)

    def isPeterTheOneAlreadyRealraumMember(self, irc, msg, args):
        """takes no arguments

        Tell me!
        """
        irc.reply("YES! What a dumb question ...", prefixNick=False)

    ispetertheonealreadyrealraummember = wrap(
        isPeterTheOneAlreadyRealraumMember)

    def sender(self, irc, msg, args):
        """takes no arguments

        Tell me the sender (can be fun!).
        """

        irc.reply(
            "you are " + msg.nick + ", what did you expect?", prefixNick=False)

    sender = wrap(sender)

Class = RealRaum


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
