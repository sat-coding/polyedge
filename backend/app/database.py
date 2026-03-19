import sqlite3
from pathlib import Path
from app.config import settings

def get_conn() -> sqlite3.Connection:
    db = Path(settings.database_path)
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript("""
CREATE TABLE IF NOT EXISTS markets (id TEXT PRIMARY KEY,question TEXT NOT NULL,category TEXT,yes_price REAL,no_price REAL,volume_24h REAL,liquidity REAL,end_date TEXT,resolved INTEGER DEFAULT 0,resolution TEXT,updated_at TEXT DEFAULT (datetime('now')));
CREATE TABLE IF NOT EXISTS signals (id INTEGER PRIMARY KEY AUTOINCREMENT,market_id TEXT,scan_timestamp TEXT DEFAULT (datetime('now')),ai_probability REAL,confidence TEXT,ev_per_dollar REAL,kelly_fraction REAL,suggested_position REAL,direction TEXT,reasoning TEXT,model_used TEXT,reasoning_effort TEXT,risk_check_result TEXT);
CREATE TABLE IF NOT EXISTS trades (id INTEGER PRIMARY KEY AUTOINCREMENT,signal_id INTEGER,market_id TEXT,mode TEXT NOT NULL,direction TEXT NOT NULL,price REAL,size REAL,shares REAL,fee REAL,order_id TEXT,status TEXT DEFAULT pending,executed_at TEXT,created_at TEXT DEFAULT (datetime('now')));
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY AUTOINCREMENT,market_id TEXT,direction TEXT,entry_price REAL,current_price REAL,shares REAL,cost_basis REAL,unrealized_pnl REAL,log_return REAL,opened_at TEXT,closed_at TEXT,status TEXT DEFAULT open);
CREATE TABLE IF NOT EXISTS backtest_runs (id INTEGER PRIMARY KEY AUTOINCREMENT,params TEXT,start_date TEXT,end_date TEXT,total_trades INTEGER,win_rate REAL,total_pnl REAL,max_drawdown REAL,sharpe_ratio REAL,equity_curve TEXT,created_at TEXT DEFAULT (datetime('now')));
    """)
    conn.commit(); conn.close()

if __name__ == "__main__":
    init_db(); print("DB initialized")
