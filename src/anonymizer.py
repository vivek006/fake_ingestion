import pandas as pd

def generalize_age(birthdate):
    """
    Generalizes the age into a 10-year age group based on birthdate.
    """
    year = int(birthdate.split('-')[0])
    age_group = (2023 - year) // 10 * 10
    return f"[{age_group}-{age_group + 10}]"

def anonymize_data(data):
    """
    Anonymizes and processes the downloaded data by masking user-identifiable information,
    except for city and country.

    Args:
        data (list): List of dictionaries representing user data.

    Returns:
        pd.DataFrame: Processed and anonymized data.
    """
    anonymized = []
    for entry in data:
        # Masking user-identifiable information
        name = "****"  # Mask the name
        phone_number = "****"  # Mask the phone number
        email_domain = entry["email"].split('@')[1]  # Keep only the email domain
        location = entry.get("address", {})

        # Mask the address-related information (but leave city and country unmasked)
        street = "****"
        street_name = "****"
        building_number = "****"
        city = entry["address"].get("city", "****").lower()  # Unmasked city
        country = entry["address"].get("country", "****").lower()  # Unmasked country
        zipcode = "****"  # Mask the zip code
        latitude = None  # Mask geographical coordinates
        longitude = None

        # Generalize the age
        age_group = generalize_age(entry["birthday"])

        # Add anonymized data to the list
        anonymized.append({
            "name": name,
            "phone_number": phone_number,
            "email_domain": email_domain,
            "street": street,
            "street_name": street_name,
            "building_number": building_number,
            "city": city,  # Unmasked city
            "zipcode": zipcode,
            "country": country,  # Unmasked country
            "latitude": latitude,
            "longitude": longitude,
            "age_group": age_group
        })

    return pd.DataFrame(anonymized)
