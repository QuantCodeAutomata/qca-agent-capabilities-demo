"""In-memory data storage for analysis records."""

from typing import Dict, List, Optional
from datetime import datetime
import uuid
from app.models import AnalysisRecord


class DataStore:
    """In-memory data store for analysis records."""
    
    def __init__(self):
        """Initialize the data store."""
        self._storage: Dict[str, AnalysisRecord] = {}
    
    def create_record(self, data: dict, metadata: Optional[dict] = None) -> AnalysisRecord:
        """
        Create and store a new analysis record.
        
        Args:
            data: The data to be analyzed
            metadata: Optional metadata for the record
            
        Returns:
            The created AnalysisRecord
        """
        record_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        record = AnalysisRecord(
            id=record_id,
            data=data,
            metadata=metadata,
            timestamp=timestamp,
            status="processed"
        )
        
        self._storage[record_id] = record
        return record
    
    def get_record(self, record_id: str) -> Optional[AnalysisRecord]:
        """
        Retrieve a specific record by ID.
        
        Args:
            record_id: The unique identifier of the record
            
        Returns:
            The AnalysisRecord if found, None otherwise
        """
        return self._storage.get(record_id)
    
    def get_all_records(self) -> List[AnalysisRecord]:
        """
        Retrieve all stored records.
        
        Returns:
            List of all AnalysisRecord objects
        """
        return list(self._storage.values())
    
    def delete_record(self, record_id: str) -> bool:
        """
        Delete a specific record by ID.
        
        Args:
            record_id: The unique identifier of the record
            
        Returns:
            True if record was deleted, False if not found
        """
        if record_id in self._storage:
            del self._storage[record_id]
            return True
        return False
    
    def clear_all(self) -> int:
        """
        Clear all records from storage.
        
        Returns:
            Number of records cleared
        """
        count = len(self._storage)
        self._storage.clear()
        return count
    
    def get_count(self) -> int:
        """
        Get the total number of stored records.
        
        Returns:
            Total count of records
        """
        return len(self._storage)


data_store = DataStore()
