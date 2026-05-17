import aiosqlite
import uuid
from typing import Optional, Dict, Any
from core.security.crypto import encrypt, decrypt

class ContextEngine:
    def __init__(self, db_path: str = "execra.db"):
        self.db_path = db_path

    async def create_session(self, domain: str) -> str:
        session_id = str(uuid.uuid4())
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS session_context (session_id TEXT PRIMARY KEY, current_step INTEGER, step_description TEXT, domain TEXT)"
            )
            await db.execute(
                "INSERT INTO session_context (session_id, current_step, step_description, domain) VALUES (?, ?, ?, ?)",
                (session_id, 0, "", domain)
            )
            await db.commit()
        return session_id

    async def update_step(self, session_id: str, step: int, description: str) -> None:
        encrypted_desc = encrypt(description)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE session_context SET current_step = ?, step_description = ? WHERE session_id = ?",
                (step, encrypted_desc, session_id)
            )
            await db.commit()

    async def get_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT session_id, current_step, step_description, domain FROM session_context WHERE session_id = ?",
                (session_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    step_desc = row[2]
                    # Attempt to decrypt if it's set
                    decrypted_desc = decrypt(step_desc) if step_desc else ""
                    return {
                        "session_id": row[0],
                        "current_step": row[1],
                        "step_description": decrypted_desc,
                        "domain": row[3]
                    }
        return None
