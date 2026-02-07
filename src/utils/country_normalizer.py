"""Normalize country names and codes to ISO 2-letter format."""


# Mapping of various country formats to ISO 2-letter codes
COUNTRY_MAP = {
    # United States variations
    'US': 'US',
    'USA': 'US',
    'UNITED STATES': 'US',
    'UNITED STATES OF AMERICA': 'US',
    'U.S.': 'US',
    'U.S.A.': 'US',

    # Canada variations
    'CA': 'CA',
    'CANADA': 'CA',
    'CAN': 'CA',

    # United Kingdom variations
    'GB': 'GB',
    'UK': 'GB',
    'UNITED KINGDOM': 'GB',
    'GREAT BRITAIN': 'GB',
    'ENGLAND': 'GB',
    'SCOTLAND': 'GB',
    'WALES': 'GB',

    # Australia variations
    'AU': 'AU',
    'AUS': 'AU',
    'AUSTRALIA': 'AU',

    # India variations
    'IN': 'IN',
    'IND': 'IN',
    'INDIA': 'IN',

    # Germany variations
    'DE': 'DE',
    'DEU': 'DE',
    'GERMANY': 'DE',
    'DEUTSCHLAND': 'DE',

    # France variations
    'FR': 'FR',
    'FRA': 'FR',
    'FRANCE': 'FR',

    # Netherlands variations
    'NL': 'NL',
    'NLD': 'NL',
    'NETHERLANDS': 'NL',
    'NEDERLAND': 'NL',
    'HOLLAND': 'NL',

    # New Zealand variations
    'NZ': 'NZ',
    'NZL': 'NZ',
    'NEW ZEALAND': 'NZ',

    # Ireland variations
    'IE': 'IE',
    'IRL': 'IE',
    'IRELAND': 'IE',

    # Spain variations
    'ES': 'ES',
    'ESP': 'ES',
    'SPAIN': 'ES',
    'ESPAÑA': 'ES',

    # Italy variations
    'IT': 'IT',
    'ITA': 'IT',
    'ITALY': 'IT',
    'ITALIA': 'IT',

    # Japan variations
    'JP': 'JP',
    'JPN': 'JP',
    'JAPAN': 'JP',

    # China variations
    'CN': 'CN',
    'CHN': 'CN',
    'CHINA': 'CN',

    # Mexico variations
    'MX': 'MX',
    'MEX': 'MX',
    'MEXICO': 'MX',

    # Brazil variations
    'BR': 'BR',
    'BRA': 'BR',
    'BRAZIL': 'BR',
    'BRASIL': 'BR',

    # Add more as needed...
}


# Country code to full name mapping (for display)
COUNTRY_NAMES = {
    'US': 'United States',
    'CA': 'Canada',
    'GB': 'United Kingdom',
    'AU': 'Australia',
    'IN': 'India',
    'DE': 'Germany',
    'FR': 'France',
    'NL': 'Netherlands',
    'NZ': 'New Zealand',
    'IE': 'Ireland',
    'ES': 'Spain',
    'IT': 'Italy',
    'JP': 'Japan',
    'CN': 'China',
    'MX': 'Mexico',
    'BR': 'Brazil',
}


def normalize_country(country: str) -> str:
    """
    Normalize country name/code to ISO 2-letter format.

    Args:
        country: Country name or code in any format

    Returns:
        ISO 2-letter country code, or original value if not found
    """
    if not country:
        return None

    # Clean and uppercase
    country_clean = country.strip().upper()

    # Remove common variations
    country_clean = country_clean.replace('.', '')

    # Look up in mapping
    normalized = COUNTRY_MAP.get(country_clean)

    if normalized:
        return normalized

    # If already 2-letter code not in map, return as-is
    if len(country_clean) == 2:
        return country_clean

    # Otherwise return None (Unknown)
    return None


def get_country_name(code: str) -> str:
    """
    Get full country name from ISO code.

    Args:
        code: 2-letter ISO country code

    Returns:
        Full country name, or the code if not found
    """
    if not code:
        return 'Unknown'

    return COUNTRY_NAMES.get(code.upper(), code)
