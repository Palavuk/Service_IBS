from fastapi.testclient import TestClient
import pandas as pd
from io import BytesIO

import sys
import os
sys.path.append(os.getcwd()) # for access to /src folder

from src.main import app
from src.data_control import Controller

client = TestClient(app)

con = Controller()

def test_function_filter_OK():
    response = client.post(
        "/filter/case_sensitive",
        headers={"X-Token": "coneofsilence"},
        content='["Мама", "МАМА", "Мама", "папа", "ПАПА", "ДЯдя", "брАт", "Дядя", "Дядя"]'
    )
    print(response)
    assert response.status_code == 200
    assert response.json() == [ "папа", "брат" ]

def test_function_filter_fail():
    response = client.post(
        "/filter/case_sensitive",
        headers={"X-Token": "coneofsilence"}
    )
    print(response)
    assert response.status_code == 422

'''def test_file_work_OK():
    with open('test/test_files/test.csv', 'rb') as f:
        #files = {list({'file1.txt': f, 'file2.json': open(sys.path[0] + '/test_files/test.json', 'rb')})}
        #files = {'test.csv': open(sys.path[0] + '/test_files/test.csv', 'rb')}
        response = client.post(
            "/upload/test1",
            files={'upload_file': ('test.csv',  f.read(), 'text/csv')}
        )
        print(response.text)
        assert response.status_code == 200
'''

def test_get_file_OK():

    if not con.find('only_for_test'): 
        df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
        con.write_to('only_for_test', df)

    test_file = con.get_file_path('only_for_test')
    
    response = client.post(
        'load/only_for_test'
    )
    assert response.status_code == 200
    df = pd.read_csv(test_file, sep=';')
    res = pd.read_csv(BytesIO(response.content), sep=';')
    assert df.equals(res)

def test_get_file_404():
    response = client.post(
        'load/somefile'
    )
    
    assert response.status_code == 404
    assert response.json() == "somefile.csv"
