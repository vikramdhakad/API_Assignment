CONVERSION_RATES = {
    'Argentine Peso': 1362.405328,
    'Australian Dollar': 1.545985,
    'Bahraini Dinar': 0.376000,
    'Botswana Pula': 13.258752,
    'Brazilian Real': 5.546294,
    'British Pound': 0.753523,
    'Bruneian Dollar': 1.289309,
    'Bulgarian Lev': 1.687067,
    'Canadian Dollar': 1.379705,
    'Chilean Peso': 969.313382,
    'Chinese Yuan Renminbi': 7.211799,
    'Colombian Peso': 4127.206764,
    'Czech Koruna': 21.202637,
    'Danish Krone': 6.441233,
    'Emirati Dirham': 3.672500,
    'Euro': 0.862584,
    'Hong Kong Dollar': 7.849301,
    'Hungarian Forint': 344.082137,
    'Icelandic Krona': 123.695327,
    'Indian Rupee': 87.235520,
    'Indonesian Rupiah': 16439.206668,
    'Iranian Rial': 42002.575623,
    'Israeli Shekel': 3.413635,
    'Japanese Yen': 147.415802,
    'Kazakhstani Tenge': 543.194422,
    'Kuwaiti Dinar': 0.305656,
    'Libyan Dinar': 5.455606,
    'Malaysian Ringgit': 4.277073,
    'Mauritian Rupee': 46.701591,
    'Mexican Peso': 18.858887,
    'Nepalese Rupee': 139.642259,
    'New Zealand Dollar': 1.690248,
    'Norwegian Krone': 10.238938,
    'Omani Rial': 0.384994,
    'Pakistani Rupee': 282.838964,
    'Philippine Peso': 57.887110,
    'Polish Zloty': 3.686461,
    'Qatari Riyal': 3.640000,
    'Romanian New Leu': 4.378168,
    'Russian Ruble': 80.000111,
    'Saudi Arabian Riyal': 3.750000,
    'Singapore Dollar': 1.289309,
    'South African Rand': 18.157526,
    'South Korean Won': 1387.775932,
    'Sri Lankan Rupee': 301.283893,
    'Swedish Krona': 9.653996,
    'Swiss Franc': 0.804112,
    'Taiwan New Dollar': 29.754394,
    'Thai Baht': 32.748036,
    'Trinidadian Dollar': 6.768490,
    'Turkish Lira': 40.637478
}


def convert_price(usd_amount, target_currency):
    # Case-insensitive exact match
    for name in CONVERSION_RATES:
        if name.lower() == target_currency.lower():
            rate = CONVERSION_RATES[name]
            converted = round(usd_amount * rate, 2)
            return {"converted_price": converted, "currency": name}

    # Partial (substring) match if unambiguous
    matches = [name for name in CONVERSION_RATES if target_currency.lower() in name.lower()]
    if len(matches) == 1:
        rate = CONVERSION_RATES[matches[0]]
        converted = round(usd_amount * rate, 2)
        return {"converted_price": converted, "currency": matches[0]}
    if len(matches) > 1:
        return {
            "error": f"Ambiguous currency name '{target_currency}'. Did you mean one of: {', '.join(matches[:5])}?"
        }

    return {"error": "Unsupported currency"}

