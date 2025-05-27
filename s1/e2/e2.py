import utils.session as s
import utils.ui as ui

class Position:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Star:

    def __init__(self, id: str, resonance: int , position: Position):
        self.id = id
        self.resonance = resonance
        self.position = position

    def __str__(self):
        return f"{self.id}: resonance={self.resonance}, position=({self.position.x}, {self.position.y}, {self.position.z}))"

def get_stars():
    endpoint = lambda page, sort_by, sort_direction: f"/v1/s1/e2/resources/stars?page={page}&sort-by={sort_by}&sort-direction={sort_direction}"
    print(f"\nObtaining stars")

    stars: list[Star] = []
    stars_per_response = 3

    # 1. get the total number of stars
    response0 = s.get(endpoint(1, "id", "desc"))

    if response0.status_code != 200:
        ui.error(f"Failed to fetch initial request to obtain total stars: {response0.status_code} - {response0.text}")
        return

    total_stars = response0.headers["x-total-count"]
    print(f"Total stars available: {total_stars}")

    for p in range(1, int(total_stars) // stars_per_response + 2):
        response = s.get(endpoint(p, "id", "desc"))

        if response.status_code != 200:
            ui.error(f"Failed to fetch stars from page {p}: {response.status_code} - {response.text}")
            return

        if len(response.json()) == 0:
            print(f"No more stars found in page {p}.")
            break

        page_stars: list[Star] = [ Star(s["id"], s["resonance"], Position(s["position"]["x"], s["position"]["y"], s["position"]["z"])) for s in response.json() ]
        stars.extend(page_stars)

        print(f"Obtained stars from page {p}: {len(response.json())}")

    return stars

def find_avg_resonance(stars: list[Star]) -> int:
    if not stars:
        ui.error("No stars found to calculate average resonance.")
        return 0

    total_resonance = sum(star.resonance for star in stars)
    avg_resonance = total_resonance // len(stars)

    print(f"\nAverage resonance: {avg_resonance}")
    return avg_resonance

def send_ans(avg_resonance: int):
    endpoint = "/v1/s1/e2/solution"
    body = {
        "average_resonance": avg_resonance
    }
    print(f"\nStarted petition to send answer")
    response = s.post(endpoint, json=body)

    if response.status_code != 200:
        print(f"- error sending answer: {response.text}")
    else:
        print(f"- answer sent succesfully, feedback from server: {response.text}")

def main():
    stars = get_stars()
    send_ans(find_avg_resonance(stars))


if __name__ == '__main__':
    main()

# fe05a4b2-9bad-4ea8-95ff-e9c9b258ec2c: resonance=133, position=(0.577352145256762, 0.7045718362149235, 0.045824383655662215))

# fdce2d4c-d1de-44f4-97cd-7926b978a049: resonance=546, position=(0.5557683234056182, 0.718408275296326, 0.15479682527406413))}

# fd81715a-992a-4b59-8310-a5f02ed0c167: resonance=399, position=(0.5175758410355906, 0.12100419586826572, 0.22469733703155736))