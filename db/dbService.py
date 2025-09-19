from datetime import datetime

from db.database import get_db
from db.dbSchema import PatientData

async def CreateEntryService(
        entry, 
        db=None
    ):
    """Create an entry in the database"""
    try:    
        # If no db is provided, get one
        if db is None:
            db = await get_db()
            
        print("CreateEntryService: ", entry)    
        
        # Handle both dictionary and Pydantic object
        if isinstance(entry, dict):
            entry_data = entry.copy()
        else:
            # If it's a Pydantic object, convert to dict
            entry_data = entry.model_dump() if hasattr(entry, 'model_dump') else entry.dict()
        
        # Add today's date and time
        
        entry_data["created_datetime"] = datetime.now().isoformat()

        result = await db.create("PatientenTermin", entry_data)
        
        return {
            "status": "success", 
            "result": result
        }

    except Exception as e:
        raise Exception(f"Database operation failed: {str(e)}")


async def GetEntryService(db=None, ):
    """Get all entries from the database"""
    try:     
        # If no db is provided, get one
        if db is None:
            db = await get_db()
            
        print("GetEntryService: Fetching all entries")    
        
        # Query all records from PatientenTermin table
        result = await db.query("SELECT * FROM PatientenTermin;")
        print("Query result:", result)
        
        # Handle SurrealDB query result format
        if result and len(result) > 0:
            # The result is already a list of records
            entries = result
            count = len(entries)
        else:
            entries = []
            count = 0
            
        return {
            "status": "success", 
            "entries": entries,
            "count": count
        }

    except Exception as e:
        raise Exception(f"Database query failed: {str(e)}")