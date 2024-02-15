import requests


def test_pokemon_type_api():
    base_url = "https://pokeapi.co/api/v2/"
    type_url = base_url + "type"

    response = requests.get(type_url)
    data = response.json()["count"]

    assert response.status_code == 200, f"Failed to get response from {type_url}"
    assert 'application/json' in response.headers['Content-Type'], f"Response from {type_url} is not in JSON format"
    assert data == 20, f"Expected 20 different Pokémon types, but got {data}"

    data2 = response.json()

    fire_type_id = None
    for result in data2['results']:
        if result['name'] == 'fire':
            fire_type_id = result['url'].split('/')[-2]
            break

    assert fire_type_id is not None, "Fire type not found in Pokémon type API response"

    fire_type_url = base_url + f"type/{fire_type_id}"
    fire_type_response = requests.get(fire_type_url)
    fire_type_data = fire_type_response.json()

    charmander_exists = False
    bulbasaur_exists = False

    for pokemon in fire_type_data['pokemon']:
        if pokemon['pokemon']['name'] == 'charmander':
            charmander_exists = True
            break

    for pokemon in fire_type_data['pokemon']:
        if pokemon['pokemon']['name'] == 'bulbasaur':
            bulbasaur_exists = True
            break

    assert charmander_exists, "Charmander is not in the JSON of the Fire Pokémon list"
    assert not bulbasaur_exists, "Bulbasaur is in the JSON of the Fire Pokémon list"

    expected_weights = {
        'charizard-gmax': 10000,
        'cinderace-gmax': 10000,
        'coalossal-gmax': 10000,
        'centiskorch-gmax': 10000,
        'groudon-primal': 9997
    }

    for pokemon in fire_type_data['pokemon']:
        pokemon_name = pokemon['pokemon']['name']
        if pokemon_name in expected_weights:
            temp_pokemon_id = pokemon['pokemon']['url'].split('/')[-2]
            temp_url = "https://pokeapi.co/api/v2/pokemon/" + temp_pokemon_id
            temp_response = requests.get(temp_url)
            data4 = temp_response.json()['weight']

            assert expected_weights[
                       pokemon_name] == data4, f"{pokemon_name} does not have the expected weight of {expected_weights[pokemon_name]}"

    print("All assertions passed successfully")
