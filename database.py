import sqlite3
import os
from flask import g

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventario.db')


def get_db():
    """Retorna la conexión SQLite usando flask.g para reutilizarla en la misma petición."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Cierra la conexión a la BD si existe."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Crea las tablas si no existen e inserta datos de prueba."""
    db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")

    db.executescript("""
        CREATE TABLE IF NOT EXISTS tipos_inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cuenta_contable TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo','Inactivo'))
        );

        CREATE TABLE IF NOT EXISTS articulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            existencia REAL NOT NULL DEFAULT 0,
            id_tipo_inventario INTEGER NOT NULL,
            id_almacen INTEGER,
            costo_unitario REAL NOT NULL DEFAULT 0,
            estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo','Inactivo')),
            FOREIGN KEY (id_tipo_inventario) REFERENCES tipos_inventario(id),
            FOREIGN KEY (id_almacen) REFERENCES almacenes(id)
        );

        CREATE TABLE IF NOT EXISTS almacenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo','Inactivo'))
        );

        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('Entrada','Salida','Ajuste')),
            id_articulo INTEGER NOT NULL,
            id_almacen INTEGER,
            fecha TEXT NOT NULL,
            cantidad REAL NOT NULL,
            monto REAL NOT NULL,
            FOREIGN KEY (id_articulo) REFERENCES articulos(id),
            FOREIGN KEY (id_almacen) REFERENCES almacenes(id)
        );
    """)

    # Insertar datos de prueba si las tablas están vacías
    tipos = db.execute("SELECT COUNT(*) FROM tipos_inventario").fetchone()[0]
    if tipos == 0:
        db.execute("INSERT INTO tipos_inventario (descripcion, cuenta_contable, estado) VALUES (?, ?, ?)",
                   ('Materia Prima', '1110-01', 'Activo'))
        db.execute("INSERT INTO tipos_inventario (descripcion, cuenta_contable, estado) VALUES (?, ?, ?)",
                   ('Producto Terminado', '1110-02', 'Activo'))
        db.execute("INSERT INTO tipos_inventario (descripcion, cuenta_contable, estado) VALUES (?, ?, ?)",
                   ('Suministros de Oficina', '1110-03', 'Activo'))

    almacenes = db.execute("SELECT COUNT(*) FROM almacenes").fetchone()[0]
    if almacenes == 0:
        db.execute("INSERT INTO almacenes (descripcion, estado) VALUES (?, ?)",
                   ('Almacén Central', 'Activo'))
        db.execute("INSERT INTO almacenes (descripcion, estado) VALUES (?, ?)",
                   ('Almacén Norte', 'Activo'))
        db.execute("INSERT INTO almacenes (descripcion, estado) VALUES (?, ?)",
                   ('Almacén Sur', 'Activo'))

    articulos = db.execute("SELECT COUNT(*) FROM articulos").fetchone()[0]
    if articulos == 0:
        db.execute("""INSERT INTO articulos (descripcion, existencia, id_tipo_inventario, id_almacen, costo_unitario, estado)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   ('Papel Bond A4 Resma', 100.0, 3, 1, 5.50, 'Activo'))
        db.execute("""INSERT INTO articulos (descripcion, existencia, id_tipo_inventario, id_almacen, costo_unitario, estado)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   ('Cemento Portland 42.5kg', 200.0, 1, 1, 12.75, 'Activo'))
        db.execute("""INSERT INTO articulos (descripcion, existencia, id_tipo_inventario, id_almacen, costo_unitario, estado)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   ('Silla Ejecutiva', 15.0, 2, 1, 85.00, 'Activo'))

    transacciones = db.execute("SELECT COUNT(*) FROM transacciones").fetchone()[0]
    if transacciones == 0:
        db.execute("""INSERT INTO transacciones (tipo, id_articulo, id_almacen, fecha, cantidad, monto)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   ('Entrada', 1, 1, '2026-10-01', 100.0, 550.0))
        db.execute("""INSERT INTO transacciones (tipo, id_articulo, id_almacen, fecha, cantidad, monto)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   ('Entrada', 2, 1, '2026-10-05', 200.0, 2550.0))
        db.execute("""INSERT INTO transacciones (tipo, id_articulo, id_almacen, fecha, cantidad, monto)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   ('Salida', 1, 1, '2026-10-15', 20.0, 110.0))

    db.commit()
    db.close()
