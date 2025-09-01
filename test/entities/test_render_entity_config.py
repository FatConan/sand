from pytest import test_data
from sand.entities import RenderEntity

def test_render_entity():
    re = RenderEntity(test_data["SITE"], test_data["SOURCE"], test_data["TARGET"])
    assert re.source == test_data["SOURCE"]
    assert re.target == test_data["TARGET"]
    assert re.site == test_data["SITE"]

def test_render_entity_validation():
    re = RenderEntity(test_data["SITE"], test_data["SOURCE"], test_data["TARGET"])
    assert re.validate() == True

    # Specify a Non target
    re = RenderEntity(test_data["SITE"], test_data["SOURCE"], None)
    assert re.validate() == False

    re = RenderEntity(test_data["SITE"], test_data["SOURCE"], None)
    assert re.validate() == False