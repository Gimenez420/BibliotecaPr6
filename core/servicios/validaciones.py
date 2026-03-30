def valodar_campos(*campos):
    
    def decorador(funcion):
        
        def wrapper(self, *args, **kwargs):
            
            for campo in campos:
                valor = getattr(self, campo, None)
                
                if valor is None or valor == "":
                    raise ValueError(f"Falta el campo: {campo}")
            
            return funcion(self, *args, **kwargs)
        
        return wrapper
    
    return decorador