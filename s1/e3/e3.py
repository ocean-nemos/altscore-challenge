import utils.session as s
import base64
import os
import json

# Set this to True to use cached data, False to fetch fresh data
USE_CACHED_DATA = False

class Person:

    def __init__(self, id: str, name: str, side: bool = None):
        # side = True indicates light side, dark side otherwise.
        self.id = id
        self.name = name
        self.side = side

class Planet:

    def __init__(self, id: str, name, people: list[Person] = []):
        self.id = id
        self.name = name
        self.people = people

    def ibf(self):
        light = 0
        dark = 0
        for p in self.people:
            if p.side is None:
                print(f"\nThe person {p.id} of the planet {self.name} has no side indicated yet")
                return None
            elif p.side:
                light += 1
            else:
                dark += 1
        return (light - dark)/len(self.people)

def save_to_cache(data, filename):
    """Save data to a cache file"""
    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    os.makedirs(cache_dir, exist_ok=True)
    filepath = os.path.join(cache_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_from_cache(filename):
    """Load data from a cache file if it exists"""
    cache_dir = os.path.join(os.path.dirname(__file__), "cache")
    filepath = os.path.join(cache_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def get_planets():
    # Check if we should use cached data
    if USE_CACHED_DATA:
        planets_data = load_from_cache("planets.json")
        if planets_data:
            print("\nUsing cached planets data")
            planets = {}
            for p_id, p_info in planets_data.items():
                planets[p_id] = Planet(p_id, p_info["name"])
            print(f" - Loaded {len(planets)} planets from cache")
            return planets

    endpoint = lambda page: f"https://swapi.tech/api/planets?page={page}&limit=10"

    planets: dict[str, Planet] = dict()

    # get all pages
    r0 = s.get_external(endpoint(1))
    if r0.status_code != 200:
        print(f"(code {r0.status_code}) Failed to retrieve planets:\n{r0.text}")
        exit(0)
    total_pages = r0.json().get("total_pages", 0)
    total_planets = r0.json().get("total_records", 0)

    print(f"\nStarted retrieval of planets\n")

    # init planets
    for p in range(1, total_pages+1):

        r = s.get_external(endpoint(p))
        if r.status_code != 200:
            print(f"(code {r.status_code}) Failed to retrieve planets:\n{r.text}")
            continue

        for p in r.json().get("results", []):
            planets[p["uid"]] = Planet(p["uid"], p["name"])

    # check that all planets were fecthed
    if len(planets) != total_planets:
        print(f"Warning: expected {total_planets} planets, but got {len(planets)}. Exiting ...")
        exit(0)

    print(f" - Finished retrieval of planets, added {len(planets)} planets.")
    
    # Save to cache
    planets_data = {p_id: {"name": planet.name} for p_id, planet in planets.items()}
    save_to_cache(planets_data, "planets.json")

    return planets

def add_people(planets: dict[str, Planet]):
    # Check if we should use cached data
    if USE_CACHED_DATA:
        people_data = load_from_cache("people.json")
        if people_data:
            print("\nUsing cached people data")
            added = 0
            for person_info in people_data:
                personid = person_info["id"]
                name = person_info["name"]
                planet_id = person_info["planet_id"]
                
                person = Person(personid, name)
                
                if planet_id in planets:
                    planets[planet_id].people.append(person)
                    added += 1
            
            print(f" - Loaded {added} people from cache")
            return

    endpoint_people = lambda page: f"https://swapi.tech/api/people?page={page}&limit=10"
    endpoint_person = lambda id: f"https://swapi.tech/api/people/{id}"

    # get all pages
    r0 = s.get_external(endpoint_people(1))
    if r0.status_code != 200:
        print(f"(code {r0.status_code}) Failed to retrieve planets:\n{r0.text}")
        exit(0)

    total_people = r0.json().get("total_records", 0)
    added = 0
    missing_ids = []
    
    # For caching
    people_cache = []

    print(f"\nStarted retrieval of people\n")

    # add people
    for p_id in range(1, total_people+1):
        r1 = s.get_external(endpoint_person(p_id))

        if r1.status_code != 200:
            print(f" - (code {r1.status_code}) Failed to retrieve person with id {p_id}, will try additional IDs later")
            missing_ids.append(p_id)
            continue
        
        data = r1.json()["result"]["properties"]

        name = data["name"]
        personid = data["url"].split("/")[-1]
        person = Person(personid, name)
        planet_id = data["homeworld"].split("/")[-1]

        print(f" - Adding person {name} with id {personid} from planet {planet_id}")

        # associate to its planet
        if planet_id in planets:
            planets[planet_id].people.append(person)
            added += 1
            # Add to cache data
            people_cache.append({
                "id": personid,
                "name": name,
                "planet_id": planet_id
            })
        else:
            print(f" - !! Warning: person {person.name} has no associated planet.")

    # Try checking beyond the reported total
    print("\nChecking for additional people beyond reported total...")
    extra_id = total_people + 1
    max_extra = extra_id + 5  # Try a few extra IDs
    
    while extra_id <= max_extra:
        r1 = s.get_external(endpoint_person(extra_id))
        if r1.status_code == 200:
            data = r1.json()["result"]["properties"]
            name = data["name"]
            personid = data["url"].split("/")[-1]
            person = Person(personid, name)
            planet_id = data["homeworld"].split("/")[-1]
            
            print(f" - Found additional person {name} with id {personid} from planet {planet_id}")
            
            if planet_id in planets:
                planets[planet_id].people.append(person)
                added += 1
                # Add to cache data
                people_cache.append({
                    "id": personid,
                    "name": name,
                    "planet_id": planet_id
                })
            else:
                print(f" - !! Warning: person {person.name} has no associated planet.")
        else:
            print(f" - No additional person found at id {extra_id}")
        
        extra_id += 1

    print(f" - Finished retrieval of people, added {added} people to planets.")
    
    # Save people data to cache
    save_to_cache(people_cache, "people.json")

def get_best():
    # 1. get planets
    planets = get_planets()

    # 2. add people to planets
    add_people(planets)

    # 3. determine side of the force for each person
    # Check if we can use cached force side data
    force_sides_cached = False
    if USE_CACHED_DATA:
        force_sides_data = load_from_cache("force_sides.json")
        if force_sides_data:
            print("\nUsing cached Force sides data")
            force_sides_cached = True
            for planet_id, planet in planets.items():
                for person in planet.people:
                    if person.id in force_sides_data:
                        person.side = force_sides_data[person.id]
                        side_name = "Light Side" if person.side else "Dark Side"
                        print(f" - {person.name} belongs to the {side_name} (from cache)")
    
    if not force_sides_cached:
        print("\nDetermining side of the Force for each person")
        force_sides_data = {}
        for planet_id, planet in planets.items():
            for person in planet.people:
                endpoint_oracle = f"/v1/s1/e3/resources/oracle-rolodex?name={person.name}"
                r = s.get(endpoint_oracle)
                
                if r.status_code == 200:
                    oracle_notes = r.json().get("oracle_notes", "")
                    decoded_notes = base64.b64decode(oracle_notes).decode('utf-8')
                    
                    # Check if light or dark side based on the decoded message
                    if "Light Side" in decoded_notes:
                        person.side = True
                        print(f" - {person.name} belongs to the Light Side")
                    elif "Dark Side" in decoded_notes:
                        person.side = False
                        print(f" - {person.name} belongs to the Dark Side")
                    else:
                        print(f" - Could not determine side for {person.name}: {decoded_notes}")
                    
                    # Cache the force side if determined
                    if person.side is not None:
                        force_sides_data[person.id] = person.side
                else:
                    print(f" - Failed to get oracle info for {person.name}: {r.text}")
        
        # Save force sides data to cache
        save_to_cache(force_sides_data, "force_sides.json")
    
    # 4. Calculate IBF and find balanced planet
    print("\nCalculating IBF for each planet")
    balanced_planet = None
    closest_to_zero = float('inf')
    
    for planet_id, planet in planets.items():
        ibf = planet.ibf()
        if ibf is not None:
            print(f"Planet {planet.name} has IBF: {ibf}")
            if abs(ibf) < abs(closest_to_zero):
                closest_to_zero = ibf
                balanced_planet = planet
    
    if balanced_planet:
        print(f"\nThe most balanced planet is: {balanced_planet.name} with IBF {closest_to_zero}")
        return {
            "planet": balanced_planet.name
        }
    else:
        print("No balanced planet found!")
        return None


def send_ans(payload: dict):
    endpoint = "/v1/s1/e3/solution"
    r = s.post(endpoint, json=payload)

    if r.status_code == 200:
        print(f"Successfully sent answer, response obtained:\n{r.json()}")
    else:
        print(f"Failed to send answer:\n{r.text}")

def main():
    best = get_best()
    if best:
        send_ans(best)

if __name__ == "__main__":
    main()