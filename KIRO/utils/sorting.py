def binary_search(
    array:list,
    value,
    return_index_if_not_in_list:bool=False,
    )->int:
    """Recherche dichotomique d'un élément dans un tableau trié.
    Renvoie -1 si la valeur n'est pas n'est pas dans le tableau.

    Args:
        array (list): Tableau trié.
        value (any): Valeur à rechercher.
        return_index (bool) : Si mis à False, la fonction renvoie -1 si la 
            valeur n'est pas trouvée dans la liste. Sinon, la fonction renvoie 
            l'indice où il faudrait insérer la valeur pour que 'array' reste
            trié.

    Returns:
        int: Index de la valeur si elle est dans le tableau, -1 sinon.
    """
    
    # On commence par vérifier que le tableau n'est pas vide
    if len(array) == 0:
        # Valeur non trouvée, on 0 ou -1 en fonction de si l'utilisateur 
        #   cherche un indice d'insertion
        if return_index_if_not_in_list : return  0
        else                           : return -1

    # Ensuite, on vérifie que la valeur est du bon type
    # NOTE : On est surs à ce stade qu'il y a au moins un élément
    elif not isinstance(value, type(array[0])):
        return -1
   
    # --- Dans les autres cas, nous faisons notre algo de tri
    # On définit les bornes de la recherche de façon récursive. On regarde si
    # la valeur est plus petite ou plus grande que le milieu, et on change la
    # borne correspondante en fonction du résultat.
    # Dans le cas où on tombe sur la bonne valeur, on revoie le résultat.
    
    # CAS GENERAL : On fait le tri
    
    left =  0
    right = len(array)-1
    while left <= right:
        middle = (left + right) // 2
        if array[middle] == value:
            return middle
        elif array[middle] < value:
            left = middle+1
        else:
            right = middle-1
    
    # --- Dans le cas où on ne trouve pas la valeur, on renvoie en fonction 
    # de ce qui est choisi l'indice pour une insertion triée, ou -1.
    if return_index_if_not_in_list : 
        # NOTE : left et right+1 sont forcément égaux, on peut donc renvoyer 
        #       left ou right+1 
        return left
    else:
        return -1

def insert_in_sorted_array(
    array:list,
    value,
    )->list:
    """Insère dans une liste déjà triée une valeur.

    Args:
        array (list): Liste triée
        value (any): Valeur à insérer
    """
    indice_d_insertion = binary_search(
        array=array,
        value=value,
        return_index_if_not_in_list=True,
    )
        
    array.insert(indice_d_insertion,value)
    return array
    