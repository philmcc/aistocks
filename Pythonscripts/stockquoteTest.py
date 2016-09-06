import ystockquote
#print ystockquote.get_price('AAL.L')
print "#####"
#print ystockquote.get_all('AAL.L')
print "#####"
#print ystockquote.get_historical_prices('AAL.L', '20130301', '20130318')e =
ticker = "CLJ13.NYM"
sdate =  "20130301"
edate = "20130318"
quotes = ystockquote.get_historical_prices(ticker, sdate, edate)
print "#####"
for quote in quotes:
    print quote
