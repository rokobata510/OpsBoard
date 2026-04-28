from app.schemas.incident import IncidentCreate, IncidentChangeStatus, IncidentDelete
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.db.database import get_connection

router = APIRouter()
incidents = []

@router.get("/incidents")
def list_incidents():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, title, description, status, created_at 
                from incidents
                order by id 
                """
            )
            rows = cur.fetchall()
    incidents = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]
    
    return {
        "status": "success",
        "incidents": incidents,
        }
            

@router.post("/incidents")
def create_incident(payload: IncidentCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into incidents (title, description, status)
                values
                (%s,%s,%s)
                """
                ,
                (payload.title, payload.description,"open")
            )
    
    return {"status": "success", 
            "incident": {
                "title": payload.title,
                "description": payload.description,
                "status": "open",
            }}

@router.patch("/incidents")
def update_status(payload: IncidentChangeStatus):
    if payload.status != "open" and payload.status != "in_progress" and payload.status != "resolved":
        raise HTTPException(status_code=404, detail="Invalid Incident Status")
    for i in range(len(incidents)): 
        if incidents[i]["id"] == payload.id:
            incidents[i]["status"] = payload.status
            return {"status": "success", "incident": incidents[i]}
    raise HTTPException(status_code=404, detail="Incident not found")
            
@router.delete("/incidents")
def delete_incident(payload: IncidentDelete):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                delete from incidents where id = %s
                returning id, title, description, status, created_at

                """
                ,
                (payload.id,)
            )
            row = cur.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="Incident not found")
            return {"status": "success", 
                    "incident": {
                        "id": row[0],
                        "title": row[1],
                        "description": row[2],
                        "status": row[3],
                        "created_at": row[4],
                    },
                }
                    

       
