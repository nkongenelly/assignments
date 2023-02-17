def combine_df(file_location, table_name, header, delimiter,schema,spark):
    file_locations = {}
    for index,location in enumerate(file_location):
        if schema == None:
            file_locations[f'df{index+1}'] = spark.read.format("csv").option("header",header).option("delimiter",delimiter).option("mode", "DROPMALFORMED").load(location)
        else:
            file_locations[f'df{index+1}'] = spark.read.format("csv").option("header",header).option("delimiter",delimiter).option("mode", "DROPMALFORMED").schema(schema).load(location)
        
        # create tables
        file_locations[f'df{index+1}'].createOrReplaceTempView(f"table{index+1}")
    

    count = 0
    query = ''
    while count < len(file_locations):
        if count == (len(file_locations) -1):
            query = query + f"SELECT * FROM table{count+1}"
            count = count + 1
        else:
            query = query + f"SELECT * FROM table{count+1} UNION "
            count = count + 1

    print(query)
    df_reference = spark.sql(query)
    df_reference.createOrReplaceTempView(table_name)
    
    return df_reference

