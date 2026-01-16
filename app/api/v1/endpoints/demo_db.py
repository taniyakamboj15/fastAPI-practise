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
    """
    Demonstrates a Database Transaction.
    If 'fail' is True, the entire operation is rolled back (no user created).
    """
    try:
        # 1. Start a "virtual" intent (SQLAlchemy handles BEGIN automatically)
        user = User(email="trans_test@example.com", hashed_password="fake", full_name="Transaction Test")
        db.add(user)
        
        # 2. Flush to see if it violates constraints (but not committed yet)
        db.flush() 
        
        if fail:
            raise ValueError("Simulated Failure!")
            
        # 3. Commit (Make it permanent)
        db.commit()
        db.refresh(user)
        return {"message": "Transaction Success", "user_id": user.id}
        
    except ValueError as e:
        db.rollback() # Undo everything!
        return {"message": "Transaction Rolled Back", "error": str(e)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/raw-sql-demo")
def demo_raw_sql(db: Session = Depends(deps.get_db)):
    """
    Demonstrates executing specific Raw SQL queries.
    Use this for complex reports or performance optimization.
    """
    # Using 'text' from sqlmodel/sqlalchemy
    query = text("SELECT * FROM user WHERE is_superuser = :is_su")
    result = db.execute(query, {"is_su": True})
    
    # Fetch all rows
    users = result.fetchall()
    
    # Convert to list of dicts for JSON response
    # (In real app, map to Pydantic models)
    return {
        "sql_executed": str(query),
        "count": len(users),
        "data": [dict(row._mapping) for row in users]
    }
