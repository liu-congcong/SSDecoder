from base64 import urlsafe_b64decode
from re import compile
from urllib.parse import parse_qsl


def decode_string(string):
    remainder = len(string) % 4
    if remainder:
        string += '=' * (4 - remainder)
    return urlsafe_b64decode(string).decode()


class SSDecoder:

    def __init__(self):
        # ss://method:password@server:port #
        self.ss = compile('([^:]+):([^@]+)@([^:]+):(\d+)')
        self.ss_keys = ('method', 'password', 'server', 'port')
        # ssr://server:port:protocol:method:obfs:password_base64/?params_base64 #
        self.ssr = compile('([^:]+):(\d+):([^:]+):([^:]+):([^:]+):([^:]+)\/\?(.+)')
        self.ssr_keys = ('server', 'port', 'protocol', 'method', 'obfs', 'password', 'remains')
        self.decoder_hash = {'ss': self.decode_ss, 'ssr': self.decode_ssr}
        return None


    def decode_ss(self, string):
        try:
            decoded_string = decode_string(string[5 : ])
        except:
            raise Exception('Can not decode this SS.')
        match_result = self.ss.match(decoded_string)
        assert match_result, 'Can not decode this SS.'
        for key, value in zip(self.ss_keys, match_result.groups()):
            yield (key, value)
        return None


    def decode_ssr(self, string):
        try:
            decoded_string = decode_string(string[6 : ])
        except:
            raise Exception('Can not decode this SSR.')
        match_result = self.ssr.match(decoded_string)
        assert match_result, 'Can not decode this SSR.'
        for key, value in zip(self.ssr_keys, match_result.groups()):
            if key == 'remains':
                for key_, value_ in parse_qsl(value):
                    yield (key_, decode_string(value_))
            else:
                if key == 'password':
                    value = decode_string(value)
                yield (key, value)
        return None


    def decode(self, string, string_type):
        hash = dict()
        for key, value in self.decoder_hash[string_type](string):
            hash[key] = value
            print('{0:>14}: {1}'.format(key, value), flush = True)
        return hash
