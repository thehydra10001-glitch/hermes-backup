# Indian Mobile Number Prefix Database

## How Indian Mobile Numbers Work

- **Format:** 10 digits, starts with 6, 7, 8, or 9
- **International:** +91 XXXXXXXXXX
- **First 4-5 digits** determine original operator and telecom circle

## Prefix-to-Operator Mapping (Original Allocation)

**⚠️ Mobile Number Portability (MNP)** may have changed the actual operator. This is the *original* allocation only.

### Vodafone Idea (Vi) — Gujarat Circle (7011-7099)

```
7011-7099: Vodafone Idea (Vi) - Gujarat Circle
```

Full range allocated to Vodafone Idea in Gujarat.

### Other Common Gujarat Prefixes

| Prefix | Operator | Circle |
|--------|----------|--------|
| 7011-7099 | Vodafone Idea (Vi) | Gujarat |
| 8128-8129 | BSNL | Gujarat |
| 9724-9729 | Vodafone Idea (Vi) | Gujarat |
| 9924-9929 | Vodafone Idea (Vi) | Gujarat |

### Operator Prefix Ranges (Pan-India Reference)

| Operator | Typical Prefix Range |
|----------|---------------------|
| Jio | 6200-6299, 7000-7099 (varies), 8588-8599 |
| Airtel | 7000-7099 (varies), 8144-8149, 9844-9849 |
| Vodafone Idea (Vi) | 7011-7099 (Gujarat), 8588-8599 (varies) |
| BSNL | 9411-9499 (varies by circle) |

## Lookup Methods

### Method 1: Prefix Analysis (Free, No API)

```python
# Extract prefix and match against database
number = "7011670115"
prefix4 = number[:4]  # "7011"
prefix5 = number[:5]  # "70116"
```

### Method 2: NumVerify API

```bash
# Requires free API key from numverify.com
curl -s "http://apilayer.net/api/validate?access_key=YOUR_KEY&number=7011670115&country_code=IN"
```

Returns: valid, number, local_format, international_format, country_prefix, country_code, country_name, location, carrier

### Method 3: PhoneInfoga

```bash
source ~/osint-env/bin/activate
cd ~/PhoneInfoga && python3 phoneinfoga.py -n +917011670115
```

## Limitations

1. **MNP (Mobile Number Portability)** — Users can port to any operator; prefix only shows original allocation
2. **Location** — Shows registered telecom circle, not real-time GPS location
3. **Owner name** — Not available via free APIs; requires Truecaller (auth needed) or law enforcement
4. **Live tracking** — Only possible via telecom operator or law enforcement with legal authorization

## Circle Codes

| Circle | State/Region |
|--------|--------------|
| Gujarat | Gujarat, Dadra & Nagar Haveli, Daman & Diu |
| Mumbai | Mumbai, Thane, Navi Mumbai |
| Delhi | Delhi, Noida, Gurgaon |
| Maharashtra | Maharashtra (excl. Mumbai) |
| Karnataka | Karnataka |
| Tamil Nadu | Tamil Nadu, Chennai |
| Andhra Pradesh | Andhra Pradesh, Telangana |
| Kolkata | West Bengal |
| Punjab | Punjab, Chandigarh |
| Rajasthan | Rajasthan |
| UP East | Uttar Pradesh (East) |
| UP West | Uttar Pradesh (West) |
| MP & Chhattisgarh | Madhya Pradesh, Chhattisgarh |
| Bihar & Jharkhand | Bihar, Jharkhand |
| Orissa | Odisha |
| Assam | Assam |
| North East | NE states (Meghalaya, Mizoram, etc.) |
| HP | Himachal Pradesh |
| J&K | Jammu & Kashmir |
| Kerala | Kerala |
| Haryana | Haryana |

## Sources

- TRAI (Telecom Regulatory Authority of India) allocation data
- Operator-wise prefix allocation lists
- Community-maintained databases (may be outdated)
