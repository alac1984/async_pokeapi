import pytest
from httpx import Response

from evolution import get_pokemon_id
from evolution import get_evolution_chain_url
from evolution import get_evolution_name


@pytest.mark.asyncio
async def test_get_pokemon(respx_mock):
    mock_route = respx_mock.get("https://pokeapi.co/api/v2/pokemon/pikachu")
    mock_route.return_value = Response(200, json={"id": 31})
    result = await get_pokemon_id("pikachu")

    assert mock_route.called
    assert result == 31


@pytest.mark.asyncio
async def test_get_evolution_chain(respx_mock):
    mock_route = respx_mock.get("https://pokeapi.co/api/v2/pokemon-species/31")
    mock_route.return_value = Response(
        200, json={"evolution_chain": {"url": "https://www.pokemon.com/pokemon31"}}
    )
    result = await get_evolution_chain_url(31)

    assert mock_route.called
    assert result == "https://www.pokemon.com/pokemon31"


@pytest.mark.asyncio
async def test_get_evolution_name_no_evolution(respx_mock):
    mock_route = respx_mock.get("https://pokeapi.co/api/v2/evolution-chain/72")
    mock_route.return_value = Response(200, json={"chain": {"evolves_to": []}})

    result = await get_evolution_name("https://pokeapi.co/api/v2/evolution-chain/72")

    assert mock_route.called
    assert result is None


@pytest.mark.asyncio
async def test_get_evolution_name_with_evolution(respx_mock):
    mock_route = respx_mock.get("https://pokeapi.co/api/v2/evolution-chain/72")
    mock_route.return_value = Response(
        200, json={"chain": {"evolves_to": [{"species": {"name": "wartotle"}}]}}
    )

    result = await get_evolution_name("https://pokeapi.co/api/v2/evolution-chain/72")

    assert mock_route.called
    assert result == "wartotle"
