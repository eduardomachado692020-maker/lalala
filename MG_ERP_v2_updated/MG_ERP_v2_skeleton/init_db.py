import sqlite3, os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
# Allow the database location to be overridden via the DB_PATH environment
# variable.  This mirrors the configuration in ``app.py`` and ensures that
# both the application and initialisation script operate on the same
# database file when customised.  When the environment variable is
# undefined it falls back to ``erp.db`` in this directory.
DB_PATH = os.environ.get("DB_PATH", os.path.join(APP_DIR, "erp.db"))

DDL = [
    """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        modelo TEXT,
        capacidade TEXT,
        cor TEXT,
        sku TEXT UNIQUE
    );
    """
    ,
    """
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        preco_lista REAL DEFAULT 0,
        preco_unit REAL DEFAULT 0,
        custo_snapshot REAL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """
    ,
    """
    -- Stock movements for products.  The 'origem' column uses a check
    -- constraint to enforce that only recognised event types are stored.
    -- Additional values 'ajuste_edit_prod' and 'venda_edit' are
    -- permitted to support editing operations without violating
    -- integrity constraints.  See the accompanying application code for
    -- how these values are used.
    CREATE TABLE IF NOT EXISTS stock_moves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        origem TEXT NOT NULL CHECK(origem IN ('ajuste', 'venda', 'ajuste_edit_prod', 'venda_edit')),
        quantidade INTEGER NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """
]

SEED = [
    ("Console XYZ","Slim","500GB","Preto","XYZ-SLIM-500GB-PT-00001"),
    ("Console XYZ","Slim","1TB","Preto","XYZ-SLIM-1TB-PT-00001")
]

def main() -> None:
    """Initialise or update the ERP database.

    This function creates the required tables and optionally seeds the
    database with example data when it is empty.  Seeding can be
    disabled by setting the ``SEED_DB`` environment variable to ``0``.
    The database location is determined by ``DB_PATH`` in the environment
    or defaults to ``erp.db`` in the application directory.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # Execute each DDL statement defined above.  Separating them into
    # individual entries ensures that a failure in one statement does
    # not prevent the others from running.
    for stmt in DDL:
        cur.execute(stmt)
    # Determine whether to seed the database.  If the environment
    # variable SEED_DB is set to '0', seeding is skipped.  Otherwise it
    # proceeds when the products table is empty.
    seed_enabled = os.environ.get("SEED_DB", "1") != "0"
    if seed_enabled:
        cur.execute("SELECT COUNT(*) FROM products")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO products (nome,modelo,capacidade,cor,sku) VALUES (?,?,?,?,?)",
                SEED,
            )
            # Seed a couple of sales entries tied to the seeded products
            cur.execute(
                "INSERT INTO sales (product_id, preco_lista, preco_unit, custo_snapshot) VALUES (1, 2500, 2400, 2000)"
            )
            cur.execute(
                "INSERT INTO sales (product_id, preco_lista, preco_unit, custo_snapshot) VALUES (2, 3000, 2899, 2300)"
            )
    con.commit()
    con.close()
    print(f"ERP DB criado/atualizado em: {DB_PATH}")

if __name__ == '__main__':
    main()
