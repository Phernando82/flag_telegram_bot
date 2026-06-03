# Country Flag Bot

Telegram data query bot · Python · python-telegram-bot · REST API integration

---

## Overview

Telegram bot that resolves country identifiers — name, ISO Alpha-2, ISO Alpha-3, or UN numeric code — into flag images via the CountryFlagsAPI. Demonstrates REST API consumption, input normalization, and asynchronous message handling using the `python-telegram-bot` v20+ async architecture. The same lookup-and-respond pattern is directly applicable to industrial asset query bots, where operators retrieve equipment status or sensor readings via chat interface.

---

## Technical Highlights

**Async handler architecture (python-telegram-bot v20+)**
Each command and message is processed by a dedicated async handler registered on the Application dispatcher. Non-blocking execution keeps the bot responsive under concurrent user requests — the same concurrency model used in IoT gateway services handling simultaneous device messages.

**Multi-format identifier resolution**
A single lookup accepts four input formats (country name, ISO Alpha-2, ISO Alpha-3, UN numeric code) and resolves them against a normalized reference dataset. Equivalent to tag aliasing in industrial historians, where a device can be queried by asset ID, tag name, or location code.

**External REST API integration**
Validated queries are forwarded to CountryFlagsAPI as dynamic URL endpoints. Demonstrates the request-build → validate → dispatch → deliver pipeline common to IoT cloud connectors and industrial API gateways.

**Input normalization pipeline**
Raw user input is lowercased and whitespace-normalized before lookup, making the resolution tolerant of formatting inconsistencies — a standard preprocessing step in industrial data ingestion pipelines dealing with operator free-text input.

**Environment-based configuration**
Bot token is loaded from environment variables via `python-decouple`, keeping credentials out of source code. Standard practice for secrets management in containerized industrial edge deployments.

---

## Stack

Python 3.10+ · python-telegram-bot v20+ · CountryFlagsAPI · python-decouple · asyncio

---

## Installation

```bash
git clone https://github.com/Phernando82/flag_telegram_bot.git
cd country-flag-bot
pip install -r requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
# Edit .env:
# TOKEN=your_telegram_bot_token
```

Run:

```bash
python main.py
```

---

## Usage

| Input | Example |
|---|---|
| Country name | `Brazil` |
| ISO Alpha-2 | `BR` |
| ISO Alpha-3 | `BRA` |
| UN numeric code | `076` |

Reference for all codes: https://www.iban.com/country-codes

**Commands:**

```
/start   — welcome message and usage instructions
/help    — reference guide with link to code table
```

Any non-command message is treated as a country lookup.

---

## Architecture

```
User input (Telegram)
      │
      ▼
  Input normalization (lowercase + whitespace strip)
      │
      ▼
  Lookup against reference dataset (195 countries, 4 identifier formats)
      │
      ├── Not found → error message with reference link
      │
      └── Found → build CountryFlagsAPI URL → reply with flag
```

---

## Relevance to Industry 4.0

The core pattern — receive identifier, normalize input, validate against reference dataset, query external API, return structured response — maps directly to industrial operator assist bots:

- **Multi-format identifier resolution** → querying assets by tag name, IP, serial number, or location code in a CMMS or historian
- **Async handler dispatcher** → event-driven message routing in MQTT brokers or OPC-UA servers
- **REST API dispatch pipeline** → integration layer between Telegram/chat interfaces and industrial REST APIs (Ignition, Node-RED, cloud IoT platforms)
- **Environment-based secrets** → credential management in containerized edge deployments (Docker, Kubernetes on industrial gateways)

---

## Known Limitations

- CountryFlagsAPI (`countryflagsapi.com`) is a third-party service; availability depends on the provider.
- Partial name matching is not supported — input must match a known identifier exactly.

---

## License

MIT · Bug reports: @Phernando82
