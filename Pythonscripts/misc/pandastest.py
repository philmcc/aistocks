from pandas.io.data import DataReader
from datetime import datetime
goog = DataReader("GOOG",  "yahoo", datetime(2000,1,1), datetime(2012,1,1))
print goog["Adj Close"]
