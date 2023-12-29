from osgeo import ogr
from qgis.gui import QgisInterface
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
import shutil
import os
from ...helpers.utils import Utils
import re


def generate_project(local: str,
                     srid_type: str,
                     srid: str,
                     project_name: str,
                     project_path: str,
                     iface: QgisInterface):
    """Gets a geopackage, in one of the available locales, and creates a QGIS project in the specified path
       with the same data of the geopackage but with the specified srid

       Args:
          local: The language of the geopackage
          srid_type (str): The type of the srid, like EPSG
          srid (int): The srid of the new geopackage
          project_name (str): The name of the project
          project_path (str): The path to the project
          iface: The QgisInterface

       Raises:
              ValueError: If the local is not pt_BR or es_ES
              OSError: If the user has no permission (errno.EACCES), or no space left on device (errno.ENOSPC)
              FileNotFoundError: If the project_path is not a valid path

    """
    plugin_dir = os.path.dirname(__file__)
    plugin_dir = plugin_dir.replace('core' + os.sep + 'project_creation', 'resources')

    # Gets the available locales
    locales_re = 'sanihubramales_(.*)\\.gpkg'
    locales = []
    for f in os.scandir(os.path.join(plugin_dir, 'geopackages', local)):
        name = f.name
        if re.search(locales_re, name) is not None:
            # if re.match(locales_re, name):
            locale = re.search(locales_re, name).group(1)
            locales.append(locale)

    # Checks if local asked exist in the available locales
    if local not in locales:
        raise ValueError(f'Invalid local value, got {local} but expected {locales}')

    # path_in = os.path.join(plugin_dir, 'geopackages', local,'sanihubramales_' + local + '.gpkg')
    path_in = os.path.join(plugin_dir, 'geopackages', local)

    # We will not allow the user to create a project in the root directory of the plugin.
    if not os.path.isabs(project_path):
        raise FileNotFoundError(f'Invalid path, got {project_path}, expected an absolute path')

    # Creates the new directory, if it doesn't exist
    os.makedirs(project_path, exist_ok=True)

    path_out_file = rf'{project_path}/sanihubramales_{local}.gpkg'
    path_out = rf'{project_path}'
    qgis_path = rf'{project_path}/{project_name}.qgs'

    # Copy the geopackage to the new file
    shutil.copytree(path_in, path_out, dirs_exist_ok=True)
    conn = ogr.Open(path_out_file)

    # Now create another geopackage, with all the layers from the list
    utils = Utils()
    iface.newProject()
    project = QgsProject.instance()
    group = project.layerTreeRoot().addGroup(utils.tr('SaniHUB Ramales'))
    root = project.layerTreeRoot()
    for i, layer_info in enumerate(conn):
        layer = QgsVectorLayer(path_out_file + "|layername=" + layer_info.GetName(), layer_info.GetName(), 'ogr')
        crs = layer.crs()
        crs.createFromOgcWmsCrs(f"{srid_type}:{srid}")
        layer.setCrs(crs)
        # add layer to group
        if layer.isValid() and layer.featureCount() < 1:
            project.addMapLayer(layer, False)
            group.addLayer(layer)

            # Close the layers
            node = root.findLayer(layer.id())
            node.setExpanded(True)
            node.setExpanded(False)

    project.write(qgis_path)





