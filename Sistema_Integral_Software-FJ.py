
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
# Clase AdministradorSistema
class AdministradorSistema:

    def _init_(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    # Registrar clientes
    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise ValueError("Debe ingresar un cliente válido")

        for registrado in self.__clientes:
            if registrado.identificador == cliente.identificador:
                raise ValueError("Ya existe un cliente con ese identificador")

        self.__clientes.append(cliente)
        return "Cliente registrado correctamente"

    # Registrar servicios
    def registrar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise ValueError("Debe ingresar un servicio válido")

        for registrado in self.__servicios:
            if registrado.codigo == servicio.codigo:
                raise ValueError("Ya existe un servicio con ese código")

        self.__servicios.append(servicio)
        return "Servicio registrado correctamente"

    # Registrar reservas
    def registrar_reserva(self, reserva):

        if not isinstance(reserva, Reserva):
            raise ValueError("Debe ingresar una reserva válida")

        # Evitar códigos de reserva repetidos
        for registrada in self.__reservas:
            if registrada.codigo == reserva.codigo:
                raise ErrorReserva("Ya existe una reserva con ese código")

        # Verificar que el cliente esté registrado
        if not any(cliente is reserva.cliente
            for cliente in self.__clientes):
            raise ErrorReserva("El cliente no está registrado en el sistema")

        # Verificar que el servicio esté registrado
        if not any(servicio is reserva.servicio
            for servicio in self.__servicios):
            raise ErrorReserva("El servicio no está registrado en el sistema")

        # Verificar el estado inicial
        if reserva.estado != "Pendiente":
            raise ErrorReserva("Solo se pueden registrar reservas pendientes")

        self.__reservas.append(reserva)
        return "Reserva registrada correctamente"

    # Confirmar reservas con impuestos y descuentos opcionales
    def confirmar_reserva(self, reserva, impuesto=0, descuento=0):

        # Verificar que la reserva exista en el sistema
        if not any(registrada is reserva
            for registrada in self.__reservas):
            raise ErrorReserva("La reserva no está registrada en el sistema")

        # Comprobar el estado
        if reserva.estado != "Pendiente":
            raise ErrorReserva("Solo se pueden confirmar reservas pendientes")

        # Evitar conflictos con otras reservas confirmadas
        for registrada in self.__reservas:
            if (registrada is not reserva
                    and registrada.servicio is reserva.servicio
                    and registrada.estado == "Confirmada"):
                raise ErrorReserva("El servicio ya tiene una reserva confirmada")

        # Confirmar aplicando impuestos y descuentos
        return reserva.confirmar_reserva(impuesto, descuento)

    # Cancelar reservas
    def cancelar_reserva(self, reserva):

        # Verificar que la reserva exista en el sistema
        if not any(registrada is reserva
            for registrada in self.__reservas):
            raise ErrorReserva("La reserva no está registrada en el sistema")

        return reserva.cancelar_reserva()

    # Mostrar clientes registrados
    def mostrar_clientes(self):

        print("\n--- Clientes Registrados ---")

        if not self.__clientes:
            print("No hay clientes registrados")
            return
        for cliente in self.__clientes:
            print(cliente.mostrar_info())
            print("--------------------")

    # Mostrar servicios registrados
    def mostrar_servicios(self):

        print("\n---Servicios Registrados---")

        if not self.__servicios:
            print("No hay servicios registrados")
            return
        for servicio in self.__servicios:
            print(servicio.mostrar_descripcion())
            print("--------------------")

    # Mostrar reservas registradas
    def mostrar_reservas(self):

        print("\n--- Reservas Registradas ---")

        if not self.__reservas:
            print("No hay reservas registradas")
            return
        for reserva in self.__reservas:
            print(reserva.mostrar_info())
            print("--------------------")
    
