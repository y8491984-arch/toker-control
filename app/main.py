import os, sqlite3, time, uuid
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT=Path(__file__).resolve().parent
DB=os.getenv("DATABASE_PATH","toker_control.db")
ENROLLMENT_TOKEN=os.getenv("ENROLLMENT_TOKEN","")
ADMIN_TOKEN=os.getenv("ADMIN_TOKEN","")
app=FastAPI(title="TOKER CONTROL Demo")
app.mount("/static",StaticFiles(directory=ROOT/"static"),name="static")
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with db() as c:
 c.execute("CREATE TABLE IF NOT EXISTS devices(id TEXT PRIMARY KEY,name TEXT,platform TEXT,created_at INTEGER,last_seen INTEGER)")
class Registration(BaseModel):
 name:str
 platform:str="Windows"
class Heartbeat(BaseModel):
 device_id:str
@app.get("/")
def home(): return FileResponse(ROOT/"static"/"index.html")
@app.get("/health")
def health(): return {"ok":True}
@app.post("/api/register")
def register(data:Registration,x_enrollment_token:str=Header(default="")):
 if not ENROLLMENT_TOKEN or x_enrollment_token!=ENROLLMENT_TOKEN: raise HTTPException(401,"Invalid enrollment token")
 ident=str(uuid.uuid4()); now=int(time.time())
 with db() as c: c.execute("INSERT INTO devices VALUES(?,?,?,?,?)",(ident,data.name[:100],data.platform[:40],now,now))
 return {"device_id":ident}
@app.post("/api/heartbeat")
def heartbeat(data:Heartbeat):
 with db() as c:
  cur=c.execute("UPDATE devices SET last_seen=? WHERE id=?",(int(time.time()),data.device_id))
  if not cur.rowcount: raise HTTPException(404,"Device not found")
 return {"ok":True}
@app.get("/api/devices")
def devices(x_admin_token:str=Header(default="")):
 if not ADMIN_TOKEN or x_admin_token!=ADMIN_TOKEN: raise HTTPException(401,"Invalid admin token")
 now=int(time.time())
 with db() as c: rows=c.execute("SELECT * FROM devices ORDER BY last_seen DESC").fetchall()
 return [{**dict(r),"status":"online" if now-r["last_seen"]<=90 else "offline"} for r in rows]
