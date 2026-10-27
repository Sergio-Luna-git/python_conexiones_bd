"""bbdd.py — Clases de acceso a datos para la base de datos 'employees'
creada por schema_employees.sql.

Encapsula: conexión (gestor de contexto), repositorio de empleados
(CRUD + departamentos + salarios), transacciones y llamadas a
procedimientos/funciones almacenadas. Ver Ud2 — Acceso a Bases de
Datos Relacionales para la explicación detallada de cada clase.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date

import mysql.connector
from mysql.connector import errorcode

from demo_tema2 import DB_CONFIG

FECHA_SIN_FIN = date(9999, 1, 1)  # convención usada en dept_emp y salaries

# ---------------------------------------------------------------------------
#                configuración de conexión base de datos
# ---------------------------------------------------------------------------
# Conexión
# ---------------------------------------------------------------------------
class ConexionBD:
    """Gestor de contexto para una conexión MySQL.

    Uso:
        with ConexionBD(DB_CONFIG) as cnx:
            cursor = cnx.cursor()
            ...
    """
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "33006")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "dbrootpass"),
        "database": os.getenv("DB_NAME", "sakila")
    }
    def __init__(self, config: dict):
        self.config = DB_CONFIG
        self.cnx = None

    def __enter__(self) -> mysql.connector.MySQLConnection:
        try:
            self.cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError("Usuario o contraseña incorrectos") from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError(
                    f"La base de datos '{self.config.get('database')}' no existe. "
                    "¿Has cargado schema_employees.sql?"
                ) from err
            raise
        return self.cnx

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.cnx is not None and self.cnx.is_connected():
            self.cnx.close()

# ---------------------------------------------------------------------------
# Modelo
# ---------------------------------------------------------------------------
@dataclass
class Empleado:
    nombre: str
    apellido: str
    fecha_nacimiento: date
    genero: str  # 'M' o 'F'
    fecha_contratacion: date
    emp_no: int | None = None  # se rellena tras insertar


# ---------------------------------------------------------------------------
# Repositorio de empleados
# ---------------------------------------------------------------------------
class RepositorioEmpleados:
    """Operaciones CRUD sobre employees, dept_emp y salaries."""

    def __init__(self, config: dict):
        self.config = config

    def insertar(self, empleado: Empleado) -> Empleado:
        """Inserta un empleado y devuelve el mismo objeto con el emp_no asignado."""
        consulta = (
            "INSERT INTO employees "
            "(first_name, last_name, hire_date, gender, birth_date) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        datos = (
            empleado.nombre,
            empleado.apellido,
            empleado.fecha_contratacion,
            empleado.genero,
            empleado.fecha_nacimiento,
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, datos)
            empleado.emp_no = cursor.lastrowid
            cnx.commit()
            cursor.close()
        return empleado

    def asignar_departamento(self, emp_no: int, dept_no: str, desde: date) -> None:
        consulta = (
            "INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date) "
            "VALUES (%s, %s, %s, %s)"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, (emp_no, dept_no, desde, FECHA_SIN_FIN))
            cnx.commit()
            cursor.close()

    def insertar_salario(self, emp_no: int, salario: int, desde: date, hasta: date = FECHA_SIN_FIN) -> None:
        consulta = (
            "INSERT INTO salaries (emp_no, salary, from_date, to_date) "
            "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)"
        )
        datos = {"emp_no": emp_no, "salary": salario, "from_date": desde, "to_date": hasta}
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, datos)
            cnx.commit()
            cursor.close()

    def actualizar_apellido(self, emp_no: int, nuevo_apellido: str) -> None:
        consulta = "UPDATE employees SET last_name = %s WHERE emp_no = %s"
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, (nuevo_apellido, emp_no))
            cnx.commit()
            cursor.close()

    def eliminar(self, emp_no: int) -> None:
        """Borra el empleado; dept_emp y salaries caen en cascada (ON DELETE CASCADE)."""
        consulta = "DELETE FROM employees WHERE emp_no = %s"
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, (emp_no,))
            cnx.commit()
            cursor.close()

    def buscar_contratados_entre(self, inicio: date, fin: date) -> list[Empleado]:
        consulta = (
            "SELECT emp_no, first_name, last_name, birth_date, gender, hire_date "
            "FROM employees WHERE hire_date BETWEEN %s AND %s"
        )
        resultado = []
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, (inicio, fin))
            for emp_no, nombre, apellido, nacimiento, genero, contratacion in cursor:
                resultado.append(Empleado(nombre, apellido, nacimiento, genero, contratacion, emp_no))
            cursor.close()
        return resultado

    def departamento_actual(self, emp_no: int) -> str | None:
        consulta = (
            "SELECT d.dept_name FROM dept_emp de "
            "JOIN departments d ON d.dept_no = de.dept_no "
            "WHERE de.emp_no = %s AND de.to_date = %s"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, (emp_no, FECHA_SIN_FIN))
            fila = cursor.fetchone()
            cursor.close()
        return fila[0] if fila else None

    def mover_de_departamento(self, cursor, emp_no: int, dept_origen: str, dept_destino: str, fecha: date) -> None:
        """Pensado para usarse DENTRO de un bloque `with Transaccion(cnx) as cursor:`,
        no abre conexión propia: cierra la asignación anterior y abre la nueva
        como una única unidad atómica."""
        cursor.execute(
            "UPDATE dept_emp SET to_date = %s WHERE emp_no = %s AND dept_no = %s AND to_date = %s",
            (fecha, emp_no, dept_origen, FECHA_SIN_FIN),
        )
        cursor.execute(
            "INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date) VALUES (%s, %s, %s, %s)",
            (emp_no, dept_destino, fecha, FECHA_SIN_FIN),
        )


# ---------------------------------------------------------------------------
# Procedimientos y funciones almacenadas
# ---------------------------------------------------------------------------
class RepositorioProcedimientos:
    """Envuelve llamadas al procedimiento almacenado 'multiply'."""

    def __init__(self, config: dict):
        self.config = config

    def multiplicar(self, a: int, b: int) -> int:
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            resultado = cursor.callproc("multiply", (a, b, 0))
            cursor.close()
            return resultado[2]  # el tercer argumento es el OUT


class RepositorioFunciones:
    """Envuelve llamadas a la función almacenada 'antiguedad_anios'."""

    def __init__(self, config: dict):
        self.config = config

    def antiguedad_anios(self, emp_no: int) -> int:
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute("SELECT antiguedad_anios(%s)", (emp_no,))
            valor = cursor.fetchone()[0]
            cursor.close()
            return valor
