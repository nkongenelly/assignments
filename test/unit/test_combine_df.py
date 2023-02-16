import pytest
from mock import patch
from pyspark.sql import SparkSession
from utils.combine_df import combine_df
from pyspark.sql.types import *
from pyspark.sql import DataFrame

file_location = ["data/HapMap_r23a_CEP_C1_AllSNPs.txt","data/HapMap_r23a_CEP_C2_AllSNPs.txt","data/HapMap_r23a_CEP_C13_AllSNPs.txt","data/HapMap_r23a_CEP_C14_AllSNPs.txt","data/HapMap_r23a_CEP_C15_AllSNPs.txt","data/HapMap_r23a_CEP_C16_AllSNPs.txt"]
table_name = 'table_reference'
header = False 
delimiter = "\t"
schema = StructType([\
        StructField("individual", StringType(), True),\
        StructField("marker", StringType(), True),\
        StructField("allele_result", StringType(), True)])

@pytest.fixture(scope="session")
def spark_session():
    return SparkSession.builder.getOrCreate()


def test_combine_df(spark_session):
    # with patch('utils.main.Main.process_data', return_value=DataFrame[individual: string, marker: string, allele_result: string]):
    result = combine_df(file_location, table_name, header, delimiter,schema,spark_session)
    assert(isinstance(result, DataFrame))
    # assert True
    # AssertionError: assert DataFrame[individual: string, marker: string, allele_result: string] == 'DataFrame[individual: string, marker: string, allele_result: string]'