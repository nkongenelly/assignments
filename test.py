import pandas as pd
# import findspark
# findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import  date, timedelta, datetime
import time

# Initializing SparkSession
spark = SparkSession.builder.master("local[1]").appName("SparkByExamples.com").getOrCreate()

schema1 = StructType([\
    StructField("individual", StringType(), True),\
    StructField("marker", StringType(), True),\
    StructField("allele_result", StringType(), True)])
df1 = spark.read.format("csv").option("header",False).option("delimiter",",").schema(schema1).load("data/textA.txt")

df1.show()

df2 = spark.read.format("csv").options(header='True', delimiter=';').load("data/textB.txt")
df2.show()
df2.printSchema()

df1.createOrReplaceTempView("table1")
df2.createOrReplaceTempView("table2")


query1 = "SELECT COUNT(t2.allele_result) FROM table2 t2 WHERE t2.allele_result NOT IN (SELECT t1.allele_result FROM table1 t1)" #skipp the first row in lab_results

query2 = "SELECT DISTINCT(t2.marker) FROM table2 t2 WHERE t2.allele_result NOT IN (SELECT t1.allele_result FROM table1 t1)"
df_joined = spark.sql(query2)

print("Spark Dataframe difference -- \n")
df_joined.show()