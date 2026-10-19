from collections import deque

cola = deque()

def agregar(dato):
    cola.append(dato)

def show():
    return cola

def delete():
    if len(cola) == 0:
        return "La cola se encuentra vacía"
    cola.popleft()

print (delete())

agregar("ciente 1")
agregar("ciente 2")

print (delete())

print(show())