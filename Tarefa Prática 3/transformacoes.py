# Aline Freire de Rezende
# DRE: 116110571

import numpy as np
import math

def lerMalha(nome):
    """Recebe uma string com o nome do arquivo .obj a ser lido. Retorna um
    np.ndarray com as x,y,z coordenadas dos pontos (uma coluna é um ponto) da
    malha e uma lista de strings, onde cada elemento da lista define uma face."""
    vertices = []
    faces = []
    arquivo = open(nome, "r")
    for line in arquivo:
        if line[0] == "v":
            partes = line.split(" ")
            vertices.append([float(partes[1]), float(partes[2]),\
                             float(partes[3])])
        if line[0] == "f":
            faces.append(line)
    arquivo.close()
    pontos = np.transpose(np.array(vertices))
    return pontos, faces

    
def escreverMalha(pts, faces, nome):
    """Recebe uma nd.array com x,y,z coordenadas de todos os pontos da malha,
    uma lista com os strings representando as faces da malha e
    um nome do arquivo no qual a malha deve ser escrita (em formato .obj)."""
    novo = np.transpose(pontos)
    arquivo = open(nome, "w")
    for ponto in novo:
        arquivo.write("v ")
        for eixo in ponto:
            arquivo.write(str(eixo) + " ")
        arquivo.write("\n")
        
    for face in faces:
        arquivo.write(face)       
    arquivo.close()
    
#=================================================================
# Escreva todas as possíveis funções auxiliares dentro desse bloco


def transformacaoAfim(pts):
    """Recebe um np.ndarray com x,y,z coordenadas de pontos. A função adiciona
    a 4a coordenada para representar os pontos em coordenadas homogêneas
    e aplica uma transformação afim. O valor de retorno é um np.ndarray
    com x,y,z coordenadas dos pontos transformados."""
    # crie a matriz composta de todas as transformações em coordenadas homogêneas
    # multiplique os pontos em coordenadas homogêneas por essa matriz
    # descarte a 4a coordenada e retorna apenas as coordenadas x,y,z dos pontos

    ones = np.ones((1,len(pts[0])), int) # matriz de uma dimensão para representar coordenadas homogêneas
    pts = np.append(pts, ones, 0) # adição das coordenadas homogêneas no array de pontos

    ninety = math.pi/2 # angulo de 90°
    height = 1/(pts[1].max() - pts[1].min()) # inverso da altura do Bob
     
    roty = np.array([[math.cos(-ninety), 0, math.sin(-ninety), 0],[0, 1, 0, 0],[-math.sin(-ninety), 0, math.cos(-ninety), 0], [0, 0, 0, 1]]) # rotação antihorária de -90° no eixo y
    rotx = np.array([[1, 0, 0, 0],[math.cos(ninety), 0, -math.sin(ninety), 0],[0, math.sin(ninety), math.cos(ninety), 0], [0, 0, 0, 1]]) # rotação antihorária de 90° no eixo x
    scaling = np.array([[height, 0, 0, 0],[0, height, 0, 0],[0, 0, height, 0], [0, 0, 0, 1]]) # escalonamento de acordo com a altura de Bob
    

    transformation = scaling @ rotx @ roty #transformação sem a translação
    pts = transformation @ pts # execução da transformação atual
    newHeight = pts[2].min() # altura da origem até a base de Bob
    translation = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, -newHeight], [0, 0, 0, 1]]) # translação para sentar Bob no plano xy
    pts = translation @ pts # execução da translação

    pts = pts[:-1] # cortar a última linha, das coordenadas homogênes dos pontos
    
    return pts


#=================================================================

pontos, faces = lerMalha("bob.obj")
pontos = transformacaoAfim(pontos)
escreverMalha(pontos, faces, "bob_novo.obj")

