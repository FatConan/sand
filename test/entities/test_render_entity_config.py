from pytest import test_data
from sand.entities import RenderEntity
from sand.entities.resources import LessResource, ScssResource, PlainResource
from sand.entities.pages import Page, RawContent

RENDER_ENTITY_CLASSES = [Page, RawContent, PlainResource, LessResource, ScssResource]

def test_render_entity():
    re = RenderEntity(test_data["site"], test_data["target"], test_data["source"])
    assert re.source == test_data["source"]
    assert re.target == test_data["target"]
    assert re.site == test_data["site"]

def test_render_entity_validation():
    re = RenderEntity(test_data["site"], test_data["target"], test_data["source"])
    assert re.validate() == True

    #Same check. with test data as kwargs
    re = RenderEntity(**test_data)
    assert re.validate() == True

    re = RenderEntity(test_data["site"], test_data["target"], None)
    assert re.validate() == True

    #Make sure that's consistent behaviour for all our built in render entities
    for render_class in RENDER_ENTITY_CLASSES:
        re = render_class(**test_data)
        assert re.validate() == True

    # Specify a Non target, this should be invalid for all of our renderers
    re = RenderEntity(test_data["site"], None, test_data["source"])
    assert re.validate() == False

    for render_class in RENDER_ENTITY_CLASSES:
        re = render_class(test_data["site"], None, test_data["source"])
        assert re.validate() == False

