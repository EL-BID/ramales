from osgeo import ogr
from qgis.gui import QgisInterface
from qgis.core import QgsProject
from qgis.core import QgsVectorLayer
import shutil
import os
from ...helpers.utils import Utils
import re
import json


def replace_resume_frame_ids(a3_qpt_file, a2_qpt_file,
                             resume_frame_id_replace, resume_frame_id,
                             blocks_layer_id_replace, blocks_layer_id):
    if resume_frame_id is None or blocks_layer_id is None:
        raise ValueError('Resume frame or blocks layer id not found')

    for f in (a3_qpt_file, a2_qpt_file):
        with open(f, 'r') as file:
            text = file.read()
        text_edited = (text.replace(blocks_layer_id_replace,
                                    blocks_layer_id)
                       .replace(resume_frame_id_replace,
                                resume_frame_id))
        with open(f, 'w') as file:
            file.write(text_edited)


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
    qgis_path = rf'{project_path}/{project_name}.qgz'

    # Copy the geopackage to the new file
    shutil.copytree(path_in, path_out, dirs_exist_ok=True)
    conn = ogr.Open(path_out_file)

    # Now create another geopackage, with all the layers from the list
    utils = Utils()
    iface.newProject()
    project = QgsProject.instance()
    group = project.layerTreeRoot().addGroup(utils.translate('SaniHUB Ramales'))
    root = project.layerTreeRoot()
    plugin_dir = utils.get_plugin_dir()
    localizations_file = os.path.join(plugin_dir, 'resources', 'localizations', f'{local}.json')
    localizations = json.load(open(localizations_file))

    # resume frame vars
    resume_frame = localizations['layers']['resume_frame']
    blocks = localizations['layers']['blocks']

    a2_qpt_file = os.path.join(path_out, 'saniHUB_Ramales_padraoA2.qpt')
    a3_qpt_file = os.path.join(path_out, 'saniHUB_Ramales_padraoA3.qpt')

    resume_frame_id_replace = '<<RESUME_FRAME_ID>>'
    blocks_layer_id_replace = '<<BLOCKS_ID>>'

    resume_frame_id, blocks_layer_id = None, None
    for i, layer_info in enumerate(conn):
        layer_name = layer_info.GetName()
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
            if layer_name == resume_frame:
                node.setItemVisibilityChecked(True)
                resume_frame_id = layer.id()
            elif layer_name == blocks:
                node.setItemVisibilityChecked(True)
                blocks_layer_id = layer.id()
            else:
                node.setExpanded(True)
                node.setExpanded(False)

    replace_resume_frame_ids(a3_qpt_file, a2_qpt_file,
                             resume_frame_id_replace, resume_frame_id,
                             blocks_layer_id_replace, blocks_layer_id)
    project.write(qgis_path)





