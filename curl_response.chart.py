# -*- coding: utf-8 -*-
# Description: curl response netdata python.d module
# Author: maksokami
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
from bases.FrameworkServices.UrlService import UrlService

priority = 90000

ORDER = [
    'curl_response',
]

CHARTS = {
    'curl_response': {
        'options': [None, 'curl_response', 'milliseconds', None, 'curl.response', 'area'],
        'lines': [
            ['tcp_connect', 'tcp_connect', 'absolute'],
            ['dnslookup', 'dnslookup', 'absolute'],
            ['tls_handshake', 'tls_handshake', 'absolute'],
            ['total', 'total', 'absolute']
        ]
    }
}


def right(v_str, v_char):
    # Return everything to the right of first v_chat encounter in the v_str
    # "test:10" -> "10"
    try:
        char_index = v_str.rfind(v_char)
        if char_index >= 0:
            return v_str[char_index+1:]
        else:
            return v_str
    except Exception:
        return v_str


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.values=dict()
        self.url = configuration.get('url', 'https://www.google.com')

    @staticmethod
    def check():
        return True

    def logMe(self,msg):
        self.debug(msg)

    def _get_curl_response(self):
        # GET RAW DATA
        # Result is in seconds: 0.0943. Convert to ms (x1000)

        MULTIPLIER = 1000 # Convert seconds to milliseconds

        curl_command = [
            "curl",
            "--write-out", "tcp_connect:%{time_connect}|dnslookup:%{time_namelookup}|tls_handshake:%{time_appconnect}|total:%{time_total}\n",
            "--silent",
            "--output", "/dev/null",
            self.url
        ]

        # Indexes of the result list: 0-tcp_connect, 1-dnslookup, 2-tls_hanshake, 3-total
        res = []
        result = subprocess.run(curl_command, capture_output=True, text=True)
      
        # Check if the command was successful
        if result.returncode == 0:
            tmp_list = result.stdout.split("|")
            for item in tmp_list:
                res.append(  float(right(item, ":")))
            return {"tcp_connect":res[0]*MULTIPLIER, "dnslookup": res[1]*MULTIPLIER, "tls_handshake":res[2]*MULTIPLIER, "total":res[3]*MULTIPLIER}
        else:
            return {"tcp_connect":0.0, "dnslookup": 0.0, "tls_handshake":0.0, "total":0.0}

    def _get_data(self):
        tmp_dict = self._get_curl_response()
        return tmp_dict
