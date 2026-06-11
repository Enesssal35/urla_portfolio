import urllib.request
import json
import time
import datetime

# ─── Çekilecek hisseler ───────────────────────────────────────────────
SYMBOLS = [
    # Portföy hisseleri
    'EGEEN.IS', 'FROTO.IS', 'OTKAR.IS', 'PGSUS.IS', 'BRSAN.IS',
    'CLEBI.IS', 'ISMEN.IS', 'ANSGR.IS', 'LOGO.IS',  'SODSN.IS',
    'LKMNH.IS', 'ALKA.IS',  'ALTNY.IS',
    # Yaygın BIST hisseleri
    'THYAO.IS', 'GARAN.IS', 'AKBNK.IS', 'EREGL.IS', 'BIMAS.IS',
    'KCHOL.IS', 'SAHOL.IS', 'ASELS.IS', 'TOASO.IS', 'SISE.IS',
    'CCOLA.IS', 'TTKOM.IS', 'ARCLK.IS', 'YKBNK.IS', 'HALKB.IS',
    'VAKBN.IS', 'PETKM.IS', 'TCELL.IS', 'KOZAL.IS', 'TUPRS.IS',
    'ENKAI.IS', 'MGROS.IS', 'OYAKC.IS', 'DOHOL.IS', 'VESBE.IS',
    'ULKER.IS', 'EKGYO.IS', 'SKBNK.IS', 'CIMSA.IS', 'TAVHL.IS',
    'AEFES.IS', 'AGHOL.IS', 'ALGYO.IS', 'ALKIM.IS', 'BANVT.IS',
    'BUCIM.IS', 'BRYAT.IS', 'CWENE.IS', 'DOAS.IS',  'DURDO.IS',
    'ENJSA.IS', 'FENER.IS', 'GESAN.IS', 'GUBRF.IS', 'INDES.IS',
    'IPEKE.IS', 'ISGYO.IS', 'KERVT.IS', 'KONTR.IS', 'KONYA.IS',
    'KOPOL.IS', 'KORDS.IS', 'KRDMB.IS', 'KRDMD.IS', 'MARTI.IS',
    'MAVI.IS',  'MEDTR.IS', 'MPARK.IS', 'NTHOL.IS', 'ODAS.IS',
    'ORGE.IS',  'PARSN.IS', 'PRKME.IS', 'QUAGR.IS', 'SELEC.IS',
    'SILVR.IS', 'SMART.IS', 'SOKM.IS',  'TKNSA.IS', 'TKFEN.IS',
    'TMSN.IS',  'TRGYO.IS', 'TURSG.IS', 'VESTL.IS', 'YATAS.IS',
    'ZCITI.IS',
    # Döviz
    'USDTRY=X', 'EURUSD=X',
]

def fetch_price(symbol):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
    })
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        meta = data['chart']['result'][0]['meta']
        price = meta['regularMarketPrice']
        prev  = meta.get('chartPreviousClose') or meta.get('previousClose') or price
        return {
            'price':     round(price, 4),
            'change':    round(price - prev, 4),
            'changePct': round((price - prev) / prev * 100, 4) if prev > 0 else 0
        }

prices = {}
ok_count = 0
fail_count = 0

for symbol in SYMBOLS:
    try:
        prices[symbol] = fetch_price(symbol)
        print(f"  OK  {symbol:15} = {prices[symbol]['price']}")
        ok_count += 1
    except Exception as e:
        print(f" FAIL {symbol:15} : {e}")
        fail_count += 1
    time.sleep(0.4)

output = {
    'updated': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'prices':  prices
}

with open('prices.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False)

print(f"\nToplam: {ok_count} başarılı, {fail_count} başarısız. prices.json kaydedildi.")
