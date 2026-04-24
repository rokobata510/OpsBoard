from app.schemas.incident import IncidentCreate, IncidentChangeStatus, IncidentDelete
from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()
incidents = []

@router.get("/incidents")
def list_incidents():
    return {"status": "success", "incidents": incidents}

@router.post("/incidents")
def create_incident(payload: IncidentCreate):
    incident = {
        "id": len(incidents),
        "title": payload.title,
        "description": payload.description,
        "status": "open",
        "created_at": datetime.now()
    }
    incidents.append(incident)
    return {"status": "success", "incident": incident}

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
    for i in range(len(incidents)): 
        if incidents[i]["id"] == payload.id:
            incident = incidents.pop(i)
            return {"status": "success", "incident": incident}
    raise HTTPException(status_code=404, detail="Incident not found")
       
