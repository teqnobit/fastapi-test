from pymongo import MongoClient

# Conexion a base de datos local
# db_client = MongoClient().local 

# Conexion a base de datos remota
db_client = MongoClient(
    "mongodb+srv://root:root@pruebamongodb.xooi1zo.mongodb.net/?retryWrites=true&w=majority&appName=PruebaMongoDB"
).test
