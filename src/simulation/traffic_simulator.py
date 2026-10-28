

def calculate_queue(
    start_queue,
    arriving_vehicles,
    green_seconds,
    weather="Clear",
    accident=False
):
    capacity_per_second = 0.5

    if weather == "Rainy":
        capacity_per_second *= 0.85

    if accident:
        capacity_per_second *= 0.60

    total_vehicles = start_queue + arriving_vehicles

    passed_vehicles = min(
        total_vehicles,
        int(green_seconds * capacity_per_second)
    )

    remaining_queue = total_vehicles - passed_vehicles

    return remaining_queue


def simulate_intersection(
    main_vehicles,
    side_vehicles,
    main_green,
    side_green,
    weather="Clear",
    accident=False
):
    if main_green + side_green != 54:
        raise ValueError("Toplam yesil sure 54 saniye olmali")

    if not (10 <= main_green <= 44 and 10 <= side_green <= 44):
        raise ValueError("Yesil sureler 10 ile 44 saniye arasinda olmali")

    main_queue = calculate_queue(
        start_queue=0,
        arriving_vehicles=main_vehicles,
        green_seconds=main_green,
        weather=weather,
        accident=accident
    )

    side_queue = calculate_queue(
        start_queue=0,
        arriving_vehicles=side_vehicles,
        green_seconds=side_green,
        weather=weather,
        accident=False
    )

    return {
        "main_queue": main_queue,
        "side_queue": side_queue,
        "total_queue": main_queue + side_queue
    }



def find_best_green_time(
    main_vehicles,
    side_vehicles,
    weather="Clear",
    accident=False
):
    best_result = None
    best_main_green = 0
    best_side_green = 0

    for main_green in range(10, 45):
        side_green = 54 - main_green

        result = simulate_intersection(
            main_vehicles=main_vehicles,
            side_vehicles=side_vehicles,
            main_green=main_green,
            side_green=side_green,
            weather=weather,
            accident=accident
        )

        if best_result is None or result["total_queue"] < best_result["total_queue"]:
            best_result = result
            best_main_green = main_green
            best_side_green = side_green

    return {
        "main_green": best_main_green,
        "side_green": best_side_green,
        "total_queue": best_result["total_queue"]
    }