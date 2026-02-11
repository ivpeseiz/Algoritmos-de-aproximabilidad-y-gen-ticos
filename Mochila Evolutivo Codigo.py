import random
CAPACIDAD_MOCHILA = 995
POBLACION_INICIAL = 500
GENERACIONES = 15
PROB_MUTACION = 0.01
PROB_CRUCE = 0.9

NUM_TOR = 15
N = len(items)
ELITISMO = 10
DENSIDAD_INICIAL = 0.1
SEMILLAS_HEURISTICAS = 2



###_______________________________________ FUNCION FITNESS ______________________________________________###

def fitness(individuo):
    valor_total = 0
    peso_total = 0
    for i, gen in enumerate(individuo):
        if gen:   # si gen es 1
            v, w = items[i]
            valor_total += v
            peso_total += w

    if peso_total <= CAPACIDAD_MOCHILA:
        return valor_total
    else:
        # Penalización suave (parece que es mejor que devolver 0)
        #return valor_total * (CAPACIDAD_MOCHILA / peso_total)
        # Penalizacion total (si rompe la mochila devuelve 0)
        return 0
    
###_______________________________________ FUNCION CREAR INDIVIDUO ______________________________________________###

def crear_individuo():
    individuo = [0] * N
    peso = 0

    # Si caben en la mochila voy metiedno items aleatoriamente
    for i in random.sample(range(N), N):  
        if random.random() < DENSIDAD_INICIAL:  # densidad de dispersion de los 1's en los individuos iniciales (siempre que quepan en la mochila)
            if peso + items[i][1] <= CAPACIDAD_MOCHILA:
                individuo[i] = 1
                peso += items[i][1]

    return individuo



###_______________________________________ FUNCION DE SELECCION (POR TORNEO) ______________________________________________###

def seleccion(poblacion):
    candidatos = random.sample(poblacion, NUM_TOR)
    return max(candidatos, key=lambda x: x[1])[0][:]  # devuelve el individuo, porque la poblacion era una lista de tuplas (individuo, fitness(individuo))



###_______________________________________ FUNCION DE CRUCE (UNIFORME) ______________________________________________###

def cruce(padre1, padre2):
    if random.random() > PROB_CRUCE:
        return padre1[:], padre2[:]  # sin cruce

    hijo1 = padre1[:]  # Hacemos una copia completa de los padres
    hijo2 = padre2[:]

    for i in range(N):
        if random.random() < 0.5:   # Mezclamos aleatoriamente
            hijo1[i], hijo2[i] = hijo2[i], hijo1[i]

    return hijo1, hijo2



###_______________________________________ FUNCION DE MUTACION (FACTIBLE) ______________________________________________###

def mutacion(individuo):
    peso_total = sum(items[i][1] for i in range(N) if individuo[i] == 1)

    for i in range(N):     # ¿Deberia hacer un random.shuffle(range(N)) para evitar que sea menos probable coger los primeros objetos de la mochila?
        if random.random() < PROB_MUTACION:

            if individuo[i] == 1:
                # Siempre es seguro sacar un objeto de la mochila (no pone en peligro la factibilidad)
                individuo[i] = 0
                peso_total -= items[i][1]

            else:
                # Solo metemos el objeto en la mochila si cabe
                if peso_total + items[i][1] <= CAPACIDAD_MOCHILA:
                    individuo[i] = 1
                    peso_total += items[i][1]

    return individuo


###_______________________________________ FUNCION DE ARREGLAR ______________________________________________###

def arreglar(individuo):
    peso_total = sum(items[i][1] for i in range(N) if individuo[i] == 1)
    if peso_total <= CAPACIDAD_MOCHILA:
        return individuo

    # Si pesa demasiado, eliminamos ítems de menor ratio valor/peso
    indices = [i for i in range(N) if individuo[i] == 1]
    indices.sort(key=lambda i: items[i][0] / items[i][1])

    for i in indices:
        if peso_total <= CAPACIDAD_MOCHILA:
            break
        individuo[i] = 0
        peso_total -= items[i][1]

    return individuo




###_______________________________________ SEMILLAS HEURISTICAS ______________________________________________###


def semilla_por_ratio():
    individuo = [0] * N
    peso = 0

    orden = sorted(range(N), key=lambda i: items[i][0]/items[i][1], reverse=True)

    for i in orden:
        v, w = items[i]
        if peso + w <= CAPACIDAD_MOCHILA:
            individuo[i] = 1
            peso += w

    return individuo


###_______________________________________ MOCHILA-APX ______________________________________________###

def mochila_apx():
    objetos = []
    i = 0
    for valor, peso in items:
        objetos.append((valor/peso, valor, peso, i))
        i += 1
    objetos_ordenados = objetos[:]
    objetos_ordenados.sort(reverse = True)
    
    w, v, j, seleccionados, primero, k = 0, 0, 0, [], True, N-1
    
    for ratio, valor, peso, indice in objetos_ordenados:
        if w + peso <= CAPACIDAD_MOCHILA:
            w += peso
            v += valor
            seleccionados.append(indice)
        else:
            if primero:
                k = j
                primero = False
        j += 1
    ratio, valor, peso, indice = objetos[k+1]
    if k != N-1 and (valor > v and peso <= CAPACIDAD_MOCHILA):
        v = valor
        seleccionados = [k+1]
    
    sol_apx = [0]*N
    for indice in seleccionados:
        sol_apx[indice] = 1
    return sol_apx
    

###_______________________________________ ALGORITMO GENETICO ______________________________________________###

def algoritmo_genetico():
    poblacion= []
    
    
    # He metido la funcion crear poblacion en algoritmo genetico porque es mas comodo para introducir semillas heuristicas/APX
    # Para evitar evaluar varias veces cada individuo, la poblacion sera una lista de tuplas (individuo, fitness(individuo))
    #poblacion.append((mochila_apx(), None))
    
    #for _ in range(SEMILLAS_HEURISTICAS):
        #poblacion.append((semilla_por_ratio(), None))
        
    

    while len(poblacion) < POBLACION_INICIAL:
        poblacion.append((crear_individuo(), None))

    poblacion = [(individuo, fitness(individuo)) for individuo, _ in poblacion]
    
    
    for gen in range(GENERACIONES): # Bucle de evolución

        # Ordenamos por fitness de manera decreciente
        poblacion.sort(key=lambda x: x[1], reverse=True)

        nueva_poblacion = []

        # Elitismo
        for i in range(ELITISMO):   # Aqui decidimos cuántos de los mejores individuos se mantendrán en cada generacion
            nueva_poblacion.append((poblacion[i][0][:], poblacion[i][1]))

        # Reproducción
        while len(nueva_poblacion) < POBLACION_INICIAL:
            padre1 = seleccion(poblacion)
            padre2 = seleccion(poblacion)

            hijo1, hijo2 = cruce(padre1, padre2)

            # Arreglamos después del cruce
            hijo1 = arreglar(hijo1)
            hijo2 = arreglar(hijo2)

            # Mutación factible (no requiere arreglar otra vez)
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)

            nueva_poblacion.append((hijo1, fitness(hijo1)))
            if len(nueva_poblacion) < POBLACION_INICIAL:
                nueva_poblacion.append((hijo2, fitness(hijo2)))

        poblacion = nueva_poblacion
        print(f"Generación {gen+1}: Mejor valor = {poblacion[0][1]}")

    poblacion.sort(key=lambda x: x[1], reverse=True)
    return poblacion[0]


###_______________________________________ EJECUCION ______________________________________________###

t0 = time()
mejor_individuo, mejor_valor = algoritmo_genetico()
t1 = time()
print(f"Mejor individuo: {mejor_individuo}")
print(f"Valo total: {mejor_valor}")
print(f"Peso total: {sum(items[i][1] for i in range(len(items)) if mejor_individuo[i] == 1)}")
print(f"Tiempo total: {t1-t0}")