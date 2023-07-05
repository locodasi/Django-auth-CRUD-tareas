from django.contrib.auth.models import User
import re

def validarUsuario(u:User):
    
    if validarUsername(u.username) and validarPassword(u):
        return True
    else:
        return False
    
def validarUsername(username):

    if len(username) == 0 or len(username) > 150 or username == None:    
        return False
    
    p = r"[a-zA-Z0-9.+-_@]+"
    
    if not re.match(p,username):
        return False
    
    return True
    
def validarPassword(u:User):
    if u.username == u.password:
        return False
    
    if len(u.password) < 8:
        return False
    
    if u.password.isnumeric():
        return False
    
    contrasComunes=["qwerty123","qwertyui","contraseña","password","1q2w3e4r5t"]
    
    if u.password in contrasComunes:
        return False
    
    
    return True

