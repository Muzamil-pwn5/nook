from app.llm.tool_schemas import get_tool_schemas


def test_llm_tool_schemas():
    tools = get_tool_schemas()

    assert len(tools) == 3

    tool_names = {
        tool["name"]
        for tool in tools
    }

    assert tool_names == {
        "search_products",
        "check_inventory",
        "create_order",
    }

    for tool in tools:
        assert tool["type"] == "function"
        assert tool["strict"] is True
        assert tool["parameters"]["additionalProperties"] is False