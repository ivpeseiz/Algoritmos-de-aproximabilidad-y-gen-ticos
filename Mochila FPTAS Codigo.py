
def mochila_dinamica(valores, pesos, peso, valores_originales):
    
    n = len(valores)
    v_max = int(sum(valores))
    INF = int(sum(pesos)) + 1
    mochila = [[0] + ([INF] * v_max) for _ in range(n+1)]
    #print(mochila)
    for i in range(1, n + 1):
        for v in range (1, v_max + 1):
            if valores[i - 1] <= v:
                mochila[i][v] = min(mochila[i - 1][v], mochila[i - 1][v - valores[i - 1]] + pesos[i - 1])
            else:
                mochila[i][v] = mochila[i - 1][v]
                
    
    mejor = 0
    for v in range(v_max + 1):
        if mochila[n][v] <= peso:
            mejor = v
    
    v = mejor
    seleccionados = []
    for i in range(n, 0, -1):
        if v >= valores[i - 1] and mochila[i][v] == (mochila[i - 1][v - valores[i - 1]] + pesos[i - 1]):
            seleccionados.append(i - 1)
            v -= valores[i - 1]
    
    # Calculamos el valor real (sin escalado) de la solución aproximada que nos devuelve el algoritmo
    mejor_original = 0
    for i in seleccionados:
        mejor_original += valores_originales[i]
    
    return seleccionados, mejor_original


def mochila_fptas(valores, pesos, peso, epsilon):
    
    p = max(valores)
    n = len(valores)
    k = max((epsilon * p) / n, 1)
    #print(k)
    valoress = valores[:]
    for i in range(n):
        valoress[i] = int(valoress[i]/k)
        #print(valores[i])
        
    
    return mochila_dinamica(valoress, pesos, peso, valores)



