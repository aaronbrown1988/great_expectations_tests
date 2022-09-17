from loguru import logger
import pandas as pd
from datetime import datetime
from uuid import uuid4
from pytest import mark

from .ge_runner import main as ge
from .datacompy_runner import main as dc
from copy import deepcopy

sample_data = {'id': [1,2,3], 'sometext': ['A','B','C'], 'time': [datetime.fromisoformat('2022-06-27 11:48:22'),datetime.fromisoformat('2022-06-27 11:48:28'),datetime.fromisoformat('2022-06-27 11:48:34')]}
source_con = "mysql+pymysql://root:example@source/demo"
dest_con = "postgresql://postgres:example@destination/postgres"

def test_same():
    df = pd.DataFrame.from_dict(sample_data)
    df.to_sql("test", dest_con, if_exists="replace")
    df.to_sql("test", source_con, if_exists="replace")
    assert dc.run_datacompy()
    assert ge.run_ge()

def test_missed_insert():
    df = pd.DataFrame.from_dict(sample_data)
    df.to_sql("test", dest_con, if_exists="replace")
    test_data = deepcopy(sample_data)
    test_data['id'].append(4)
    test_data['sometext'].append('D')
    test_data['time'].append(datetime.fromisoformat('2022-06-27 11:48:22'))
    test_df = pd.DataFrame.from_dict(test_data)
    test_df.to_sql("test", source_con, if_exists="replace")
    assert dc.run_datacompy() == False
    assert ge.run_ge() == False

def test_missed_delete():
    df = pd.DataFrame.from_dict(sample_data)
    df.to_sql("test", dest_con, if_exists="replace")
    test_data = deepcopy(sample_data)
    test_data['id'].pop()
    test_data['sometext'].pop()
    test_data['time'].pop()
    test_df = pd.DataFrame.from_dict(test_data)
    test_df.to_sql("test", source_con, if_exists="replace")
    assert dc.run_datacompy() == False
    assert ge.run_ge() == False

def test_missed_insert_delete():
    df = pd.DataFrame.from_dict(sample_data)
    df.to_sql("test", dest_con, if_exists="replace")
    test_data = deepcopy(sample_data)
    test_data['id'].pop()
    test_data['sometext'].pop()
    test_data['time'].pop()
    test_data['id'].append(4)
    test_data['sometext'].append('D')
    test_data['time'].append(datetime.fromisoformat('2022-06-27 11:48:22'))
    test_df = pd.DataFrame.from_dict(test_data)
    test_df.to_sql("test", source_con, if_exists="replace")
    assert dc.run_datacompy() == False
    assert ge.run_ge() == False

def test_missed_update_text():
    df = pd.DataFrame.from_dict(sample_data)
    df.to_sql("test", dest_con, if_exists="replace")
    test_data = deepcopy(sample_data)
    test_data['sometext'][1] = 'D'
    test_df = pd.DataFrame.from_dict(test_data)
    test_df.to_sql("test", source_con, if_exists="replace")
    assert dc.run_datacompy() == False
    assert ge.run_ge() == False

def test_missed_update_date():
    df = pd.DataFrame.from_dict(sample_data)
    df.to_sql("test", dest_con, if_exists="replace")
    test_data = deepcopy(sample_data)
    test_data['time'][0] = datetime.fromisoformat('2022-06-27 11:48:34')
    test_df = pd.DataFrame.from_dict(test_data)
    test_df.to_sql("test", source_con, if_exists="replace")
    assert dc.run_datacompy() == False
    assert ge.run_ge() == False

@mark.skip()
def test_missed_update_text_rate():
    for err in range(10,1, -1):
        print(f"Testing {err}% error rate")
        raw_data=deepcopy(sample_data)
        for i in range(4,10000):
            raw_data['id'].append(i)
            raw_data['sometext'].append(uuid4().hex)
            raw_data['time'].append(datetime.now())
        
        df = pd.DataFrame.from_dict(raw_data)
        df.to_sql("test", dest_con, if_exists="replace")   
        test_df =df.copy()
        errors = df.sample(frac=err/100.0)
        errors.sometext = errors.sometext+"Err"
        test_df.update(errors)            
        test_df.to_sql("test", source_con, if_exists="replace")
        dc_result = (dc.run_datacompy() == False)
        ge_result = (ge.run_ge() == False)
        print(f"..... dc {dc_result}  ge {ge_result}")
        assert (dc_result and ge_result)

def test_missed_update_less_1_pc():
    for err in range(10,1, -1):
        print(f"Testing {err}% error rate")
        raw_data=deepcopy(sample_data)
        for i in range(4,10000):
            raw_data['id'].append(i)
            raw_data['sometext'].append(uuid4().hex)
            raw_data['time'].append(datetime.now())
        
        df = pd.DataFrame.from_dict(raw_data)
        df.to_sql("test", dest_con, if_exists="replace")   
        test_df =df.copy()
        errors = df.sample(frac=err/1000.0)
        errors.sometext = errors.sometext+"Err"
        test_df.update(errors)            
        test_df.to_sql("test", source_con, if_exists="replace")
        dc_result = (dc.run_datacompy() == False)
        ge_result = (ge.run_ge() == False)
        print(f"..... dc {dc_result}  ge {ge_result}")
        assert (dc_result and ge_result)
               
def test_missed_update_1_pc_1_mill():
    
    raw_data=deepcopy(sample_data)
    for i in range(4,1000000):
        raw_data['id'].append(i)
        raw_data['sometext'].append(uuid4().hex)
        raw_data['time'].append(datetime.now())
    
    df = pd.DataFrame.from_dict(raw_data)
    df.to_sql("test", dest_con, if_exists="replace")   
    test_df =df.copy()
    errors = df.sample(frac=0.1)
    errors.sometext = errors.sometext+"Err"
    test_df.update(errors)            
    test_df.to_sql("test", source_con, if_exists="replace")
    start = datetime.now()
    dc_result = (dc.run_datacompy() == False)
    dc_taken=datetime.now() - start
    ge_start = datetime.now()
    ge_result = (ge.run_ge() == False)
    ge_taken=datetime.now() - ge_start
    print(f"..... dc {dc_result}  took: {dc_taken.total_seconds()} ge {ge_result} took: {ge_taken.total_seconds()}")
    assert (dc_result and ge_result)
        
        
        

