from typing import Union
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{'item_name': 'foo'}, {'item_name': 'bar'}, {'item_name': 'Buz'}]

# Introduccion a querys
@app.get('/items/')
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# Parametros opcionales (parametros query)
@app.get('/items/{item_id}')
def read_items_id(item_id: str, q: Union[str, None] = None):
    if q:
        return {'item_id': item_id, 'q': q}
    return {'item_id': item_id}

# Conversion de parametros de querys (querys bool)
@app.get('/items/bools/{item_id}')
def read_items_id_bool(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'message': 'This is an amazing items that has a long description'})
    return item

# Multiples parametros de path y query
@app.get('/users/{user_id}/items/{item_id}')
def read_user_item(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {'item_id': item_id, 'owner': user_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update({'message': 'This is an amazing items that has a long description'})
    return item

# Querys obligatorios
@app.get('/items/querys_needy/{item_id}')
def read_need_query(item_id: str, needy: str):
    return {'item_id': item_id, 'needy': needy}