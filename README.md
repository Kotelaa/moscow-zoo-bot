# 🐾 Moscow Zoo totem bot

A Telegram bot designed for the Moscow Zoo concept. The main goal is to help users discover their "totem animal" through a quiz and encouraging them to participate 
in the guardianship program.

> **Note:** This is an educational project. I am not affiliated with the Moscow Zoo. All images and brand assets are used for demonstration purposes only.

---

## Features

- **Totem Quiz** – an 8-question survey using a Finite State Machine (FSM) to determine the user's animal match
- **Custom results** – each result includes a photo and description of the matched animal, designed to be shareable
- **Guardianship feature** – after the quiz, users can send their result to a zoo staff member to ask about becoming an animal guardian
- **Privacy command** – `/privacy` explains exactly what happens with user data
- **Async performance** – built on Aiogram 3, stays fast even with multiple users at the same time
- **Monitoring** – integrated logging that tracks errors and response times to a file

---

## Tech Stack

- **Language:** Python 3.14 
- **Framework:** Aiogram 3.25.0
- **State Management:** Aiogram FSM
- **Formatting:** HTML & `aiogram.utils.formatting`
- **Config:** Environment variables (`.env` / Token file)
- **Logging:** File-based error and performance logging

---

## Commands

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/survey` | Start the totem animal quiz |
| `/privacy` | Data handling information |
| `/contact` | Official zoo links |

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/Kotelaa/moscow-zoo-bot
cd MoscowZooBot
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install aiogram
```

**4. Add your bot token**

Create a `Token.py` file (or `.env` file) and add:
```python
TOKEN = "your-telegram-bot-token"
```

**5. Run the bot**
```bash
python main.py
```

