from backEnd.Conexion import Conexion

class EmpleadosCRUD:
    def __init__(self):
        self.llave_aes = "proyectoIUHGGSTN"

    def registrar_empleado_completo(self, usuario, contrasenia, rol_sistema,
                                    nombre, apellido, genero, domicilio, estado_civil,
                                    turno, email, rol_trabajo, nacionalidad, curp,
                                    departamento, rfc, telefono, nss):

        objeto_conexion = Conexion()
        conexion = objeto_conexion.conectar()

        if conexion:
            try:
                conexion.autocommit = False
                cursor = conexion.cursor()

                sql_usuario = """
                              INSERT INTO usuarios (usuario, contrasenia, rol_sistema)
                              VALUES (%s, SHA2(%s, 256), %s) \
                              """
                cursor.execute(sql_usuario, (usuario, contrasenia, rol_sistema))

                id_nuevo_usuario = cursor.lastrowid

                sql_empleado = """
                               INSERT INTO empleado (id_usuario, nombre_empleado, apellido_empleado, genero, domicilio,
                                                     estado_civil, turno, email, rol_de_trabajo, nacionalidad,
                                                     curp, departamento, rfc, telefono, nss)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                       AES_ENCRYPT(%s, %s),
                                       AES_ENCRYPT(%s, %s),
                                       AES_ENCRYPT(%s, %s)) \
                               """
                valores_empleado = (
                    id_nuevo_usuario, nombre, apellido, genero, domicilio, estado_civil,
                    turno, email, rol_trabajo, nacionalidad, curp, departamento,
                    rfc, self.llave_aes,
                    telefono, self.llave_aes,
                    nss, self.llave_aes
                )

                cursor.execute(sql_empleado, valores_empleado)

                conexion.commit()
                return True, "Empleado y credenciales registrados correctamente."

            except Exception as e:
                conexion.rollback()
                return False, f"Error al registrar. Se canceló la operación: {e}"

            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

        else:
            return False, "No se pudo conectar a la base de datos correctamente."

    def mostrar_empleados_admin(self):
        #Para el admin solamente que va a mostrar tados sensibles desencriptados
        objeto_conexion = Conexion()
        conexion = objeto_conexion.conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                sql = """
                      SELECT id_empleado, 
                             nombre_empleado, 
                             apellido_empleado, 
                             genero,
                             domicilio,
                             estado_civil, 
                             turno,
                             email, 
                             rol_de_trabajo, 
                             nacionalidad, 
                             curp, 
                             departamento,
                             CAST(AES_DECRYPT(rfc, %s) AS CHAR)      AS rfc,
                             CAST(AES_DECRYPT(telefono, %s) AS CHAR) AS telefono,
                             CAST(AES_DECRYPT(nss, %s) AS CHAR)      AS nss
                      FROM empleado 
                      """

                cursor.execute(sql, (self.llave_aes, self.llave_aes, self.llave_aes))
                resultados = cursor.fetchall()
                return True, resultados
            except Exception as e:
                return False, f"Error al consultar empleados: {e}"

            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

        else:
            return False, "Error de conexión."

    def mostrar_empleados_normal(self):
        #Esta es la vista de empleados solamente con los datos encriptados.
        objeto_conexion = Conexion()
        conexion = objeto_conexion.conectar()

        if conexion:
            try:
                cursor = conexion.cursor()
                # Se va a utilizar un texto generico de ocutlo
                sql = """
                      SELECT id_empleado, 
                             nombre_empleado, 
                             apellido_empleado,
                             genero, 
                             domicilio,
                             estado_civil, 
                             turno, 
                             email, 
                             rol_de_trabajo, 
                             nacionalidad,
                             curp, 
                             departamento,
                             '*** OCULTO ***' AS rfc,
                             '*** OCULTO ***' AS telefono,
                             '*** OCULTO ***' AS nss
                      FROM empleado 
                      """
                cursor.execute(sql)
                resultados = cursor.fetchall()
                return True, resultados
            except Exception as e:
                return False, f"Error al consultar empleados: {e}"
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            return False, "Error de conexión."

    def modificar_empleado (self, id_empleado, id_usuario, nombre, apellido, genero, domicilio, estado_civil,
                           turno, email, rol, nacionalidad, curp, departamento, rfc, telefono, nss):
        objeto_conexion = Conexion()
        conexion = objeto_conexion.conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                sql = """
                      UPDATE empleado
                      SET id_usuario        = %s, 
                          nombre_empleado   = %s, 
                          apellido_empleado = %s, 
                          genero            = %s,
                          domicilio         = %s, 
                          estado_civil      = %s,
                          turno             = %s,
                          email             = %s,
                          rol_de_trabajo    = %s,
                          nacionalidad      = %s, 
                          curp              = %s, 
                          departamento      = %s,
                          rfc               = AES_ENCRYPT(%s, %s),
                          telefono          = AES_ENCRYPT(%s, %s),
                          nss               = AES_ENCRYPT(%s, %s)
                      WHERE id_empleado = %s 
                      """
                valores = (
                    id_usuario, nombre, apellido, genero, domicilio, estado_civil,
                    turno, email, rol, nacionalidad, curp, departamento,
                    rfc, self.llave_aes,
                    telefono, self.llave_aes,
                    nss, self.llave_aes,
                    id_empleado
                )
                cursor.execute(sql, valores)
                conexion.commit()
                return True, "Empleado actualizado correctamente."
            except Exception as e:
                return False, f"Error al actualizar empleado: {e}"

            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()

        else:
            return False, "Error de conexión."

    def eliminar_empleado(self, id_empleado):
        """Elimina un registro completo buscando por su id_empleado."""
        objeto_conexion = Conexion()
        conexion = objeto_conexion.conectar()

        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "DELETE FROM empleado WHERE id_empleado = %s"

                # La coma es obligatoria en Python para indicar que es una tupla de un solo elemento
                cursor.execute(sql, (id_empleado,))
                conexion.commit()

                return True, "Empleado eliminado correctamente."
            except Exception as e:
                return False, f"Error al eliminar empleado: {e}"
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            return False, "Error de conexión."

    def validar_login(self, usuario, contrasenia):
        """
        #esta funcion va a ayudarte Gio a que en la de login puedas verificar según el Usuario y contraseña que tipo de Rol del coso
        #de la apliacion va a usar y la diferencia sobre que cosas puede ver

        Gracias Isaac, eres grande
        Un abrazo.
        """

        objeto_conexion = Conexion()
        conexion = objeto_conexion.conectar()

        if conexion:
            try:
                cursor = conexion.cursor()

                sql = """
                      SELECT id_usuario, rol_sistema
                      FROM usuarios
                      WHERE usuario = %s \
                        AND contrasenia = SHA2(%s, 256)
                      """
                cursor.execute(sql, (usuario, contrasenia))

                resultado = cursor.fetchone()

                if resultado:
                    return True, "Login exitoso", resultado[1]
                else:
                    return False, "Usuario o contraseña incorrectos", None

            except Exception as e:
                return False, f"Error al validar credenciales: {e}", None

            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            return False, "Error de conexión a la base de datos.", None
