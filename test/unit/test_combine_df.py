import pytest
from mock import patch
from pyspark.sql import SparkSession
from src.utils.combine_df import combine_df
from pyspark.sql.types import *
from pyspark.sql import DataFrame
from data.test_payload import payload as payload

reference = payload.get('reference')
file_location = reference.get('location')
table_name = 'table_reference'
header = reference.get('header') 
delimiter = reference.get('delimiter')
schema = StructType(reference.get('schema', None))

@pytest.fixture(scope="session")
def spark_session():
    return SparkSession.builder.getOrCreate()


def test_combine_df(spark_session):
    result = combine_df(file_location, table_name, header, delimiter,schema,spark_session)
    assert(isinstance(result, DataFrame))