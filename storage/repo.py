import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class Repository:
    #Generic repository for JSON-based storage.
    
    def __init__(self, filename: str, storage_dir: Optional[Path] = None):
        """
        Initialize repository.
        
        Args:
            filename: Name of file to store data
            storage_dir: Directory for storage (default: ~/.personal_assistant)
        """
        if storage_dir is None:
            storage_dir = Path.home() / '.personal_assistant'
        
        self.storage_dir = storage_dir
        self.filepath = storage_dir / filename
        self._ensure_storage_directory()
    
    def _ensure_storage_directory(self):
        """Create storage directory if it doesn't exist."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, data: List[Dict]) -> bool:
        """
        Save data to JSON file.
        
        Args:
            data: List of dictionaries to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Помилка збереження: {e}")
            return False
    
    def load(self) -> List[Dict]:
        """
        Load data from JSON file.
        
        Returns:
            List of dictionaries, empty list if error
        """
        if not self.filepath.exists():
            return []
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Помилка завантаження: {e}")
            return []
        except Exception as e:
            print(f"Неочікувана помилка: {e}")
            return []
    
    def exists(self) -> bool:
        """Check if storage file exists."""
        return self.filepath.exists()
    
    def clear(self) -> bool:
        """Delete storage file."""
        try:
            if self.exists():
                self.filepath.unlink()
                return True
            return False
        except Exception as e:
            print(f"Помилка видалення: {e}")
            return False


class ContactRepository:
    """Repository for managing contact data."""
    
    def __init__(self, filename: str = "contacts.json"):
        """
        Initialize contact repository.
        
        Args:
            filename: Name of file to store contacts
        """
        self.repo = Repository(filename)
    
    def save_contacts(self, contacts: List) -> bool:
        """
        Save contacts to storage.
        
        Args:
            contacts: List of contact objects
            
        Returns:
            True if successful, False otherwise
        """
        data = [self._contact_to_dict(contact) for contact in contacts]
        return self.repo.save(data)
    
    def load_contacts(self) -> List:
        """
        Load contacts from storage.
        
        Returns:
            List of contact objects
        """
        data = self.repo.load()
        from contacts.models import Contact
        return [Contact.from_dict(contact_dict) for contact_dict in data]
    
    def _contact_to_dict(self, contact) -> Dict:
        """Convert contact object to dictionary."""
        if hasattr(contact, 'to_dict'):
            return contact.to_dict()
        
        return {
            'name': getattr(contact, 'name', ''),
            'phone': getattr(contact, 'phone', None),
            'email': getattr(contact, 'email', None),
            'birthday': getattr(contact, 'birthday', None),
            'address': getattr(contact, 'address', None)
        }
    
    def clear(self) -> bool:
        """Clear all contacts."""
        return self.repo.clear()


class NoteRepository:
    """Repository for managing note data."""
    
    def __init__(self, filename: str = "notes.json"):
        """
        Initialize note repository.
        
        Args:
            filename: Name of file to store notes
        """
        self.repo = Repository(filename)
    
    def save_notes(self, notes: List) -> bool:
        """
        Save notes to storage.
        
        Args:
            notes: List of note objects
            
        Returns:
            True if successful, False otherwise
        """
        data = [self._note_to_dict(note) for note in notes]
        return self.repo.save(data)
    
    def load_notes(self) -> List:
        """
        Load notes from storage.
        
        Returns:
            List of note objects
        """
        data = self.repo.load()
        from notes.models import Note
        return [Note.from_dict(note_dict) for note_dict in data]
    
    def _note_to_dict(self, note) -> Dict:
        """Convert note object to dictionary."""
        if hasattr(note, 'to_dict'):
            return note.to_dict()
        
        return {
            'text': getattr(note, 'text', ''),
            'tags': getattr(note, 'tags', [])
        }
    
    def clear(self) -> bool:
        """Clear all notes."""
        return self.repo.clear()