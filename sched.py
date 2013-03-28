import urllib2
import urllib
import argparse
import re
from scrapy import log
from datetime import date


def match_airport(cand):
    if cand is None:
        return None
    else:
        return re.match('[A-Za-z]{3}', cand)


def match_month(cand):
    if cand is None:
        return None
    else:
        return re.match('[0-9]{4}', cand)


def match_day(cand):
    if cand is None:
        return None
    else:
        return re.match('[0-9]{6}', cand)


def send_request(values):
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    log.msg(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument(metavar='FROM', type=str,
                        help='The origin airport code.', dest='from')
    parser.add_argument(metavar='TO', type=str,
                        help='The destination airport code.', dest='to')
    parser.add_argument('-d', '--date', help='The date of the flight.')
    parser.add_argument('-r', '--rtn', help='Return flight or not.')

    args = vars(parser.parse_args())

    whole_year = False

    url = 'http://localhost:6800/schedule.json'
    values = {'project': 'default', 'spider': 'sky'}

    fro = args['from']
    to = args['to']
    if match_airport(fro) and match_airport(to):
        values['from'] = fro
        values['to'] = to
        dat = args['date']
        rtn = args['rtn']
        if rtn:
            values['rtn'] = rtn
        if match_day(dat) or match_month(dat):
            values['date'] = dat
        elif dat == '1':
            whole_year = True
        if not whole_year:
            send_request(values)
        else:
            today = date.today().isoformat().split('-')
            month = today[1]
            year = today[0][-2:]
            for m in range(int(month), 13):
                mnt = str(m)
                if len(mnt) == 1:
                    mnt = '0' + mnt
                values['date'] = year + mnt
                send_request(values)

    else:
        print 'Wrong arguments supplied!'
