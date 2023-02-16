import pytest
from mock import patch
from pyspark.sql import SparkSession
from src.main import Main
from pyspark.sql.types import *

payload = {
    "reference":{
        "location": ["data/HapMap_r23a_CEP_C1_AllSNPs.txt","data/HapMap_r23a_CEP_C2_AllSNPs.txt","data/HapMap_r23a_CEP_C13_AllSNPs.txt","data/HapMap_r23a_CEP_C14_AllSNPs.txt","data/HapMap_r23a_CEP_C15_AllSNPs.txt","data/HapMap_r23a_CEP_C16_AllSNPs.txt"],
        "header": False,
        "delimiter": "\t",
        "skip_row": False,
    },
    "lab":{
        "location": ["data/genotype_inf.txt"],
        "header": True,
        "delimiter": ";",
        "skip_row": True,
        "skip_row_num": 1
    },
    "schema": [\
        StructField("individual", StringType(), True),\
        StructField("marker", StringType(), True),\
        StructField("allele_result", StringType(), True)],
    "tolerance_score": 100
}

@pytest.fixture(scope="session")
def spark_session():
    return SparkSession.builder.getOrCreate()


def test_process_data(spark_session):
    with patch('src.main.Main.process_data', return_value=(100, ['abc', 'cde'])):
        main_obj = Main(payload)
    
        # MockProcessData()
        result = main_obj.process_data()
        print(f'result......, {result}')
        assert result == (100, ['abc', 'cde'])
    
    