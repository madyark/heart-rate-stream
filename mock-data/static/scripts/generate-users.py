from faker import Faker
from datetime import datetime, timezone
import random
import pandas as pd
import os
from typing import Tuple, List
import logging


def select_from_probabilities(
    options_with_probabilities: List[Tuple[str, float]]
) -> str:
    """
    Selects an option from a list based on probabilities.

    Args:
        options_with_probabilities (list of tuple):
            A list of tuples where each tuple contains an option
            and its corresponding probability.

    Returns:
        str: The selected option.
    """
    cumulative_probabilities = []
    total_probability = 0

    # Calculate cumulative probabilities
    for _, probability in options_with_probabilities:
        total_probability += probability
        cumulative_probabilities.append(total_probability)

    # Generate a random number within the total probability range
    random_number = random.randint(1, cumulative_probabilities[-1])

    # Select the option based on the random number
    for i, cumulative_probability in enumerate(cumulative_probabilities):
        if random_number <= cumulative_probability:
            selected_option = options_with_probabilities[i][0]
            break

    return selected_option


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # List of Latin-based locales supported by Faker and corresponding country names
    locales = [
        ("en_US", "US", "United States"),
        ("en_GB", "GB", "United Kingdom"),
        ("en_AU", "AU", "Australia"),
        ("pt_BR", "BR", "Brazil"),
        ("es_ES", "ES", "Spain"),
        ("fr_FR", "FR", "France"),
        ("de_DE", "DE", "Germany"),
        ("it_IT", "IT", "Italy"),
        ("nl_NL", "NL", "Netherlands"),
        ("sv_SE", "SE", "Sweden"),
        ("no_NO", "NO", "Norway"),
        ("fi_FI", "FI", "Finland"),
        ("da_DK", "DK", "Denmark"),
        ("pl_PL", "PL", "Poland"),
    ]

    height_mean_male = 175
    height_stddev_male = 8
    weight_mean_male = 80
    weight_stddev_male = 10

    height_mean_female = 162
    height_stddev_female = 7
    weight_mean_female = 65
    weight_stddev_female = 8

    # List of blood types with corresponding probabilities
    blood_types_with_probabilities = [
        ("A+", 35),
        ("A-", 6),
        ("B+", 15),
        ("B-", 2),
        ("AB+", 3),
        ("AB-", 1),
        ("O+", 36),
        ("O-", 2),
    ]

    # List of races with corresponding probabilities
    races_with_probabilities = [
        ("W", 40),
        ("B", 20),
        ("A", 15),
        ("H", 20),
        ("O", 5),
    ]

    user_data = []
    for i in range(9999):
        # Randomly select a locale
        locale, country_code, country_name = random.choice(locales)

        # Generate fake patient data using the selected locale
        fake = Faker(locale)

        dob = fake.date_of_birth(minimum_age=18, maximum_age=100)
        dob_int = int(dob.strftime("%Y%m%d"))  # reformat date of birth to YYYYMMDD

        race = select_from_probabilities(races_with_probabilities)
        blood_type = select_from_probabilities(blood_types_with_probabilities)

        # Generate first name, height, and weight based on sex
        sex = fake.random_element(elements=("M", "F"))
        if sex == "M":
            first_name = fake.first_name_male()
            height = round(random.gauss(height_mean_male, height_stddev_male))
            weight = round(random.gauss(weight_mean_male, weight_stddev_male))
        else:
            first_name = fake.first_name_female()
            height = round(random.gauss(height_mean_female, height_stddev_female))
            weight = round(random.gauss(weight_mean_female, weight_stddev_female))

        last_name = fake.last_name()

        # Have a 10% chance of user residing outside of their country of origin
        if random.random() < 0.1:
            (
                new_locale,
                address_country_code,
                address_country_name,
            ) = random.choice(locales)
            new_fake = Faker(new_locale)
            new_fake.seed_locale(new_locale)
            address = new_fake.address().title().replace("\n", ", ")
        else:
            address_country_code = country_code
            address_country_name = country_name
            address = fake.address().title().replace("\n", ", ")

        # Generate current timestamp with timezone as last update
        last_update = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        user_record = {
            "userid": 10001 + i,
            "fname": first_name,
            "lname": last_name,
            "dob": dob_int,
            "sex": sex,
            "height": height,
            "weight": weight,
            "blood_type": blood_type,
            "race": race,
            "origin_country_code": country_code,
            "origin_country_name": country_name,
            "address": address,
            "address_country_code": address_country_code,
            "address_country_name": address_country_name,
            "last_update": last_update,
        }
        user_data.append(user_record)
        logging.info(f"New user generated {i+1}")

    df = pd.DataFrame(user_data)
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "users.csv")
    df.to_csv(csv_file_path, index=False)
    logging.info("Users data successfully created")


main()
