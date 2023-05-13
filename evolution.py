from httpx import AsyncClient
from asyncio import run, gather
from typing import Optional
from rich import print

pokemons = [
    "bulbasaur",
    "charmander",
    "squirtle",
    "caterpie",
    "weedle",
    "pidgey",
    "rattata",
    "spearow",
    "ekans",
    "pikachu",
    "sandshrew",
    "clefairy",
    "vulpix",
    "jigglypuff",
    "zubat",
]


async def get_pokemon_id(poke: str) -> int:
    async with AsyncClient(base_url="https://pokeapi.co/api/v2") as client:
        response = await client.get(f"/pokemon/{poke}")

        return response.json().get("id")


async def get_evolution_chain_url(poke_id: int) -> str:
    async with AsyncClient(base_url="https://pokeapi.co/api/v2") as client:
        response = await client.get(f"/pokemon-species/{poke_id}")
        url = response.json().get("evolution_chain").get("url")

        return url


async def get_evolution_name(url: str) -> Optional[str]:
    async with AsyncClient(base_url="https://pokeapi.co/api/v2") as client:
        response = await client.get(url)
        evolves_to = response.json().get("chain").get("evolves_to")
        return (
            None if len(evolves_to) == 0 else evolves_to[0].get("species").get("name")
        )


async def get_pokemon_evolution_name(poke: str) -> None:
    id_ = await get_pokemon_id(poke)
    evo_chain = await get_evolution_chain_url(id_)
    print(await get_evolution_name(evo_chain))


async def main():
    result = gather(*[get_pokemon_evolution_name(poke) for poke in pokemons])

    await result


if __name__ == "__main__":
    run(main())
