"""
Définit un ensemble de DesignPatterns afin qu'ils soient réutilisés.
"""

class Singleton:
    """Comportement d'un Singleton.
    La classe n'est instanciée qu'une unique fois.
    
    Toute classe qui hérite de celle-ci se verra hériter de celle-ci héritera
    du comportement voulu."""
    
    # L'unique instance qui sera créée.
    __instance = None
    
    def __new__(
        cls,
        *args,
        **kwargs,
    ):
        """Fonction qui allouera l'emplacement mémoire."""
        
        # L'instance n'est créée qu'une seule fois
        if cls.__instance is None :
            cls.__instance = super(Singleton, cls).__new__(cls,*args,**kwargs)
        
        # On renvoie l'instance déjà disponible ou celle qui a été créée.
        return cls.__instance