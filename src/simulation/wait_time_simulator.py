def calculate_wait_time(
    vehicles,
    green_seconds,
    weather="Clear",
    accident=False
):
    cycle_seconds = 54

    capacity = 0.5

    if weather == "Rainy":
        capacity *= 0.85

    if accident:
        capacity *= 0.60

    # Yesil isik boyunca gecebilen arac sayisi
    passed_vehicles = min(
        vehicles,
        int(green_seconds * capacity)
    )

    # Kuyrukta kalan arac sayisi
    remaining_vehicles = vehicles - passed_vehicles

    # Gecen araclarin ortalama bekleme suresi
    # Baslangicta hepsinin kuyrukta oldugu varsayiliyor.
    if passed_vehicles > 0:
        passed_wait = sum(
            (i + 1) / capacity
            for i in range(passed_vehicles)
        )
    else:
        passed_wait = 0

    # Gecemeyen araclar en az bir dongu bekliyor
    remaining_wait = remaining_vehicles * cycle_seconds

    total_wait = passed_wait + remaining_wait

    if vehicles == 0:
        return 0

    return total_wait / vehicles


def simulate_average_wait(
    main_vehicles,
    side_vehicles,
    main_green,
    side_green,
    weather="Clear",
    accident=False
):
    main_wait = calculate_wait_time(
        main_vehicles,
        main_green,
        weather,
        accident
    )

    side_wait = calculate_wait_time(
        side_vehicles,
        side_green,
        weather,
        False
    )

    total_vehicles = main_vehicles + side_vehicles

    if total_vehicles == 0:
        return 0

    return (
        main_wait * main_vehicles
        + side_wait * side_vehicles
    ) / total_vehicles