# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import os
from PyQt4.QtXml import QDomDocument

from qgis.core import (
    QgsRasterLayer,
    QgsVectorLayer,
    QgsMapLayerRegistry
)

from .utils import change_directory


class SunlumoProject(object):

    def __init__(self, project_file):
        self.project_file = project_file
        self._parseProject(project_file)
        self.project_root = os.path.abspath(os.path.dirname(project_file))

    def _readLayers(self):
        layers = self.doc.elementsByTagName('maplayer')
        for i in xrange(layers.size()):
            yield layers.at(i)

    def _readLayouts(self):
        layouts = self.doc.elementsByTagName('Composer')
        for i in xrange(layouts.size()):
            yield layouts.at(i)

    def _readAttrs(self, obj):
        attrs = obj.attributes()
        for i in xrange(attrs.size()):
            yield attrs.item(i)

    def _getAttr(self, obj, attr):
        if not(obj):
            raise RuntimeError('XML Object must exist!')

        attrs = obj.attributes()
        return attrs.namedItem(attr).toAttr()

    def _parseProject(self, project_file):
        with open(project_file, 'rb') as project_data:
            self.doc = QDomDocument()
            validity = self.doc.setContent(project_data.read())

            # check validity of the QGIS Project XML file
            if not(validity[0]):
                raise RuntimeError(validity[1])

    def parseLayers(self):
        loaded_layers = []

        with change_directory(self.project_root):
            # remove all layers from the map registry
            QgsMapLayerRegistry.instance().removeAllMapLayers()
            for layer in self._readLayers():
                layer_type = self._getAttr(layer, 'type').value()
                if layer_type == 'vector':
                    qgsLayer = QgsVectorLayer()
                elif layer_type == 'raster':
                    qgsLayer = QgsRasterLayer()

                # read layer from XML
                qgsLayer.readLayerXML(layer.toElement())

                # add layer to the QgsMapLayerRegistry
                if qgsLayer.isValid():
                    QgsMapLayerRegistry.instance().addMapLayer(qgsLayer)
                    # add layer to the internal layer registry
                    loaded_layers.append(qgsLayer.id())
                    LOG.debug('Loaded layer: %s', qgsLayer.id())
            return loaded_layers

    def parseLayouts(self):
        available_layouts = []
        with change_directory(self.project_root):
            for layout in self._readLayouts():
                available_layouts.append(
                    self._getAttr(layout, 'title').value()
                )
        return available_layouts

    def getLayoutbyName(self, name):
        for layout in self._readLayouts():
            if self._getAttr(layout, 'title').value() == name:
                return layout
        else:
            return None