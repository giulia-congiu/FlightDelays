from contextlib import nullcontext

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza = None
        self._choiceArrivo = None

    def handleAnalizza(self, e):
        cMinTxt = self._view._txtInCMin.value

        #METTI I CONTROLLI
        #1) CONTROLLO SE è VUOTO
        if cMinTxt == '':
            self._view._txtResults.controls.clear()

        #2) CONTROLLO SE è UN INT

        #3) CONTROLLO CHE SIA UNO 0 O UN NEGATIVO

        #4) CREO GRAFO
        self._model.buildGraph(cMinTxt)


    '''caso in cui posso riempire il DRopdown solo una volta che ho creato il grafo
    perchè ho filtrato i nodi. '''
    def _fillDropdown(self, nodes):
        pass

    '''mi serve anche un metodo che mi prenda i nodi del grafo'''
    def _getAllNodes(self):
        pass

    def _choicePartenza(self,e ):
        pass

    def _choiceArrivo(self,e ):
        pass

    def handleConnessi(self, e):
        pass

    def handleCerca(self, e):
        pass
