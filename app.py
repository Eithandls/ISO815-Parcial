from flask import Flask, render_template, request, redirect, url_for, flash, g
from database import get_db, init_db, close_db

app = Flask(__name__)
app.secret_key = 'iso815-secret-key-2026'

# Inicializar la base de datos al arrancar
with app.app_context():
    init_db()


@app.teardown_appcontext
def teardown_db(exception):
    close_db()


# ─────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────

@app.route('/')
def dashboard():
    db = get_db()
    total_articulos = db.execute(
        "SELECT COUNT(*) FROM articulos WHERE estado = 'Activo'"
    ).fetchone()[0]
    total_almacenes = db.execute(
        "SELECT COUNT(*) FROM almacenes WHERE estado = 'Activo'"
    ).fetchone()[0]
    total_transacciones = db.execute(
        "SELECT COUNT(*) FROM transacciones"
    ).fetchone()[0]
    total_tipos = db.execute(
        "SELECT COUNT(*) FROM tipos_inventario WHERE estado = 'Activo'"
    ).fetchone()[0]
    ultimas_transacciones = db.execute("""
        SELECT t.id, t.tipo, t.fecha, t.cantidad, t.monto,
               a.descripcion AS articulo,
               al.descripcion AS almacen
        FROM transacciones t
        JOIN articulos a ON a.id = t.id_articulo
        LEFT JOIN almacenes al ON al.id = t.id_almacen
        ORDER BY t.id DESC
        LIMIT 5
    """).fetchall()
    return render_template(
        'dashboard.html',
        total_articulos=total_articulos,
        total_almacenes=total_almacenes,
        total_transacciones=total_transacciones,
        total_tipos=total_tipos,
        ultimas_transacciones=ultimas_transacciones,
    )


# ─────────────────────────────────────────
# TIPOS DE INVENTARIO
# ─────────────────────────────────────────

@app.route('/tipos-inventario')
def tipos_inventario_index():
    db = get_db()
    tipos = db.execute("SELECT * FROM tipos_inventario ORDER BY id DESC").fetchall()
    return render_template('tipos_inventario/index.html', tipos=tipos)


@app.route('/tipos-inventario/nuevo', methods=['GET', 'POST'])
def tipos_inventario_nuevo():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion', '').strip()
        cuenta_contable = request.form.get('cuenta_contable', '').strip()
        estado = request.form.get('estado', 'Activo')
        if not descripcion or not cuenta_contable:
            flash('Todos los campos son requeridos.', 'danger')
            return render_template('tipos_inventario/form.html', tipo=None)
        db = get_db()
        db.execute(
            "INSERT INTO tipos_inventario (descripcion, cuenta_contable, estado) VALUES (?, ?, ?)",
            (descripcion, cuenta_contable, estado)
        )
        db.commit()
        flash('Tipo de inventario creado exitosamente.', 'success')
        return redirect(url_for('tipos_inventario_index'))
    return render_template('tipos_inventario/form.html', tipo=None)


@app.route('/tipos-inventario/<int:id>/editar', methods=['GET', 'POST'])
def tipos_inventario_editar(id):
    db = get_db()
    tipo = db.execute("SELECT * FROM tipos_inventario WHERE id = ?", (id,)).fetchone()
    if tipo is None:
        flash('Tipo de inventario no encontrado.', 'danger')
        return redirect(url_for('tipos_inventario_index'))
    if request.method == 'POST':
        descripcion = request.form.get('descripcion', '').strip()
        cuenta_contable = request.form.get('cuenta_contable', '').strip()
        estado = request.form.get('estado', 'Activo')
        if not descripcion or not cuenta_contable:
            flash('Todos los campos son requeridos.', 'danger')
            return render_template('tipos_inventario/form.html', tipo=tipo)
        db.execute(
            "UPDATE tipos_inventario SET descripcion=?, cuenta_contable=?, estado=? WHERE id=?",
            (descripcion, cuenta_contable, estado, id)
        )
        db.commit()
        flash('Tipo de inventario actualizado exitosamente.', 'success')
        return redirect(url_for('tipos_inventario_index'))
    return render_template('tipos_inventario/form.html', tipo=tipo)


@app.route('/tipos-inventario/<int:id>/eliminar', methods=['POST'])
def tipos_inventario_eliminar(id):
    db = get_db()
    # Verificar FK: artículos que usan este tipo
    uso = db.execute(
        "SELECT COUNT(*) FROM articulos WHERE id_tipo_inventario = ?", (id,)
    ).fetchone()[0]
    if uso > 0:
        flash(f'No se puede eliminar: {uso} artículo(s) están asociados a este tipo.', 'danger')
        return redirect(url_for('tipos_inventario_index'))
    db.execute("DELETE FROM tipos_inventario WHERE id = ?", (id,))
    db.commit()
    flash('Tipo de inventario eliminado.', 'success')
    return redirect(url_for('tipos_inventario_index'))


# ─────────────────────────────────────────
# ARTÍCULOS
# ─────────────────────────────────────────

@app.route('/articulos')
def articulos_index():
    db = get_db()
    articulos = db.execute("""
        SELECT a.*, t.descripcion AS tipo_descripcion
        FROM articulos a
        JOIN tipos_inventario t ON t.id = a.id_tipo_inventario
        ORDER BY a.id DESC
    """).fetchall()
    return render_template('articulos/index.html', articulos=articulos)


@app.route('/articulos/nuevo', methods=['GET', 'POST'])
def articulos_nuevo():
    db = get_db()
    tipos = db.execute(
        "SELECT * FROM tipos_inventario WHERE estado='Activo' ORDER BY descripcion"
    ).fetchall()
    if request.method == 'POST':
        descripcion = request.form.get('descripcion', '').strip()
        existencia = request.form.get('existencia', '0')
        id_tipo = request.form.get('id_tipo_inventario', '')
        costo = request.form.get('costo_unitario', '0')
        estado = request.form.get('estado', 'Activo')
        if not descripcion or not id_tipo:
            flash('Los campos descripción y tipo de inventario son requeridos.', 'danger')
            return render_template('articulos/form.html', articulo=None, tipos=tipos)
        try:
            existencia = float(existencia)
            costo = float(costo)
        except ValueError:
            flash('Existencia y costo deben ser valores numéricos.', 'danger')
            return render_template('articulos/form.html', articulo=None, tipos=tipos)
        db.execute(
            "INSERT INTO articulos (descripcion, existencia, id_tipo_inventario, costo_unitario, estado) VALUES (?,?,?,?,?)",
            (descripcion, existencia, int(id_tipo), costo, estado)
        )
        db.commit()
        flash('Artículo creado exitosamente.', 'success')
        return redirect(url_for('articulos_index'))
    return render_template('articulos/form.html', articulo=None, tipos=tipos)


@app.route('/articulos/<int:id>/editar', methods=['GET', 'POST'])
def articulos_editar(id):
    db = get_db()
    articulo = db.execute("SELECT * FROM articulos WHERE id=?", (id,)).fetchone()
    if articulo is None:
        flash('Artículo no encontrado.', 'danger')
        return redirect(url_for('articulos_index'))
    tipos = db.execute(
        "SELECT * FROM tipos_inventario WHERE estado='Activo' ORDER BY descripcion"
    ).fetchall()
    if request.method == 'POST':
        descripcion = request.form.get('descripcion', '').strip()
        existencia = request.form.get('existencia', '0')
        id_tipo = request.form.get('id_tipo_inventario', '')
        costo = request.form.get('costo_unitario', '0')
        estado = request.form.get('estado', 'Activo')
        if not descripcion or not id_tipo:
            flash('Los campos descripción y tipo de inventario son requeridos.', 'danger')
            return render_template('articulos/form.html', articulo=articulo, tipos=tipos)
        try:
            existencia = float(existencia)
            costo = float(costo)
        except ValueError:
            flash('Existencia y costo deben ser valores numéricos.', 'danger')
            return render_template('articulos/form.html', articulo=articulo, tipos=tipos)
        db.execute(
            "UPDATE articulos SET descripcion=?, existencia=?, id_tipo_inventario=?, costo_unitario=?, estado=? WHERE id=?",
            (descripcion, existencia, int(id_tipo), costo, estado, id)
        )
        db.commit()
        flash('Artículo actualizado exitosamente.', 'success')
        return redirect(url_for('articulos_index'))
    return render_template('articulos/form.html', articulo=articulo, tipos=tipos)


@app.route('/articulos/<int:id>/editar/ver', methods=['GET'])
def articulos_ver(id):
    db = get_db()
    articulo = db.execute("""
        SELECT a.*, t.descripcion AS tipo_descripcion
        FROM articulos a
        JOIN tipos_inventario t ON t.id = a.id_tipo_inventario
        WHERE a.id=?
    """, (id,)).fetchone()
    if articulo is None:
        flash('Artículo no encontrado.', 'danger')
        return redirect(url_for('articulos_index'))
    transacciones = db.execute("""
        SELECT t.*, al.descripcion AS almacen
        FROM transacciones t
        LEFT JOIN almacenes al ON al.id = t.id_almacen
        WHERE t.id_articulo = ?
        ORDER BY t.id DESC
    """, (id,)).fetchall()
    return render_template('articulos/ver.html', articulo=articulo, transacciones=transacciones)


@app.route('/articulos/<int:id>/ver', methods=['GET'])
def articulos_detalle(id):
    db = get_db()
    articulo = db.execute("""
        SELECT a.*, t.descripcion AS tipo_descripcion
        FROM articulos a
        JOIN tipos_inventario t ON t.id = a.id_tipo_inventario
        WHERE a.id=?
    """, (id,)).fetchone()
    if articulo is None:
        flash('Artículo no encontrado.', 'danger')
        return redirect(url_for('articulos_index'))
    transacciones = db.execute("""
        SELECT t.*, al.descripcion AS almacen
        FROM transacciones t
        LEFT JOIN almacenes al ON al.id = t.id_almacen
        WHERE t.id_articulo = ?
        ORDER BY t.id DESC
    """, (id,)).fetchall()
    return render_template('articulos/ver.html', articulo=articulo, transacciones=transacciones)


@app.route('/articulos/<int:id>/eliminar', methods=['POST'])
def articulos_eliminar(id):
    db = get_db()
    uso = db.execute(
        "SELECT COUNT(*) FROM transacciones WHERE id_articulo = ?", (id,)
    ).fetchone()[0]
    if uso > 0:
        flash(f'No se puede eliminar: {uso} transacción(es) están asociadas a este artículo.', 'danger')
        return redirect(url_for('articulos_index'))
    db.execute("DELETE FROM articulos WHERE id=?", (id,))
    db.commit()
    flash('Artículo eliminado.', 'success')
    return redirect(url_for('articulos_index'))


# ─────────────────────────────────────────
# ALMACENES
# ─────────────────────────────────────────

@app.route('/almacenes')
def almacenes_index():
    db = get_db()
    almacenes = db.execute("SELECT * FROM almacenes ORDER BY id DESC").fetchall()
    return render_template('almacenes/index.html', almacenes=almacenes)


@app.route('/almacenes/nuevo', methods=['GET', 'POST'])
def almacenes_nuevo():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion', '').strip()
        estado = request.form.get('estado', 'Activo')
        if not descripcion:
            flash('La descripción es requerida.', 'danger')
            return render_template('almacenes/form.html', almacen=None)
        db = get_db()
        db.execute(
            "INSERT INTO almacenes (descripcion, estado) VALUES (?, ?)",
            (descripcion, estado)
        )
        db.commit()
        flash('Almacén creado exitosamente.', 'success')
        return redirect(url_for('almacenes_index'))
    return render_template('almacenes/form.html', almacen=None)


@app.route('/almacenes/<int:id>/editar', methods=['GET', 'POST'])
def almacenes_editar(id):
    db = get_db()
    almacen = db.execute("SELECT * FROM almacenes WHERE id=?", (id,)).fetchone()
    if almacen is None:
        flash('Almacén no encontrado.', 'danger')
        return redirect(url_for('almacenes_index'))
    if request.method == 'POST':
        descripcion = request.form.get('descripcion', '').strip()
        estado = request.form.get('estado', 'Activo')
        if not descripcion:
            flash('La descripción es requerida.', 'danger')
            return render_template('almacenes/form.html', almacen=almacen)
        db.execute(
            "UPDATE almacenes SET descripcion=?, estado=? WHERE id=?",
            (descripcion, estado, id)
        )
        db.commit()
        flash('Almacén actualizado exitosamente.', 'success')
        return redirect(url_for('almacenes_index'))
    return render_template('almacenes/form.html', almacen=almacen)


@app.route('/almacenes/<int:id>/eliminar', methods=['POST'])
def almacenes_eliminar(id):
    db = get_db()
    uso = db.execute(
        "SELECT COUNT(*) FROM transacciones WHERE id_almacen=? OR id_almacen_destino=?", (id, id)
    ).fetchone()[0]
    if uso > 0:
        flash(f'No se puede eliminar: {uso} transacción(es) están asociadas a este almacén.', 'danger')
        return redirect(url_for('almacenes_index'))
    db.execute("DELETE FROM almacenes WHERE id=?", (id,))
    db.commit()
    flash('Almacén eliminado.', 'success')
    return redirect(url_for('almacenes_index'))


# ─────────────────────────────────────────
# TRANSACCIONES
# ─────────────────────────────────────────

@app.route('/transacciones')
def transacciones_index():
    db = get_db()
    transacciones = db.execute("""
        SELECT t.id, t.tipo, t.fecha, t.cantidad, t.monto,
               a.descripcion AS articulo,
               al.descripcion AS almacen,
               ald.descripcion AS almacen_destino
        FROM transacciones t
        JOIN articulos a ON a.id = t.id_articulo
        LEFT JOIN almacenes al ON al.id = t.id_almacen
        LEFT JOIN almacenes ald ON ald.id = t.id_almacen_destino
        ORDER BY t.id DESC
    """).fetchall()
    return render_template('transacciones/index.html', transacciones=transacciones)


@app.route('/transacciones/nueva', methods=['GET', 'POST'])
def transacciones_nueva():
    db = get_db()
    articulos = db.execute(
        "SELECT * FROM articulos WHERE estado='Activo' ORDER BY descripcion"
    ).fetchall()
    almacenes = db.execute(
        "SELECT * FROM almacenes WHERE estado='Activo' ORDER BY descripcion"
    ).fetchall()

    if request.method == 'POST':
        tipo = request.form.get('tipo', '').strip()
        id_articulo = request.form.get('id_articulo', '')
        id_almacen = request.form.get('id_almacen', '') or None
        id_almacen_destino = request.form.get('id_almacen_destino', '') or None
        fecha = request.form.get('fecha', '').strip()
        cantidad_str = request.form.get('cantidad', '0')

        # Validaciones básicas
        if not tipo or not id_articulo or not fecha:
            flash('Tipo, artículo y fecha son requeridos.', 'danger')
            return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)

        try:
            cantidad = float(cantidad_str)
        except ValueError:
            flash('La cantidad debe ser un valor numérico.', 'danger')
            return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)

        if cantidad <= 0:
            flash('La cantidad debe ser mayor que cero.', 'danger')
            return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)

        if tipo == 'Traslado' and not id_almacen_destino:
            flash('Para un Traslado se requiere el almacén de destino.', 'danger')
            return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)

        # Obtener artículo
        articulo = db.execute("SELECT * FROM articulos WHERE id=?", (int(id_articulo),)).fetchone()
        if articulo is None:
            flash('Artículo no encontrado.', 'danger')
            return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)

        costo_unitario = articulo['costo_unitario']
        monto = cantidad * costo_unitario

        # Reglas de negocio
        if tipo == 'Entrada':
            nueva_existencia = articulo['existencia'] + cantidad
            db.execute("UPDATE articulos SET existencia=? WHERE id=?", (nueva_existencia, int(id_articulo)))

        elif tipo == 'Salida':
            if articulo['existencia'] < cantidad:
                flash(f"Existencia insuficiente. Disponible: {articulo['existencia']}", 'danger')
                return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)
            nueva_existencia = articulo['existencia'] - cantidad
            db.execute("UPDATE articulos SET existencia=? WHERE id=?", (nueva_existencia, int(id_articulo)))

        elif tipo == 'Traslado':
            # No cambia existencia total, solo se registra el movimiento
            pass

        elif tipo == 'Ajuste':
            # Suma o resta (cantidad puede ser negativa para corrección)
            nueva_existencia = articulo['existencia'] + cantidad
            if nueva_existencia < 0:
                flash('El ajuste resultaría en existencia negativa.', 'danger')
                return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)
            db.execute("UPDATE articulos SET existencia=? WHERE id=?", (nueva_existencia, int(id_articulo)))

        # Insertar transacción
        db.execute("""
            INSERT INTO transacciones (tipo, id_articulo, id_almacen, id_almacen_destino, fecha, cantidad, monto)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tipo,
            int(id_articulo),
            int(id_almacen) if id_almacen else None,
            int(id_almacen_destino) if id_almacen_destino else None,
            fecha,
            cantidad,
            monto
        ))
        db.commit()
        flash('Transacción registrada exitosamente.', 'success')
        return redirect(url_for('transacciones_index'))

    return render_template('transacciones/form.html', articulos=articulos, almacenes=almacenes)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
