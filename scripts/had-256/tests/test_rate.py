"""Rate limits before an account exists (open an account, password recovery) keep a separate counter per caller
address (Maya: d2b8f349 cast md5(IP) to int, so different addresses could share one bucket). Real WordPress (bench);
the bench lets a test present a synthetic documentation address (RFC 5737: 192.0.2.0/24, 198.51.100.0/24) through
the X-NLJ-IP header, honoured only by the bench mu-plugin.
"""
from bench import reset, record, user, clear
from session import Session

V = 'after'
A, B, C = '192.0.2.1', '192.0.2.3', '198.51.100.1'


def signup(ip):
    return Session(V, ip=ip).post('/owner/account/signup', {'name': 'דנה', 'email': user('dana')['email'], 'password': 'Another-pass-1'}, nonce=False)[0]


def recover(ip):
    return Session(V, ip=ip).post('/owner/account/recover', {'email': 'nobody.%s@example.test' % ip.replace('.', '-')}, nonce=False)[0]


clear('L01', V, 'rate limits per address')
reset(V)
a = [signup(A) for _ in range(6)]
b = signup(B)
c = signup(C)
ok1 = a[:5] == [409] * 5 and a[5] == 429 and b == 409 and c == 409
record({'id': 'L01', 'variant': V, 'label': 'real-wp', 'title': 'rate limits per address: opening an account (5 an hour)', 'status': 'pass' if ok1 else 'fail',
        'evidence': {A: a, B: b, C: c}, 'notes': '409 = the email already has an account (counted); 429 = this address hit its limit; the other addresses are not affected'})
reset(V)
a = [recover(A) for _ in range(6)]
b = recover(B)
c = recover(C)
ok2 = a[:5] == [200] * 5 and a[5] == 429 and b == 200 and c == 200
record({'id': 'L01', 'variant': V, 'label': 'real-wp', 'title': 'rate limits per address: password recovery (5 an hour)', 'status': 'pass' if ok2 else 'fail', 'evidence': {A: a, B: b, C: c}})
