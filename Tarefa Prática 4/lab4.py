# Aline Freire de Rezende - 116110571

# Scene description:
# On a starry night, the Powerpuff Cows are fighting the evil Mr. Floatie Duck.
# Buttercup attempts to poke him with her horns to stop him from dominating Barnsville.

import math
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

# para poder carregar uma malha .obj:
loadPrcFileData("","load-file-type p3assimp")

# deativar caching (para que o panda3D não use dados "velhos"):
cache = BamCache.get_global_ptr()
cache.set_active(False)


class MeuApp(ShowBase):
    def __init__(self):
        '''Abre a janela, cria um gráfo de cena e prepara tudo que é preciso
        para renderizar essa cena na janela. Define a luz da cena, chama um
        método que carrega malhas em formato .obj e mapea texturas nelas. Chama 
        também um método que define a câmera e o movimento/setting dela.'''
        ShowBase.__init__(self)
        self.carregarModelos()

        # definir luz e sombra:
        alight = AmbientLight('Ambient')
        alight.setColor((0.4, 0.4, 0.4, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
        
        plight = PointLight('plight')
        plight.setColor((0.6, 0.6, 0.6, 1))
        plight.setShadowCaster(True, 2048, 2048)
        self.render.setShaderAuto()
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(2, 6, 3)
        self.render.setLight(plnp)
    
        # desativar trackball controle de camera:
        base.disableMouse()
        # chamar o método dollyZoomTask cada frame:
        self.taskMgr.add(self.dollyZoomTask, "DollyZoomTask")


        
    ##========== Método que carrega as malhas ========== 
    def carregarModelos(self):
        '''Carrega malhas em formato .obj e mapea texturas nelas. Especifica
        a posição, escalonamento e a orientação dos modelos. Coloca os modelos
        no grafo de cena usando o método reparentTo.'''

        self.fundo = self.loader.loadModel("esquina_tex.obj")
        tex = loader.loadTexture('esquina.png')
        self.fundo.setTexture(tex,1)
        self.fundo.reparentTo(self.render) # fazendo a malha visível

        # villain
        # bob the evil floatie duck
        self.bob = self.loader.loadModel("bob190k_tex.obj")
        tex = loader.loadTexture('bob_diffuse.png')
        self.bob.setTexture(tex,1)
        self.bob.setScale(3, 3, 4) # escalonamento X, Y, Z 
        self.bob.setHpr(90,0,0) # rotacao em volta de Z, X, Y
        self.bob.setPos(4,-3,0) # posicao (X,Y,Z)
        self.bob.reparentTo(self.render)


        # powerpuff cows
        #blossom
        self.spot3 = self.loader.loadModel('spot190k_tex.obj')        
        tex = loader.loadTexture('spot_red.png')
        self.spot3.setTexture(tex,1)
        self.spot3.setHpr(-120,0,0) # rotacao em volta de Z, X, Y
        self.spot3.setScale(1, 1, 1)
        self.spot3.setPos(-1,-2,0)
        self.spot3.reparentTo(self.render)
   
        # bubbles
        self.spot1 = self.loader.loadModel("spot190k_tex.obj")
        tex = loader.loadTexture('spot_blue.png')
        self.spot1.setTexture(tex,1)
        self.spot1.setScale(1, 1, 1)
        self.spot1.setHpr(-60,10,0) # rotacao em volta de Z, X, Y 
        self.spot1.setPos(-2,-5.5,0.15) 
        self.spot1.reparentTo(self.render)

        # buttercup
        self.spot2 = self.loader.loadModel('spot190k_tex.obj')
        tex = loader.loadTexture('spot_green.png')
        self.spot2.setTexture(tex,1)
        self.spot2.setHpr(-90,-32,0) # rotacao em volta de Z, X, Y
        self.spot2.setScale(1, 1, 1)
        self.spot2.setPos(0.6,-3,1)
        self.spot2.reparentTo(self.render)
        

    ##========== Método que define o movimento de camera ========== 
    def dollyZoomTask(self, tarefa):
        '''Imita a técnica de "dolly zoom". O método aumenta o ângulo de
        visão (FOV) de uma câmera enquanto se aproxima com a câmera a um
        ponto da cena, e vice versa: diminui FOV enquanto se afasta de um
        ponto da cena. O método muda o FOV da câmera por ângulo 30 graus
        cada 3 segundos.
        
        O objetivo do movimento é focar no golpe de chifres da vaquinha verde
        no pato-boia do mau, onde ela tenta derrotá-lo na presença de suas 
        companheiras. A velocidade do zoom tem o objetivo de enfatizar o 
        sucesso do golpe.
        '''
        largura = 4
        #tarefa.time retorna o tempo que se passou em segundos, a funcao
        # math.cos é usada para criar um movimento periódico
        FOV =  40 + 33.0*math.cos(math.pi*tarefa.time/1.3)
        distance = largura/(2*math.tan(0.5*FOV/180*math.pi))        
        self.camera.lookAt(1.7,-1,2)
        self.camera.setPos(2, distance+1, 2)
        base.camLens.setFov(FOV)
        return tarefa.cont


aula4 = MeuApp()
# última linha: metódo run renderiza a janela e trata as background tarefas:
aula4.run()
