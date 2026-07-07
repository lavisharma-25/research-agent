import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from src.core.settings import settings

_checkpointer = None
_conn = None


async def get_checkpointer():
    global _checkpointer, _conn

    if _checkpointer is None:
        path = settings.CHAT_HISTORY_PATH / "memory.db"

        _conn = await aiosqlite.connect(str(path))
        _checkpointer = AsyncSqliteSaver(_conn)

    return _checkpointer


async def reset_checkpointer():
    global _checkpointer, _conn

    if _conn:
        await _conn.close()

    _conn = None
    _checkpointer = None