from threading import Lock

storage_lock = Lock() 

# note_id: note object
notes_by_id = {}
# user_id -> set(note_ids)
notes_by_user = {}

# Token storage
token_store = {}        # token -> user_id
