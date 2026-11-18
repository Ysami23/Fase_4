from abc import ABC, abstractmethod

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
            raise ValueError("El nombre debe ser un texto valido")
            
        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise ValueError("El correo no es válido")
            
        if not isinstance(contacto, str):
            raise ValueError("El contacti tiene texto")    
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
                or tarifa_base <= 0):
            raise ValueError("La tarifa debe ser un número positivo")

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
        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValueError("Las horas deben ser un número positivo")
        return self.tarifa_base * cantidad

    def mostrar_descripcion(self):
        return (f"Servicio: {self.nombre}\n"
                f"Código: {self.codigo}\n"
                f"Tarifa por hora: ${self.tarifa_base}")

    def validar_disponibilidad(self):
        if not self.__disponible:
            raise ValueError("La sala no está disponible")
        return True

