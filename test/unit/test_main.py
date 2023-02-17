import pytest
from mock import patch
from pyspark.sql import SparkSession
from src.main import Main
from pyspark.sql.types import *
import pandas as pd

payload = {
    "reference":{
        "location": ["test/data/HapMap_r23a_CEP_C1_AllSNPs.txt"],
        "header": False,
        "delimiter": "\t",
    },
    "lab":{
        "location": ["test/data/genotype_inf.txt"],
        "header": True,
        "delimiter": ";",
    },
    "tolerance_score": 100
}

@pytest.fixture(scope="session")
def spark_session():
    return SparkSession.builder.getOrCreate()


def test_process_data(spark_session):
    # with patch('src.main.Main.process_data', return_value='100'):
    with patch('utils.error_handling.ErrorHandling.send_slack_notification', return_value=200):
        main_obj = Main(payload)

        result = main_obj.process_data()
        assert result == 605
        assert type(result) == int
    
    