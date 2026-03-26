def valodar_campos(*campos):
    
    def decorador(funcion):
        
        def wrapper(self, *args, **kwargs):
            
            for campo in campos:
                if campo not in None or campo == "":
                    raise ValueError(f"Falta el campo: {campo}")
            
            return funcion(self,*args, **kwargs)
        
        return wrapper
    
    return decorador