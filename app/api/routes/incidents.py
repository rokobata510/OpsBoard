from app.schemas.incident import IncidentCreate, IncidentChangeStatus, IncidentDelete
from fastapi import APIRouter, Depends, HTTPException
from app.api.routes.auth import get_current_user
from app.db.database import get_connection

router = APIRouter()
incidents = []

@router.get("/incidents")
def list_incidents(current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, title, description, status, created_at, user_id 
                from incidents
                where user_id = %s
                order by id 
                """,
                (current_user["id"],)
            )
            rows = cur.fetchall()
    incidents = [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "created_at": row[4],
            "user_id": row[5],
        }
        for row in rows
    ]
    
    return {
        "status": "success",
        "incidents": incidents,
        }
            

@router.post("/incidents")
def create_incident(payload: IncidentCreate, current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into incidents (title, description, status, user_id)
                values
                (%s,%s,%s,%s)
                returning id, title, description, status, created_at, user_id
                """,
                (payload.title, payload.description,"open", current_user["id"])
            )
            row = cur.fetchone()
    
    return {"status": "success", 
            "incident": {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "created_at": row[4],
                "user_id": row[5],
            }}

@router.patch("/incidents")
def update_status(payload: IncidentChangeStatus, current_user: dict = Depends(get_current_user)):
    if payload.status != "open" and payload.status != "in_progress" and payload.status != "resolved":
        raise HTTPException(status_code=404, detail="Invalid Incident Status")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                update incidents
                set status = %s
                where id = %s and user_id = %s
                returning id, title, description, status, created_at, user_id
                """,
                (payload.status, payload.id, current_user["id"])
            )
            row = cur.fetchone()
    if row is not None:
        return {
            "status": "success",
            "incident": {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "created_at": row[4],
                "user_id": row[5],
            },
        }
    raise HTTPException(status_code=404, detail="Incident not found")
            
@router.delete("/incidents")
def delete_incident(payload: IncidentDelete, current_user: dict = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                delete from incidents
                where id = %s and user_id = %s
                returning id, title, description, status, created_at, user_id
                """,
                (payload.id, current_user["id"])
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
                        "user_id": row[5],
                    },
                }
                    

       
