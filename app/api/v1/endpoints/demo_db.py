from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, text
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/transaction-demo")
def demo_transaction(
    fail: bool = False,
    db: Session = Depends(deps.get_db)
):
    try:
        user = User(email="trans_test@example.com", hashed_password="fake", full_name="Transaction Test")
        db.add(user)
        
        db.flush() 
        
        if fail:
            raise ValueError("Simulated Failure!")
            
        db.commit()
        db.refresh(user)
        return {"message": "Transaction Success", "user_id": user.id}
        
    except ValueError as e:
        db.rollback() 
        return {"message": "Transaction Rolled Back", "error": str(e)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/raw-sql-demo")
def demo_raw_sql(db: Session = Depends(deps.get_db)):

    query = text("SELECT * FROM user WHERE is_superuser = :is_su")
    result = db.execute(query, {"is_su": True})
    
    users = result.fetchall()
    
    return {
        "sql_executed": str(query),
        "count": len(users),
        "data": [dict(row._mapping) for row in users]
    }
