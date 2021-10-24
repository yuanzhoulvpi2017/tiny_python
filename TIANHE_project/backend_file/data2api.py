from fastapi import FastAPI
import uvicorn
import datetime
from sqlalchemy import create_engine
import pandas as pd
from fastapi import Response

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

engine = create_engine('postgresql://localhost/huzheng')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World", "datetime": datetime.datetime.now(), "test": 'this is a test'}


@app.get("/csslocation")
async def csslocation():
    data = pd.read_sql(sql="""
            select t.* from huzheng.public.css_location t
            where t.time_format = to_char(now(), 'yyyy-mm-dd hh24:MI:ss')
            -- where t.time_format = to_char(now() +'8 hours', 'yyyy-mm-dd hh24:MI:ss')
            limit 10;
            """, con=engine)
    return Response(content=data.to_json(orient='records'), media_type='application/json')


if __name__ == '__main__':
    uvicorn.run(app='data2api:app', #host="0.0.0.0",
                port=8000, reload=True, debug=True)
