from decimal import Decimal as D, getcontext
getcontext().prec = 50
def pmt(B, i, n):
    if i == 0: return B / n
    return B * i / (1 - (1 + i) ** (-n))
def case(B, n, r, d):
    B = D(B); r = D(r); i = r / 1200
    P0 = pmt(B, i, n); base = P0 * n
    Bd = B * (1 + i) ** d
    fa = pmt(Bd, i, n - d); ft = fa * (n - d)
    io_dur = B * i; ia = pmt(B, i, n - d); it = io_dur * d + ia * (n - d)
    ea = pmt(Bd, i, n); et = ea * n
    print(f'B={B} n={n} r={r} d={d}  i={i}')
    print(f'  P0={P0:.6f}  base total={base:.4f}')
    print(f'  full: Bd={Bd:.6f} acc={Bd-B:.6f} after={fa:.6f} total={ft:.4f} extra={ft-base:.4f}')
    print(f'  io  : during={io_dur:.6f} paid int={io_dur*d:.4f} after={ia:.6f} total={it:.4f} extra={it-base:.4f}')
    print(f'  ext : after={ea:.6f} total={et:.4f} extra={et-base:.4f}')
case(1000000, 300, '4.62', 3)
case(1000000, 300, '4.62', 6)
case(1000000, 300, '4.62', 1)
case(600000, 180, '5', 2)
case(400000, 120, '0', 3)
