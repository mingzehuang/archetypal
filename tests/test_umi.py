import collections
import io
import os

import pytest
from archetypal import copy_file, UmiTemplate, settings


@pytest.mark.xfail(raises=AssertionError)
def test_template_to_template(config):
    """load the json into UmiTemplate object, then convert bacl to json and
    compare"""
    import json
    file = './input_data/umi_samples/BostonTemplateLibrary_2.json'
    if file:
        with open(file, 'r') as f:
            a = json.load(f)
            data_dict = collections.OrderedDict({'GasMaterials': [],
                                                 'GlazingMaterials': [],
                                                 'OpaqueMaterials': [],
                                                 'OpaqueConstructions': [],
                                                 'WindowConstructions': [],
                                                 'StructureDefinitions': [],
                                                 'DaySchedules': [],
                                                 'WeekSchedules': [],
                                                 'YearSchedules': [],
                                                 'DomesticHotWaterSettings': [],
                                                 'VentilationSettings': [],
                                                 'ZoneConditionings': [],
                                                 'ZoneConstructionSets': [],
                                                 'ZoneLoads': [],
                                                 'Zones': [],
                                                 'WindowSettings': [],
                                                 'BuildingTemplates': []})
            data_dict.update(a)

        # Create data folder if does not exist
        if not os.path.isdir(os.path.relpath(settings.data_folder)):
            os.mkdir(os.path.relpath(settings.data_folder))

        path = os.path.join(os.path.relpath(settings.data_folder), 'a.json')
        with io.open(path, 'w+', encoding='utf-8') as path_or_buf:
            a = json.dumps(data_dict, indent=2)
            path_or_buf.write(a)
        with open(path, 'r') as f:
            a = json.load(f)
    b = UmiTemplate.from_json(file).to_json(
        os.path.join(os.path.relpath(settings.data_folder),
                     'b.json'))
    b = json.loads(b)
    assert a == b


def test_umi_routine(config):
    idf_source = [
        './input_data/necb/NECB 2011-FullServiceRestaurant-NECB HDD '
        'Method-CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw.idf',
        './input_data/necb/NECB 2011-LargeHotel-NECB HDD '
        'Method-CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw.idf',
        './input_data/umi_samples/VentilationSimpleTest.idf'
    ]
    idf = copy_file(idf_source)
    wf = './input_data/CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw'
    a = UmiTemplate.from_idf(idf, wf, load=True, run_eplus_kwargs=dict(
        prep_outputs=True), name='Mixed_Files')
    print(a.BuildingTemplates)

    print(a.to_json())


def test_umi_samples(config):
    idf_source = ['./input_data/umi_samples/B_Off_0.idf',
                  './input_data/umi_samples/B_Ret_0.idf',
                  './input_data/umi_samples/B_Res_0_Masonry.idf',
                  './input_data/umi_samples/B_Res_0_WoodFrame.idf']
    idf_source = copy_file(idf_source)
    # run_eplus(idf_source, weather_file='./input_data/CAN_PQ_Montreal.Intl.AP'
    #                                    '.716270_CWEC.epw')
    wf = './input_data/CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw'
    a = UmiTemplate.from_idf(idf_source, wf, load=True, run_eplus_kwargs=dict(
        prep_outputs=True, expandobjects=True), name='Umi_Samples')
    print(a.BuildingTemplates)

    print(a.to_json())
