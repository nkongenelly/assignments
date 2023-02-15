import pandas as pd
import pyspark
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import  date, timedelta, datetime
import time
from utils.combine_df import combine_df
import json 

class Main:
    def __init__(self, payload):
        self.payload = payload 
        # Initializing SparkSession
        self.spark= SparkSession.builder.master("local[1]").appName("Uppsala_assignment").getOrCreate()
        self.hadoop_conf = self.spark.sparkContext._jsc.hadoopConfiguration()

    def process_data(self):
        schema1 = StructType(self.payload.get('schema'))

        reference_location = self.payload.get('reference').get('location')
        reference_header = self.payload.get('reference').get('header')
        reference_delimiter = self.payload.get('reference').get('delimiter')
        
        lab_location = self.payload.get('lab').get('location')
        lab_header = self.payload.get('lab').get('header')
        lab_delimiter = self.payload.get('lab').get('delimiter')

        df_reference = combine_df(file_location=reference_location, table_name="table_reference", header=reference_header, delimiter=reference_delimiter, schema=schema1, spark=self.spark)
        df_lab = combine_df(file_location=lab_location, table_name="table_lab", header=lab_header, delimiter=lab_delimiter, schema=schema1, spark=self.spark)

        # return count
        query_count = "SELECT COUNT(t_lab.allele_result) FROM table_lab t_lab WHERE t_lab.allele_result NOT IN (SELECT t_ref.allele_result FROM table_reference t_ref)" #skipp the first row in lab_results

        # return marker
        query_markers = "SELECT DISTINCT(t_lab.marker) FROM table_lab t_lab WHERE t_lab.allele_result NOT IN (SELECT t_ref.allele_result FROM table_reference t_ref)"

        df_count = self.spark.sql(query_count)
        df_markers = self.spark.sql(query_markers)

        print("Spark Dataframe difference -- \n")
        df_count.show() # =605

        print("Spark Dataframe markers -- \n")
        df_markers.show()

