#pip install monero
from config import *
from monero.base58 import _hexToBin as hextobin
#var der = generate_key_derivation(pub, sec)
#var pubkey = derive_public_key(der, i, spk)
def ge_frombytes_vartime(key):
    return False
'''
function Ia(a, b) {
    a = a | 0;
    b = b | 0;
    var c = 0
        , d = 0
        , e = 0
        , f = 0
        , g = 0
        , h = 0
        , j = 0
        , k = 0
        , l = 0
        , m = 0
        , n = 0
        , o = 0
        , p = 0
        , q = 0
        , r = 0
        , s = 0
        , t = 0
        , u = 0
        , v = 0
        , w = 0
        , x = 0
        , y = 0
        , z = 0
        , A = 0
        , B = 0
        , C = 0
        , E = 0
        , F = 0
        , G = 0
        , H = 0
        , I = 0
        , J = 0
        , K = 0
        , L = 0
        , M = 0
        , N = 0
        , O = 0
        , P = 0
        , Q = 0
        , R = 0
        , S = 0
        , T = 0
        , U = 0
        , V = 0
        , W = 0
        , X = 0
        , Y = 0
        , Z = 0
        , _ = 0
        , $ = 0
        , aa = 0
        , ba = 0
        , ca = 0
        , da = 0
        , ea = 0
        , ha = 0
        , ia = 0
        , ja = 0
        , ka = 0
        , la = 0
        , ma = 0
        , na = 0
        , oa = 0
        , pa = 0;
    h = i;
    i = i + 192 | 0;
    f = h + 160 | 0;
    c = h + 120 | 0;
    t = h + 80 | 0;
    d = h + 40 | 0;
    e = h;
    k = fa(b >> 0 | 0, 1, 0, 1) | 0 | 0;
    m = kb(fa(b + 1 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    l = D;
    oa = kb(fa(b + 2 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 16) | 0;
    l = l | D;
    B = kb(fa(b + 3 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 24) | 0;
    B = m | k | oa | B;
    l = l | D;
    oa = fa(b + 6 >> 0 | 0, 1, 0, 0) | 0 | 0;
    k = fa(b + 4 >> 0 | 0, 1, 0, 1) | 0 | 0;
    m = kb(fa(b + 5 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    pa = D;
    oa = kb(oa & 255 | 0, 0, 16) | 0;
    oa = m | k | oa;
    pa = pa | D;
    k = kb(oa | 0, pa | 0, 6) | 0;
    m = D;
    n = fa(b + 9 >> 0 | 0, 1, 0, 0) | 0 | 0;
    ma = fa(b + 7 >> 0 | 0, 1, 0, 1) | 0 | 0;
    o = kb(fa(b + 8 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    p = D;
    n = kb(n & 255 | 0, 0, 16) | 0;
    n = o | ma | n;
    p = p | D;
    ma = fa(b + 12 >> 0 | 0, 1, 0, 0) | 0 | 0;
    o = fa(b + 10 >> 0 | 0, 1, 0, 1) | 0 | 0;
    A = kb(fa(b + 11 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    na = D;
    ma = kb(ma & 255 | 0, 0, 16) | 0;
    ma = A | o | ma;
    na = na | D;
    o = kb(ma | 0, na | 0, 3) | 0;
    A = D;
    z = fa(b + 15 >> 0 | 0, 1, 0, 0) | 0 | 0;
    ka = fa(b + 13 >> 0 | 0, 1, 0, 1) | 0 | 0;
    u = kb(fa(b + 14 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    x = D;
    z = kb(z & 255 | 0, 0, 16) | 0;
    z = u | ka | z;
    x = x | D;
    ka = fa(b + 16 >> 0 | 0, 1, 0, 1) | 0 | 0;
    u = kb(fa(b + 17 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    w = D;
    j = kb(fa(b + 18 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 16) | 0;
    w = w | D;
    y = kb(fa(b + 19 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 24) | 0;
    y = u | ka | j | y;
    w = w | D;
    j = fa(b + 22 >> 0 | 0, 1, 0, 0) | 0 | 0;
    ka = fa(b + 20 >> 0 | 0, 1, 0, 1) | 0 | 0;
    u = kb(fa(b + 21 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    s = D;
    j = kb(j & 255 | 0, 0, 16) | 0;
    j = u | ka | j;
    s = s | D;
    ka = fa(b + 25 >> 0 | 0, 1, 0, 0) | 0 | 0;
    u = fa(b + 23 >> 0 | 0, 1, 0, 1) | 0 | 0;
    r = kb(fa(b + 24 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    la = D;
    ka = kb(ka & 255 | 0, 0, 16) | 0;
    ka = r | u | ka;
    la = la | D;
    u = kb(ka | 0, la | 0, 5) | 0;
    r = D;
    q = fa(b + 28 >> 0 | 0, 1, 0, 0) | 0 | 0;
    g = fa(b + 26 >> 0 | 0, 1, 0, 1) | 0 | 0;
    ja = kb(fa(b + 27 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    v = D;
    q = kb(q & 255 | 0, 0, 16) | 0;
    q = ja | g | q;
    v = v | D;
    g = b + 31 | 0;
    ja = fa(g >> 0 | 0, 1, 0, 0) | 0 | 0;
    ia = fa(b + 29 >> 0 | 0, 1, 0, 1) | 0 | 0;
    ha = kb(fa(b + 30 >> 0 | 0, 1, 0, 1) | 0 | 0 | 0, 0, 8) | 0;
    b = D;
    ja = kb(ja & 255 | 0, 0, 16) | 0;
    b = kb(ha | ia | ja | 0, b | D | 0, 2) | 0;
    b = b & 33554428;
    if ((b | 0) == 33554428 & 0 == 0 & ((q | 0) == 16777215 & (v | 0) == 0) & ((ka | 0) == 16777215 & (la | 0) == 0) & ((j | 0) == 16777215 & (s | 0) == 0) & ((y | 0) == -1 & (w | 0) == 0) & ((z | 0) == 16777215 & (x | 0) == 0) & ((ma | 0) == 16777215 & (na | 0) == 0) & ((n | 0) == 16777215 & (p | 0) == 0) & ((oa | 0) == 16777215 & (pa | 0) == 0) & (l >>> 0 > 0 | (l | 0) == 0 & B >>> 0 > 4294967276)) {
        pa = -1;
        i = h;
        return pa | 0
    }
    ba = kb(n | 0, p | 0, 5) | 0;
    oa = D;
    pa = kb(z | 0, x | 0, 2) | 0;
    da = D;
    ca = kb(j | 0, s | 0, 7) | 0;
    ia = D;
    j = kb(q | 0, v | 0, 4) | 0;
    ja = D;
    ha = hb(b | 0, 0, 16777216, 0) | 0;
    ha = jb(ha | 0, D | 0, 25) | 0;
    ea = D;
    ma = sb(ha | 0, ea | 0, 19, 0) | 0;
    ma = hb(ma | 0, D | 0, B | 0, l | 0) | 0;
    $ = D;
    ea = kb(ha | 0, ea | 0, 25) | 0;
    ha = D;
    la = hb(k | 0, m | 0, 16777216, 0) | 0;
    la = jb(la | 0, D | 0, 25) | 0;
    Y = D;
    oa = hb(ba | 0, oa | 0, la | 0, Y | 0) | 0;
    ba = D;
    Y = kb(la | 0, Y | 0, 25) | 0;
    Y = gb(k | 0, m | 0, Y | 0, D | 0) | 0;
    la = D;
    na = hb(o | 0, A | 0, 16777216, 0) | 0;
    na = jb(na | 0, D | 0, 25) | 0;
    _ = D;
    k = hb(pa | 0, da | 0, na | 0, _ | 0) | 0;
    da = D;
    _ = kb(na | 0, _ | 0, 25) | 0;
    na = D;
    pa = hb(y | 0, w | 0, 16777216, 0) | 0;
    pa = jb(pa | 0, D | 0, 25) | 0;
    aa = D;
    v = hb(ca | 0, ia | 0, pa | 0, aa | 0) | 0;
    ia = D;
    aa = kb(pa | 0, aa | 0, 25) | 0;
    pa = D;
    l = hb(u | 0, r | 0, 16777216, 0) | 0;
    l = jb(l | 0, D | 0, 25) | 0;
    ca = D;
    ja = hb(j | 0, ja | 0, l | 0, ca | 0) | 0;
    j = D;
    ca = kb(l | 0, ca | 0, 25) | 0;
    l = D;
    Z = hb(ma | 0, $ | 0, 33554432, 0) | 0;
    Z = fb(Z | 0, D | 0, 26) | 0;
    ka = D;
    la = hb(Y | 0, la | 0, Z | 0, ka | 0) | 0;
    ka = kb(Z | 0, ka | 0, 26) | 0;
    ka = gb(ma | 0, $ | 0, ka | 0, D | 0) | 0;
    $ = hb(oa | 0, ba | 0, 33554432, 0) | 0;
    $ = fb($ | 0, D | 0, 26) | 0;
    ma = D;
    Z = hb($ | 0, ma | 0, o | 0, A | 0) | 0;
    na = gb(Z | 0, D | 0, _ | 0, na | 0) | 0;
    ma = kb($ | 0, ma | 0, 26) | 0;
    ma = gb(oa | 0, ba | 0, ma | 0, D | 0) | 0;
    ba = hb(k | 0, da | 0, 33554432, 0) | 0;
    ba = fb(ba | 0, D | 0, 26) | 0;
    oa = D;
    $ = hb(ba | 0, oa | 0, y | 0, w | 0) | 0;
    pa = gb($ | 0, D | 0, aa | 0, pa | 0) | 0;
    oa = kb(ba | 0, oa | 0, 26) | 0;
    oa = gb(k | 0, da | 0, oa | 0, D | 0) | 0;
    da = hb(v | 0, ia | 0, 33554432, 0) | 0;
    da = fb(da | 0, D | 0, 26) | 0;
    k = D;
    u = hb(da | 0, k | 0, u | 0, r | 0) | 0;
    l = gb(u | 0, D | 0, ca | 0, l | 0) | 0;
    k = kb(da | 0, k | 0, 26) | 0;
    k = gb(v | 0, ia | 0, k | 0, D | 0) | 0;
    ia = hb(ja | 0, j | 0, 33554432, 0) | 0;
    ia = fb(ia | 0, D | 0, 26) | 0;
    v = D;
    u = hb(b | 0, 0, ia | 0, v | 0) | 0;
    u = gb(u | 0, D | 0, ea | 0, ha | 0) | 0;
    v = kb(ia | 0, v | 0, 26) | 0;
    v = gb(ja | 0, j | 0, v | 0, D | 0) | 0;
    j = a + 40 | 0;
    ga(j | 0, ka | 0, 4, 0);
    ga(a + 44 | 0, la | 0, 4, 0);
    ga(a + 48 | 0, ma | 0, 4, 0);
    ga(a + 52 | 0, na | 0, 4, 0);
    ga(a + 56 | 0, oa | 0, 4, 0);
    ga(a + 60 | 0, pa | 0, 4, 0);
    ga(a + 64 | 0, k | 0, 4, 0);
    ga(a + 68 | 0, l | 0, 4, 0);
    ga(a + 72 | 0, v | 0, 4, 0);
    ga(a + 76 | 0, u | 0, 4, 0);
    u = a + 80 | 0;
    ga(u | 0, 1 | 0, 4, 0);
    v = a + 84 | 0;
    l = v + 0 | 0;
    k = l + 36 | 0;
    do {
        ga(l | 0, 0 | 0, 4, 0);
        l = l + 4 | 0
    } while ((l | 0) < (k | 0));
    Ja(c, j);
    ya(t, c, 240);
    r = c + 4 | 0;
    s = c + 8 | 0;
    k = c + 12 | 0;
    l = c + 16 | 0;
    m = c + 20 | 0;
    n = c + 24 | 0;
    o = c + 28 | 0;
    p = c + 32 | 0;
    q = c + 36 | 0;
    E = fa(u | 0, 4, 0, 0) | 0 | 0;
    oa = fa(v | 0, 4, 0, 0) | 0 | 0;
    ca = fa(a + 88 | 0, 4, 0, 0) | 0 | 0;
    I = fa(a + 92 | 0, 4, 0, 0) | 0 | 0;
    G = fa(a + 96 | 0, 4, 0, 0) | 0 | 0;
    C = fa(a + 100 | 0, 4, 0, 0) | 0 | 0;
    B = fa(a + 104 | 0, 4, 0, 0) | 0 | 0;
    z = fa(a + 108 | 0, 4, 0, 0) | 0 | 0;
    x = fa(a + 112 | 0, 4, 0, 0) | 0 | 0;
    v = fa(a + 116 | 0, 4, 0, 0) | 0 | 0;
    w = (fa(r | 0, 4, 0, 0) | 0 | 0) - oa | 0;
    y = (fa(s | 0, 4, 0, 0) | 0 | 0) - ca | 0;
    A = (fa(k | 0, 4, 0, 0) | 0 | 0) - I | 0;
    b = (fa(l | 0, 4, 0, 0) | 0 | 0) - G | 0;
    F = (fa(m | 0, 4, 0, 0) | 0 | 0) - C | 0;
    H = (fa(n | 0, 4, 0, 0) | 0 | 0) - B | 0;
    V = (fa(o | 0, 4, 0, 0) | 0 | 0) - z | 0;
    pa = (fa(p | 0, 4, 0, 0) | 0 | 0) - x | 0;
    J = (fa(q | 0, 4, 0, 0) | 0 | 0) - v | 0;
    ga(c | 0, (fa(c | 0, 4, 0, 0) | 0 | 0) - E | 0, 4, 0);
    ga(r | 0, w | 0, 4, 0);
    ga(s | 0, y | 0, 4, 0);
    ga(k | 0, A | 0, 4, 0);
    ga(l | 0, b | 0, 4, 0);
    ga(m | 0, F | 0, 4, 0);
    ga(n | 0, H | 0, 4, 0);
    ga(o | 0, V | 0, 4, 0);
    ga(p | 0, pa | 0, 4, 0);
    ga(q | 0, J | 0, 4, 0);
    J = t + 4 | 0;
    pa = t + 8 | 0;
    V = t + 12 | 0;
    H = t + 16 | 0;
    F = t + 20 | 0;
    b = t + 24 | 0;
    A = t + 28 | 0;
    y = t + 32 | 0;
    w = t + 36 | 0;
    oa = oa + (fa(J | 0, 4, 0, 0) | 0 | 0) | 0;
    ca = ca + (fa(pa | 0, 4, 0, 0) | 0 | 0) | 0;
    I = I + (fa(V | 0, 4, 0, 0) | 0 | 0) | 0;
    G = G + (fa(H | 0, 4, 0, 0) | 0 | 0) | 0;
    C = C + (fa(F | 0, 4, 0, 0) | 0 | 0) | 0;
    B = B + (fa(b | 0, 4, 0, 0) | 0 | 0) | 0;
    z = z + (fa(A | 0, 4, 0, 0) | 0 | 0) | 0;
    x = x + (fa(y | 0, 4, 0, 0) | 0 | 0) | 0;
    v = v + (fa(w | 0, 4, 0, 0) | 0 | 0) | 0;
    ga(t | 0, E + (fa(t | 0, 4, 0, 0) | 0 | 0) | 0, 4, 0);
    ga(J | 0, oa | 0, 4, 0);
    ga(pa | 0, ca | 0, 4, 0);
    ga(V | 0, I | 0, 4, 0);
    ga(H | 0, G | 0, 4, 0);
    ga(F | 0, C | 0, 4, 0);
    ga(b | 0, B | 0, 4, 0);
    ga(A | 0, z | 0, 4, 0);
    ga(y | 0, x | 0, 4, 0);
    ga(w | 0, v | 0, 4, 0);
    Ka(a, c, t);
    Ja(d, a);
    ya(d, d, t);
    v = d + 4 | 0;
    w = d + 8 | 0;
    x = d + 12 | 0;
    y = d + 16 | 0;
    z = d + 20 | 0;
    A = d + 24 | 0;
    B = d + 28 | 0;
    b = d + 32 | 0;
    C = d + 36 | 0;
    F = (fa(v | 0, 4, 0, 0) | 0 | 0) - (fa(r | 0, 4, 0, 0) | 0 | 0) | 0;
    G = (fa(w | 0, 4, 0, 0) | 0 | 0) - (fa(s | 0, 4, 0, 0) | 0 | 0) | 0;
    H = (fa(x | 0, 4, 0, 0) | 0 | 0) - (fa(k | 0, 4, 0, 0) | 0 | 0) | 0;
    I = (fa(y | 0, 4, 0, 0) | 0 | 0) - (fa(l | 0, 4, 0, 0) | 0 | 0) | 0;
    V = (fa(z | 0, 4, 0, 0) | 0 | 0) - (fa(m | 0, 4, 0, 0) | 0 | 0) | 0;
    ca = (fa(A | 0, 4, 0, 0) | 0 | 0) - (fa(n | 0, 4, 0, 0) | 0 | 0) | 0;
    pa = (fa(B | 0, 4, 0, 0) | 0 | 0) - (fa(o | 0, 4, 0, 0) | 0 | 0) | 0;
    oa = (fa(b | 0, 4, 0, 0) | 0 | 0) - (fa(p | 0, 4, 0, 0) | 0 | 0) | 0;
    J = (fa(C | 0, 4, 0, 0) | 0 | 0) - (fa(q | 0, 4, 0, 0) | 0 | 0) | 0;
    ga(e | 0, (fa(d | 0, 4, 0, 0) | 0 | 0) - (fa(c | 0, 4, 0, 0) | 0 | 0) | 0, 4, 0);
    E = e + 4 | 0;
    ga(E | 0, F | 0, 4, 0);
    F = e + 8 | 0;
    ga(F | 0, G | 0, 4, 0);
    G = e + 12 | 0;
    ga(G | 0, H | 0, 4, 0);
    H = e + 16 | 0;
    ga(H | 0, I | 0, 4, 0);
    I = e + 20 | 0;
    ga(I | 0, V | 0, 4, 0);
    V = e + 24 | 0;
    ga(V | 0, ca | 0, 4, 0);
    ca = e + 28 | 0;
    ga(ca | 0, pa | 0, 4, 0);
    pa = e + 32 | 0;
    ga(pa | 0, oa | 0, 4, 0);
    oa = e + 36 | 0;
    ga(oa | 0, J | 0, 4, 0);
    Oa(f, e);
    J = f + 1 | 0;
    K = f + 2 | 0;
    L = f + 3 | 0;
    M = f + 4 | 0;
    N = f + 5 | 0;
    O = f + 6 | 0;
    P = f + 7 | 0;
    Q = f + 8 | 0;
    R = f + 9 | 0;
    S = f + 10 | 0;
    T = f + 11 | 0;
    U = f + 12 | 0;
    u = f + 13 | 0;
    W = f + 14 | 0;
    X = f + 15 | 0;
    Y = f + 16 | 0;
    Z = f + 17 | 0;
    _ = f + 18 | 0;
    $ = f + 19 | 0;
    aa = f + 20 | 0;
    ba = f + 21 | 0;
    t = f + 22 | 0;
    da = f + 23 | 0;
    ea = f + 24 | 0;
    ha = f + 25 | 0;
    ia = f + 26 | 0;
    ja = f + 27 | 0;
    ka = f + 28 | 0;
    la = f + 29 | 0;
    ma = f + 30 | 0;
    na = f + 31 | 0;
    do {
        if (!((((fa(J >> 0 | 0, 1, 0, 0) | 0 | (fa(f >> 0 | 0, 1, 0, 0) | 0) | (fa(K >> 0 | 0, 1, 0, 0) | 0) | (fa(L >> 0 | 0, 1, 0, 0) | 0) | (fa(M >> 0 | 0, 1, 0, 0) | 0) | (fa(N >> 0 | 0, 1, 0, 0) | 0) | (fa(O >> 0 | 0, 1, 0, 0) | 0) | (fa(P >> 0 | 0, 1, 0, 0) | 0) | (fa(Q >> 0 | 0, 1, 0, 0) | 0) | (fa(R >> 0 | 0, 1, 0, 0) | 0) | (fa(S >> 0 | 0, 1, 0, 0) | 0) | (fa(T >> 0 | 0, 1, 0, 0) | 0) | (fa(U >> 0 | 0, 1, 0, 0) | 0) | (fa(u >> 0 | 0, 1, 0, 0) | 0) | (fa(W >> 0 | 0, 1, 0, 0) | 0) | (fa(X >> 0 | 0, 1, 0, 0) | 0) | (fa(Y >> 0 | 0, 1, 0, 0) | 0) | (fa(Z >> 0 | 0, 1, 0, 0) | 0) | (fa(_ >> 0 | 0, 1, 0, 0) | 0) | (fa($ >> 0 | 0, 1, 0, 0) | 0) | (fa(aa >> 0 | 0, 1, 0, 0) | 0) | (fa(ba >> 0 | 0, 1, 0, 0) | 0) | (fa(t >> 0 | 0, 1, 0, 0) | 0) | (fa(da >> 0 | 0, 1, 0, 0) | 0) | (fa(ea >> 0 | 0, 1, 0, 0) | 0) | (fa(ha >> 0 | 0, 1, 0, 0) | 0) | (fa(ia >> 0 | 0, 1, 0, 0) | 0) | (fa(ja >> 0 | 0, 1, 0, 0) | 0) | (fa(ka >> 0 | 0, 1, 0, 0) | 0) | (fa(la >> 0 | 0, 1, 0, 0) | 0) | (fa(ma >> 0 | 0, 1, 0, 0) | 0) | (fa(na >> 0 | 0, 1, 0, 0) | 0)) & 255) + -1 & -256 | 0) == -256)) {
            v = (fa(r | 0, 4, 0, 0) | 0 | 0) + (fa(v | 0, 4, 0, 0) | 0 | 0) | 0;
            w = (fa(s | 0, 4, 0, 0) | 0 | 0) + (fa(w | 0, 4, 0, 0) | 0 | 0) | 0;
            x = (fa(k | 0, 4, 0, 0) | 0 | 0) + (fa(x | 0, 4, 0, 0) | 0 | 0) | 0;
            y = (fa(l | 0, 4, 0, 0) | 0 | 0) + (fa(y | 0, 4, 0, 0) | 0 | 0) | 0;
            z = (fa(m | 0, 4, 0, 0) | 0 | 0) + (fa(z | 0, 4, 0, 0) | 0 | 0) | 0;
            A = (fa(n | 0, 4, 0, 0) | 0 | 0) + (fa(A | 0, 4, 0, 0) | 0 | 0) | 0;
            B = (fa(o | 0, 4, 0, 0) | 0 | 0) + (fa(B | 0, 4, 0, 0) | 0 | 0) | 0;
            b = (fa(p | 0, 4, 0, 0) | 0 | 0) + (fa(b | 0, 4, 0, 0) | 0 | 0) | 0;
            C = (fa(q | 0, 4, 0, 0) | 0 | 0) + (fa(C | 0, 4, 0, 0) | 0 | 0) | 0;
            ga(e | 0, (fa(c | 0, 4, 0, 0) | 0 | 0) + (fa(d | 0, 4, 0, 0) | 0 | 0) | 0, 4, 0);
            ga(E | 0, v | 0, 4, 0);
            ga(F | 0, w | 0, 4, 0);
            ga(G | 0, x | 0, 4, 0);
            ga(H | 0, y | 0, 4, 0);
            ga(I | 0, z | 0, 4, 0);
            ga(V | 0, A | 0, 4, 0);
            ga(ca | 0, B | 0, 4, 0);
            ga(pa | 0, b | 0, 4, 0);
            ga(oa | 0, C | 0, 4, 0);
            Oa(f, e);
            if ((((fa(J >> 0 | 0, 1, 0, 0) | 0 | (fa(f >> 0 | 0, 1, 0, 0) | 0) | (fa(K >> 0 | 0, 1, 0, 0) | 0) | (fa(L >> 0 | 0, 1, 0, 0) | 0) | (fa(M >> 0 | 0, 1, 0, 0) | 0) | (fa(N >> 0 | 0, 1, 0, 0) | 0) | (fa(O >> 0 | 0, 1, 0, 0) | 0) | (fa(P >> 0 | 0, 1, 0, 0) | 0) | (fa(Q >> 0 | 0, 1, 0, 0) | 0) | (fa(R >> 0 | 0, 1, 0, 0) | 0) | (fa(S >> 0 | 0, 1, 0, 0) | 0) | (fa(T >> 0 | 0, 1, 0, 0) | 0) | (fa(U >> 0 | 0, 1, 0, 0) | 0) | (fa(u >> 0 | 0, 1, 0, 0) | 0) | (fa(W >> 0 | 0, 1, 0, 0) | 0) | (fa(X >> 0 | 0, 1, 0, 0) | 0) | (fa(Y >> 0 | 0, 1, 0, 0) | 0) | (fa(Z >> 0 | 0, 1, 0, 0) | 0) | (fa(_ >> 0 | 0, 1, 0, 0) | 0) | (fa($ >> 0 | 0, 1, 0, 0) | 0) | (fa(aa >> 0 | 0, 1, 0, 0) | 0) | (fa(ba >> 0 | 0, 1, 0, 0) | 0) | (fa(t >> 0 | 0, 1, 0, 0) | 0) | (fa(da >> 0 | 0, 1, 0, 0) | 0) | (fa(ea >> 0 | 0, 1, 0, 0) | 0) | (fa(ha >> 0 | 0, 1, 0, 0) | 0) | (fa(ia >> 0 | 0, 1, 0, 0) | 0) | (fa(ja >> 0 | 0, 1, 0, 0) | 0) | (fa(ka >> 0 | 0, 1, 0, 0) | 0) | (fa(la >> 0 | 0, 1, 0, 0) | 0) | (fa(ma >> 0 | 0, 1, 0, 0) | 0) | (fa(na >> 0 | 0, 1, 0, 0) | 0)) & 255) + -1 & -256 | 0) == -256) {
                ya(a, a, 280);
                break
            } else {
                pa = -1;
                i = h;
                return pa | 0
            }
        }
    } while (0);
    Oa(f, a);
    do {
        if (((fa(f >> 0 | 0, 1, 0, 0) | 0) & 1 | 0) != ((fa(g >> 0 | 0, 1, 0, 1) | 0 | 0) >>> 7 | 0)) {
            Oa(f, a);
            if ((((fa(J >> 0 | 0, 1, 0, 0) | 0 | (fa(f >> 0 | 0, 1, 0, 0) | 0) | (fa(K >> 0 | 0, 1, 0, 0) | 0) | (fa(L >> 0 | 0, 1, 0, 0) | 0) | (fa(M >> 0 | 0, 1, 0, 0) | 0) | (fa(N >> 0 | 0, 1, 0, 0) | 0) | (fa(O >> 0 | 0, 1, 0, 0) | 0) | (fa(P >> 0 | 0, 1, 0, 0) | 0) | (fa(Q >> 0 | 0, 1, 0, 0) | 0) | (fa(R >> 0 | 0, 1, 0, 0) | 0) | (fa(S >> 0 | 0, 1, 0, 0) | 0) | (fa(T >> 0 | 0, 1, 0, 0) | 0) | (fa(U >> 0 | 0, 1, 0, 0) | 0) | (fa(u >> 0 | 0, 1, 0, 0) | 0) | (fa(W >> 0 | 0, 1, 0, 0) | 0) | (fa(X >> 0 | 0, 1, 0, 0) | 0) | (fa(Y >> 0 | 0, 1, 0, 0) | 0) | (fa(Z >> 0 | 0, 1, 0, 0) | 0) | (fa(_ >> 0 | 0, 1, 0, 0) | 0) | (fa($ >> 0 | 0, 1, 0, 0) | 0) | (fa(aa >> 0 | 0, 1, 0, 0) | 0) | (fa(ba >> 0 | 0, 1, 0, 0) | 0) | (fa(t >> 0 | 0, 1, 0, 0) | 0) | (fa(da >> 0 | 0, 1, 0, 0) | 0) | (fa(ea >> 0 | 0, 1, 0, 0) | 0) | (fa(ha >> 0 | 0, 1, 0, 0) | 0) | (fa(ia >> 0 | 0, 1, 0, 0) | 0) | (fa(ja >> 0 | 0, 1, 0, 0) | 0) | (fa(ka >> 0 | 0, 1, 0, 0) | 0) | (fa(la >> 0 | 0, 1, 0, 0) | 0) | (fa(ma >> 0 | 0, 1, 0, 0) | 0) | (fa(na >> 0 | 0, 1, 0, 0) | 0)) & 255) + -1 & -256 | 0) == -256) {
                pa = -1;
                i = h;
                return pa | 0
            } else {
                Y = a + 4 | 0;
                _ = a + 8 | 0;
                aa = a + 12 | 0;
                ca = a + 16 | 0;
                ea = a + 20 | 0;
                ia = a + 24 | 0;
                ka = a + 28 | 0;
                ma = a + 32 | 0;
                oa = a + 36 | 0;
                Z = 0 - (fa(Y | 0, 4, 0, 0) | 0 | 0) | 0;
                $ = 0 - (fa(_ | 0, 4, 0, 0) | 0 | 0) | 0;
                ba = 0 - (fa(aa | 0, 4, 0, 0) | 0 | 0) | 0;
                da = 0 - (fa(ca | 0, 4, 0, 0) | 0 | 0) | 0;
                ha = 0 - (fa(ea | 0, 4, 0, 0) | 0 | 0) | 0;
                ja = 0 - (fa(ia | 0, 4, 0, 0) | 0 | 0) | 0;
                la = 0 - (fa(ka | 0, 4, 0, 0) | 0 | 0) | 0;
                na = 0 - (fa(ma | 0, 4, 0, 0) | 0 | 0) | 0;
                pa = 0 - (fa(oa | 0, 4, 0, 0) | 0 | 0) | 0;
                ga(a | 0, 0 - (fa(a | 0, 4, 0, 0) | 0 | 0) | 0, 4, 0);
                ga(Y | 0, Z | 0, 4, 0);
                ga(_ | 0, $ | 0, 4, 0);
                ga(aa | 0, ba | 0, 4, 0);
                ga(ca | 0, da | 0, 4, 0);
                ga(ea | 0, ha | 0, 4, 0);
                ga(ia | 0, ja | 0, 4, 0);
                ga(ka | 0, la | 0, 4, 0);
                ga(ma | 0, na | 0, 4, 0);
                ga(oa | 0, pa | 0, 4, 0);
                break
            }
        }
    } while (0);
    ya(a + 120 | 0, a, j);
    pa = 0;
    i = h;
    return pa | 0
}
'''
def generate_key_derivation(pub, sec):
    if len(pub) != 64 or len(sec) != 64:
        print("Invalid input length")
        return
    pub_b = hextobin(pub)
    sec_b = hextobin(sec)
    print('pub',pub) #extra
    print('pub_b',pub_b)
    print('sec',sec) #private_view_key
    print('sec_b',sec_b)
    ge_p3_b = ge_frombytes_vartime(pub_b)
    print(test_ge_p3_b)
    return True

'''
this.generate_key_derivation = function(pub, sec) {
    if (pub.length !== 64 || sec.length !== 64) {
        throw "Invalid input length";
    }
    var pub_b = hextobin(pub);
    var sec_b = hextobin(sec);
    var pub_m = Module._malloc(KEY_SIZE);
    Module.HEAPU8.set(pub_b, pub_m);
    var sec_m = Module._malloc(KEY_SIZE);
    Module.HEAPU8.set(sec_b, sec_m);
    var ge_p3_m = Module._malloc(STRUCT_SIZES.GE_P3);
    var ge_p2_m = Module._malloc(STRUCT_SIZES.GE_P2);
    var ge_p1p1_m = Module._malloc(STRUCT_SIZES.GE_P1P1);
    if (Module.ccall("ge_frombytes_vartime", "bool", ["number", "number"], [ge_p3_m, pub_m]) !== 0) {
        throw "ge_frombytes_vartime returned non-zero error code";
    }
    Module.ccall("ge_scalarmult", "void", ["number", "number", "number"], [ge_p2_m, sec_m, ge_p3_m]);
    Module.ccall("ge_mul8", "void", ["number", "number"], [ge_p1p1_m, ge_p2_m]);
    Module.ccall("ge_p1p1_to_p2", "void", ["number", "number"], [ge_p2_m, ge_p1p1_m]);
    var derivation_m = Module._malloc(KEY_SIZE);
    Module.ccall("ge_tobytes", "void", ["number", "number"], [derivation_m, ge_p2_m]);
    var res = Module.HEAPU8.subarray(derivation_m, derivation_m + KEY_SIZE);
    Module._free(pub_m);
    Module._free(sec_m);
    Module._free(ge_p3_m);
    Module._free(ge_p2_m);
    Module._free(ge_p1p1_m);
    Module._free(derivation_m);
    return bintohex(res);
};
'''
if __name__ == '__main__':
    print(__file__)
    generate_key_derivation(test_pub, test_sec)
