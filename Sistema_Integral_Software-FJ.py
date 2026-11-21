
import math
from abc import ABC, abstractmethod
from datetime import datetime

# Excepciones personalizadas
class ErrorDisponibilidad(Exception):
    pass
class ErrorReserva(Exception):
    pass


# Función para registrar errores
def registrar_error(error):

    with open("registro_errores.txt", "a", encoding="utf-8") as archivo:

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        archivo.write( f"{fecha} - {type(error).__name__}: {error}\n" )


# Clase abstracta
class Entidad(ABC):
    def __init__(self, identificador):
        self.identificador = identificador
    @abstractmethod
    def mostrar_info(self):
        pass


# Clase Cliente
class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, contacto):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto válido")

        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise ValueError("El correo no es válido")

        if not isinstance(contacto, str):
            raise ValueError("El contacto tiene texto ")

        if not contacto.isdigit() or len(contacto) != 10:
            raise ValueError("El contacto debe tener 10 dígitos")

        self.__nombre = nombre
        self.__correo = correo
        self.__contacto = contacto

    def mostrar_info(self):
        return (f"Cliente: {self.__nombre}\n"
                f"Correo: {self.__correo}\n"
                f"Contacto: {self.__contacto}")



# Clase abstracta Servicio
class Servicio(ABC):

    def __init__(self, codigo, nombre, tarifa_base):
        if not isinstance(codigo, int) or isinstance(codigo, bool) or codigo <= 0:
            raise ValueError("El código debe ser un número entero positivo")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del servicio no puede estar vacío")

        if (isinstance(tarifa_base, bool)
                or not isinstance(tarifa_base, (int, float))
                or not math.isfinite(tarifa_base)
                or tarifa_base <= 0):
            raise ValueError("La tarifa debe ser un número positivo y finito")

        self.__codigo = codigo
        self.__nombre = nombre.strip()
        self.__tarifa_base = tarifa_base

    @property
    def codigo(self):
        return self.__codigo
    @property
    def nombre(self):
        return self.__nombre
    @property
    def tarifa_base(self):
        return self.__tarifa_base
    @abstractmethod
    def calcular_costo(self, cantidad):
        pass
    @abstractmethod
    def mostrar_descripcion(self):
        pass
    @abstractmethod
    def validar_disponibilidad(self):
        pass


# Clase ReservaSala
class ReservaSala(Servicio):

    def __init__(self, codigo, nombre, tarifa_base, disponible):
        super().__init__(codigo, nombre, tarifa_base)

        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad debe ser True o False")

        self.__disponible = disponible

    def calcular_costo(self, cantidad):
        if (isinstance(cantidad, bool)
                or not isinstance(cantidad, (int, float))
                or not math.isfinite(cantidad)
                or cantidad <= 0):
            raise ValueError("Las horas deben ser un número positivo y finito")
        costo = self.tarifa_base * cantidad
        if not math.isfinite(costo):
            raise ValueError("El costo calculado debe ser finito")
        return costo

    def mostrar_descripcion(self):
        return (f"Servicio: {self.nombre}\n"
                f"Código: {self.codigo}\n"
                f"Tarifa por hora: ${self.tarifa_base}")

    def validar_disponibilidad(self):
        if not self.__disponible:
            raise ErrorDisponibilidad("La sala no está disponible")
        return True


# Clase AlquilerEquipo
class AlquilerEquipo(Servicio):

    def __init__(self, codigo, nombre, tarifa_base, disponible):
        super().__init__(codigo, nombre, tarifa_base)

        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad debe ser True o False")
        self.__disponible = disponible

    def calcular_costo(self, cantidad):
        if (isinstance(cantidad, bool)
                or not isinstance(cantidad, (int, float))
                or not math.isfinite(cantidad)
                or cantidad <= 0):
            raise ValueError("Los días deben ser un número positivo y finito")

        costo = self.tarifa_base * cantidad

        if not math.isfinite(costo):
            raise ValueError("El costo calculado debe ser finito")
        return costo

    def mostrar_descripcion(self):
        return (f"Servicio: {self.nombre}\n"
                f"Código: {self.codigo}\n"
                f"Tarifa por día: ${self.tarifa_base}")

    def validar_disponibilidad(self):
        if not self.__disponible:
            raise ErrorDisponibilidad("El equipo no está disponible")
        return True


# Clase AsesoriaEspecializada
class AsesoriaEspecializada(Servicio):

    def __init__(self, codigo, nombre, tarifa_base, disponible):
        super().__init__(codigo, nombre, tarifa_base)

        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad debe ser True o False")
        self.__disponible = disponible

    def calcular_costo(self, cantidad):
        if (isinstance(cantidad, bool)
                or not isinstance(cantidad, (int, float))
                or not math.isfinite(cantidad)
                or cantidad <= 0):
            raise ValueError("Las horas deben ser un número positivo y finito")

        costo = self.tarifa_base * cantidad

        if not math.isfinite(costo):
            raise ValueError("El costo calculado debe ser finito")
        return costo

    def mostrar_descripcion(self):
        return (f"Servicio: {self.nombre}\n"
                f"Código: {self.codigo}\n"
                f"Tarifa por hora: ${self.tarifa_base}")

    def validar_disponibilidad(self):
        if not self.__disponible:
            raise ErrorDisponibilidad("El especialista no está disponible")
        return True



# Clase Reserva
class Reserva:

    def __init__(self, codigo, cliente, servicio, cantidad):

        # Validar el código de la reserva
        if (not isinstance(codigo, int)
                or isinstance(codigo, bool)
                or codigo <= 0):
            raise ValueError(
                "El código de reserva debe ser un entero positivo")

        # Validar el cliente
        if not isinstance(cliente, Cliente):
            raise ValueError(
                "Debe seleccionar un cliente válido")

        # Validar el servicio
        if not isinstance(servicio, Servicio):
            raise ValueError(
                "Debe seleccionar un servicio válido")

        # Validar la cantidad de horas o días
        if (isinstance(cantidad, bool)
                or not isinstance(cantidad, (int, float))
                or not math.isfinite(cantidad)
                or cantidad <= 0):
            raise ValueError(
                "La cantidad debe ser un número positivo y finito")

        # Atributos privados
        self.__codigo = codigo
        self.__cliente = cliente
        self.__servicio = servicio
        self.__cantidad = cantidad
        self.__estado = "Pendiente"

    # Propiedades de consulta
    @property
    def codigo(self):
        return self.__codigo
    @property
    def cliente(self):
        return self.__cliente
    @property
    def servicio(self):
        return self.__servicio
    @property
    def estado(self):
        return self.__estado

    # Calcular costo con impuestos y descuentos opcionales
    def calcular_costo(self, impuesto=0, descuento=0):

        # Validar los porcentajes
        for nombre, valor in [
            ("impuesto", impuesto),
            ("descuento", descuento)]:
            if (isinstance(valor, bool)
                    or not isinstance(valor, (int, float))
                    or not math.isfinite(valor)
                    or valor < 0
                    or valor > 1):
                raise ValueError(
                    f"El {nombre} debe estar entre 0 y 1")

        # Calcular el costo base
        costo_base = self.__servicio.calcular_costo(
            self.__cantidad)

        # Aplicar impuesto y descuento
        costo_con_impuesto = costo_base * (1 + impuesto)
        costo_final = costo_con_impuesto * (1 - descuento)

        if not math.isfinite(costo_final):
            raise ValueError(
                "El costo final debe ser un número finito")

        return costo_final

    # Confirmar la reserva
    def confirmar_reserva(self, impuesto=0, descuento=0):

        if self.__estado == "Cancelada":
            raise ErrorReserva(
                "No se puede confirmar una reserva cancelada")

        if self.__estado == "Confirmada":
            raise ErrorReserva(
                "La reserva ya está confirmada" )
        try:

            # Verificar disponibilidad del servicio
            self.__servicio.validar_disponibilidad()

            # Calcular costo con los porcentajes indicados
            costo = self.calcular_costo(impuesto, descuento)

        except ErrorDisponibilidad as error:
            raise ErrorReserva(
                "No se pudo confirmar la reserva: servicio no disponible") from error

        # Confirmar solamente si las validaciones fueron exitosas
        self.__estado = "Confirmada"
        return costo

    # Cancelar la reserva
    def cancelar_reserva(self):

        if self.__estado == "Cancelada":
            raise ErrorReserva(
                "La reserva ya está cancelada")

        self.__estado = "Cancelada"
        return "Reserva cancelada"

    # Mostrar información de la reserva
    def mostrar_info(self):

        return (
            f"Reserva: {self.__codigo}\n"
            f"{self.__cliente.mostrar_info()}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Cantidad: {self.__cantidad}\n"
            f"Estado: {self.__estado}")

    # ------------------------------------------------------------------
    # [NUEVO] Propiedades de solo lectura (encapsulación) y procesamiento
    # ------------------------------------------------------------------
    @property
    def codigo(self):
        return self.__codigo

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def procesar(self, descuento=None, impuesto=Servicio.IVA_DEFECTO):
        """Calcula el costo final (con descuento e IVA) y deja la reserva 'Procesada'."""
        if self.__estado != "Confirmada":                 # solo se procesa lo ya confirmado
            raise ErrorReserva(f"Solo se procesa una reserva Confirmada (estado actual: {self.__estado})")
        try:
            costo = self.__servicio.calcular_costo_final(
                self.__cantidad, impuesto=impuesto, descuento=descuento)
        except ErrorCalculo as error:
            # ENCADENAMIENTO: se conserva el error original con 'from'
            raise ErrorReserva(f"No se pudo procesar la reserva {self.__codigo}") from error
        else:                                             # se ejecuta SOLO si no hubo error
            self.__costo_total = costo
            self.__estado = "Procesada"
            return costo
        finally:                                          # se ejecuta SIEMPRE
            registrar_evento(f"Intento de procesar la reserva {self.__codigo} (estado: {self.__estado})")

    def mostrar_info(self):
        return (f"Reserva: {self.__codigo}\n"
                f"{self.__cliente.mostrar_info()}\n"
                f"Servicio: {self.__servicio.nombre}\n"
                f"Cantidad: {self.__cantidad}\n"
                f"Estado: {self.__estado}")


# ======================================================================
# [NUEVO] PASO 1: ADMINISTRACIÓN DEL SISTEMA
# ======================================================================
class GestorSistema:
    """Administra clientes, servicios y reservas en listas internas (sin base de datos)."""

    # Errores que el sistema espera y controla
    ERRORES_CONTROLADOS = (ErrorDisponibilidad, ErrorReserva, ErrorCalculo,
                           ErrorRegistro, ErrorParametros, ValueError)

    TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo, "asesoria": AsesoriaEspecializada}

    def __init__(self):
        self.__clientes = []          # lista interna de Cliente
        self.__servicios = []         # lista interna de Servicio
        self.__reservas = []          # lista interna de Reserva
        self.__exitosas = 0           # contador de operaciones correctas
        self.__fallidas = 0           # contador de operaciones con error

    # ---------- ejecutor central: mantiene el sistema estable ----------
    def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación; si falla registra el error y devuelve None (nunca se cae)."""
        try:
            resultado = funcion(*args, **kwargs)
        except self.ERRORES_CONTROLADOS as error:         # errores esperados
            self.__fallidas += 1
            registrar_error(error)
            print(f"   ✘ {descripcion}: {error}")
            return None
        except Exception as error:                        # errores inesperados: tampoco detienen el programa
            self.__fallidas += 1
            registrar_error(error)
            print(f"   ✘ {descripcion}: error inesperado ({type(error).__name__})")
            return None
        else:                                             # solo si todo salió bien
            self.__exitosas += 1
            registrar_evento(f"{descripcion} - OK")
            print(f"   ✔ {descripcion}")
            return resultado
        finally:                                          # siempre se ejecuta
            registrar_evento(f"Fin de la operación: {descripcion}")

    # ---------- búsquedas ----------
    @staticmethod
    def _buscar(lista, codigo, nombre):
        """Busca por código/identificador; si no existe lanza ErrorRegistro."""
        for elemento in lista:
            id_elemento = elemento.identificador if hasattr(elemento, "identificador") else elemento.codigo
            if id_elemento == codigo:
                return elemento
        raise ErrorRegistro(f"{nombre} '{codigo}' no existe")

    @staticmethod
    def _existe(lista, codigo):
        """True si ya hay un elemento con ese código/identificador."""
        return any((e.identificador if hasattr(e, "identificador") else e.codigo) == codigo for e in lista)

    # ---------- clientes ----------
    def _alta_cliente(self, identificador, nombre, correo, contacto):
        if not isinstance(identificador, int) or isinstance(identificador, bool) or identificador <= 0:
            raise ValueError("El identificador del cliente debe ser un entero positivo")
        if self._existe(self.__clientes, identificador):
            raise ErrorRegistro(f"Ya existe un cliente con identificador {identificador}")
        cliente = Cliente(identificador, nombre, correo, contacto)   # valida en el constructor
        self.__clientes.append(cliente)
        return cliente

    def registrar_cliente(self, identificador, nombre, correo, contacto):
        return self._ejecutar(f"Registrar cliente {identificador} ({nombre})",
                              self._alta_cliente, identificador, nombre, correo, contacto)

    # ---------- servicios ----------
    def _alta_servicio(self, tipo, **parametros):
        clase = self.TIPOS_SERVICIO.get(tipo)
        if clase is None:
            raise ErrorRegistro(f"Tipo de servicio inexistente: '{tipo}'")
        try:
            servicio = clase(**parametros)                # puede lanzar TypeError o ValueError
        except TypeError as error:                        # faltan o sobran parámetros
            raise ErrorParametros(f"Parámetros incorrectos para el servicio '{tipo}'") from error
        if self._existe(self.__servicios, servicio.codigo):
            raise ErrorRegistro(f"Ya existe un servicio con código {servicio.codigo}")
        self.__servicios.append(servicio)
        return servicio

    def crear_servicio(self, tipo, **parametros):
        return self._ejecutar(f"Crear servicio tipo '{tipo}'", self._alta_servicio, tipo, **parametros)

    # ---------- reservas ----------
    def _alta_reserva(self, codigo, id_cliente, codigo_servicio, cantidad):
        if self._existe(self.__reservas, codigo):
            raise ErrorRegistro(f"Ya existe una reserva con código {codigo}")
        cliente = self._buscar(self.__clientes, id_cliente, "Cliente")
        servicio = self._buscar(self.__servicios, codigo_servicio, "Servicio")
        reserva = Reserva(codigo, cliente, servicio, cantidad)       # valida en el constructor
        self.__reservas.append(reserva)
        return reserva

    def crear_reserva(self, codigo, id_cliente, codigo_servicio, cantidad):
        return self._ejecutar(f"Crear reserva {codigo} (cliente {id_cliente}, servicio {codigo_servicio}, cantidad {cantidad})",
                              self._alta_reserva, codigo, id_cliente, codigo_servicio, cantidad)

    def confirmar_reserva(self, codigo):
        return self._ejecutar(f"Confirmar reserva {codigo}",
                              lambda: self._buscar(self.__reservas, codigo, "Reserva").confirmar_reserva())

    def cancelar_reserva(self, codigo):
        return self._ejecutar(f"Cancelar reserva {codigo}",
                              lambda: self._buscar(self.__reservas, codigo, "Reserva").cancelar_reserva())

    def procesar_reserva(self, codigo, descuento=None):
        return self._ejecutar(f"Procesar reserva {codigo} (descuento={descuento!r})",
                              lambda: self._buscar(self.__reservas, codigo, "Reserva").procesar(descuento=descuento))

    # ---------- reporte ----------
    def reporte(self):
        """Resumen general; cada objeto se describe a sí mismo (polimorfismo)."""
        linea = "=" * 60
        print(f"\n{linea}\nREPORTE FINAL - SOFTWARE FJ\n{linea}")
        print(f"Clientes: {len(self.__clientes)} | Servicios: {len(self.__servicios)} | "
              f"Reservas: {len(self.__reservas)}")
        print(f"Operaciones exitosas: {self.__exitosas} | Operaciones fallidas: {self.__fallidas}")
        print("\n--- CLIENTES ---")
        for c in self.__clientes:
            print(c.mostrar_info(), end="\n\n")
        print("--- SERVICIOS ---")
        for s in self.__servicios:
            print(s.mostrar_descripcion(), end="\n\n")
        print("--- RESERVAS ---")
        for r in self.__reservas:
            total = f"${r.costo_total:,.2f}" if r.costo_total is not None else "sin calcular"
            print(r.mostrar_info(), f"\nTotal: {total}", sep="", end="\n\n")


# ======================================================================
# [NUEVO] PASO 4: PRUEBAS FINALES (simulación de operaciones)
# ======================================================================
def main():
    registrar_evento("=== INICIO DE LA SIMULACIÓN ===")
    g = GestorSistema()

    print("\n--- CLIENTES ---")
    g.registrar_cliente(1, "Ana Gómez", "ana@correo.com", "3101234567")        # 1  válido
    g.registrar_cliente(2, "Carlos Ruiz", "carlos@correo.com", "3157654321")   # 2  válido
    g.registrar_cliente(3, "Luis Pérez", "luis-sin-arroba", "3001112233")      # 3  correo inválido
    g.registrar_cliente(4, "María Soto", "maria@correo.com", "31012345")       # 4  contacto inválido
    g.registrar_cliente(1, "Ana Repetida", "otra@correo.com", "3101234567")    # 5  id duplicado

    print("\n--- SERVICIOS ---")
    g.crear_servicio("sala", codigo=101, nombre="Sala Ejecutiva", tarifa_base=50000, disponible=True)       # 6  válido
    g.crear_servicio("equipo", codigo=201, nombre="Portátil Pro", tarifa_base=30000, disponible=True)       # 7  válido
    g.crear_servicio("asesoria", codigo=301, nombre="Asesoría Cloud", tarifa_base=120000, disponible=True)  # 8  válido
    g.crear_servicio("sala", codigo=102, nombre="Sala Rota", tarifa_base=-500, disponible=True)             # 9  tarifa inválida
    g.crear_servicio("sala", codigo=103, nombre="Sala Incompleta")                                          # 10 faltan parámetros
    g.crear_servicio("sala", codigo=104, nombre="Sala en Mantenimiento", tarifa_base=40000, disponible=False)  # 11 válido (no disponible)
    g.crear_servicio("hologramas", codigo=999, nombre="X", tarifa_base=1)                                   # 12 tipo inexistente

    print("\n--- RESERVAS ---")
    g.crear_reserva(1, 1, 101, 3)        # 13 válida (sala 3 h)
    g.crear_reserva(2, 2, 101, -4)       # 14 cantidad inválida
    g.crear_reserva(3, 99, 101, 2)       # 15 cliente inexistente
    g.crear_reserva(4, 2, 104, 2)        # 16 válida, pero con servicio no disponible
    g.crear_reserva(5, 2, 301, 2)        # 17 válida (asesoría 2 h)

    print("\n--- CONFIRMAR / PROCESAR / CANCELAR ---")
    g.procesar_reserva(1)                      # 18 procesar sin confirmar (no permitido)
    g.confirmar_reserva(1)                     # 19 confirmar OK
    g.confirmar_reserva(1)                     # 20 confirmar dos veces (no permitido)
    g.procesar_reserva(1, descuento="PROMO10") # 21 procesar con descuento e IVA OK
    g.procesar_reserva(1)                      # 22 procesar dos veces (no permitido)
    g.cancelar_reserva(1)                      # 23 cancelar una reserva ya procesada (no permitido)
    g.confirmar_reserva(4)                     # 24 confirmar con servicio no disponible (error encadenado)
    g.confirmar_reserva(5)                     # 25 confirmar OK
    g.procesar_reserva(5, descuento=1.5)       # 26 descuento inconsistente (error encadenado)
    g.cancelar_reserva(5)                      # 27 cancelar OK
    g.cancelar_reserva(5)                      # 28 cancelar dos veces (no permitido)

    g.reporte()

    # Demostración de los métodos sobrecargados (Sala, 3 horas, tarifa 50.000)
    sala = ReservaSala(900, "Sala de prueba", 50000, True)
    print("--- SOBRECARGA DE CÁLCULO (3 horas, tarifa $50.000) ---")
    print("Costo base                    :", sala.calcular_costo(3))
    print("Con IVA 19 %                  :", sala.calcular_costo_con_impuesto(3))
    print("Descuento 10 % (numérico)     :", sala.calcular_costo_final(3, descuento=0.10))
    print("Código PROMO10 + IVA          :", sala.calcular_costo_total(3, descuento="PROMO10"))
    registrar_evento("=== FIN DE LA SIMULACIÓN ===")


if __name__ == "__main__":
    main()

