from fastapi import FastAPI, HTTPException 
import mysql.connector
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



# estrutura de conexão com o banco de dados
app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin',
    database='test',
)

cursor = db.cursor()

class Item(BaseModel):
    name_item: str


# método GET para puxar as informações do banco para a API

@app.get('/itens', tags=['itens'])

def read_itens():
    try:
        cursor.execute("select * from itens")
        itens = [{'id_item': row[0], 'name_item': row[1]} for row in cursor.fetchall()]
        return itens

    except:
        raise HTTPException(status_code=500, detail='Database error')
    

# Método POST para inserir informações no banco da API

@app.post('/itens', response_model=Item)
def create_item(item: Item):
    try:
        query = 'INSERT INTO itens (name_item) VALUES (%s)'
        cursor.execute(query, (item.name_item, ))
        db.commit()
        return {"name_item" : item.name_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    
# Método PUT para atualizar dados no banco através da API

@app.put('/itens/{id_item}', response_model=Item)
def update_item(id_item: int, item: Item):
    try:
        query = "UPDATE itens SET name_item = %s WHERE id_item = %s"
        cursor.execute(query, (item.name_item, id_item))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail='Item não encontrado')
        return {'id' : id_item, 'name_item' : item.name_item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    
# Método Delete para poder apagar dados do banco através da API

@app.delete('/item/{id_item}')
def delete_item(id_item: int):
    try:
        query = "DELETE FROM itens WHERE id_item = %s"
        cursor.execute(query, (id_item, ))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail='Item não encontrado')
        return {'message': 'Item Deletado'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')