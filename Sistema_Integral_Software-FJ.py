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
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if "@" not in correo or "." not in correo:
            raise ValueError("El correo no es válido")
        if not contacto.isdigit() or len(contacto) != 10:
            raise ValueError("El contacto debe tener 10 dígitos")
        self.__nombre = nombre
        self.__correo = correo
        self.__contacto = contacto

    def mostrar_info(self):
        return (f"Cliente: {self.__nombre}\n"
                f"Correo: {self.__correo}\n"
                f"Contacto: {self.__contacto}")
