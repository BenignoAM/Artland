from werkzeug.security import check_password_hash
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, id, nombre, correo, clave, perfil, fechanac, fechareg, fotou) -> None:
        self.id       = id
        self.nombre   = nombre
        self.correo   = correo
        self.clave    = clave
        self.perfil   = perfil
        self.fechanac = fechanac
        self.fechareg = fechareg
        self.fotou    = fotou

    @classmethod
    def validarClave(self, claveCifrada, clave):
        return check_password_hash(claveCifrada, clave)