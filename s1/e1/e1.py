import utils.session as s

def get_read() -> dict:
    # Measures found after 87 attempts
    # Time: 2.1530864197530866 hours
    # Distance: 872 AU
    print(f"\nProcess to find a measure started")

    # call this endpoint as many times as possible till finally we get a response without the failure message. the code will always be 200.
    failure_msg = "failed to measure, try again"
    endpoint = "/v1/s1/e1/resources/measurement"
    
    attemps = 0
    limit = 1000
    found = False

    while not found:
        attemps += 1
        r = s.get(endpoint)
        if r.status_code == 200:
            read = r.json()
            rtime = read["time"]
            rdistance = read["distance"]
            if failure_msg not in f"{rtime} {rdistance}":
                # we have a found valid measures if so
                found = True
            if attemps > limit:
                print("Reached the limit of attempts")
                found = False
        else:
            print(f"Unexpected error as it did not return 200 code: {r.status_code}")
            found = False

    if found:
        print(f"\nMeasures found after {attemps} attempts")
        print(f"Time: {rtime}")
        print(f"Distance: {rdistance}")
    else:
        print(f"\nNo measures found after {limit} attempts, exiting.\n\n\n")
        exit(0)

    return read

def format_read(read) -> dict:
    # converts the values of the read dict to float
    read["distance"] = float(read["distance"].strip().replace("AU", ""))
    read["time"] = float(read["time"].strip().replace("hours", ""))
    return read

def calc_speed(read: dict) -> int:
    # calculate the instantaneous orbital speed of the planet till the closest integer number
    read = format_read(read)
    speed = round(read["distance"] / read["time"])
    print(f"\nSpeed calculated for the read: {speed}")
    return speed
    
def send_answer(speed: int):
    print(f"\nSending the answer")
    endpoint = "/v1/s1/e1/solution"
    body = {
        "speed": speed
    }
    response = s.post(endpoint, json=body)

    if response.status_code == 200:
        print(f"Answer sent successfully:\n{response.json()}")
    else:
        print(f"Failed to send the answer. Status code: {response.status_code}")
        print(f"Response body: {response.text}")

def main():
    read = get_read()
    speed = calc_speed(read)
    send_answer(speed)
    print("\n\n")

# ~ ~ ~ ~ #

if __name__ == "__main__":
    main()
