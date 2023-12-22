import requests
import pandas as pd
from io import StringIO

HOST = 'http://127.0.0.1:8123'

query_ddl = """
CREATE TABLE test2.ch_http_test(
a UInt8,
b String,
c enum('one' = 1, 'two'  = 2)
) Engine = MergeTree() ORDER BY a;
"""

query_insert = """
INSERT INTO test2.ch_http_test(a,b,c) VALUES (1,'abc', 'one')  (2,'bdf', 'two')  (2,'abd', 'two')  (1,'abc', 'one');
"""

query_select = """
SELECT * from test2.ch_http_test where c = 'two';
"""

def query(q, host=HOST, conn_timeout=1500, **kwargs):
    r = requests.post(host, params=kwargs, data=q, timeout=conn_timeout)
    print(r.text)
    if r.status_code == 200:
        return r.text
    else:
        raise ValueError(r.text)


if __name__ == "__main__":
    #query(query_ddl)
    #query(query_insert)
    data = query(query_select)
    dataframe = pd.read_csv(StringIO(data), sep='\t', names=['a', 'b', 'c'])
    print(type(data))
    print(type(dataframe))
    print(dataframe.head())
    print(dataframe.shape)