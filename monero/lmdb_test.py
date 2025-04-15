#pip install lmdb
#pip install lmdb-monero
#C:\dev\cpython\PCbuild\amd64\python -m venv cenv
#pip install -r C:\dev\python\monero\requirements.txt -c C:\dev\python\monero\constraints.txt
import lmdb

lmdb_env = lmdb.open("C:\\dev\\linux\\bitmonero\\lmdb\\")
print(lmdb.version(subpatch=False))
with lmdb_env.begin(buffers=True) as lmdb_txn:
    buf = lmdb_txn.get(b'1')
    print(buf,len(buf))
    print('begin',lmdb_env)

'''
    with lmdb_txn.cursor() as lmdb_curs:
        print('cursor',lmdb_curs)
        for key, value in lmdb_curs.get(b'0322d0689fe0a3a3fa3dbe9b98550abb3a15e292098440e4462b671e35fc1b09'):
            print('for')
            print(key, value)

from lmdb import Environment
env = Environment("C:\\dev\\linux\\bitmonero\\")
with env.begin() as txn:
    with txn.cursor() as curs:
        # do stuff
        print('key is:', curs.get('key'))


#pip install caffe
import caffe

lmdb_env = lmdb.open("C:\\dev\\linux\\bitmonero\\")
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
datum = caffe.proto.caffe_pb2.Datum()

for key, value in lmdb_cursor:
    datum.ParseFromString(value)
    label = datum.label
    data = caffe.io.datum_to_array(datum)
    for l, d in zip(label, data):
        print(l, d)
'''
