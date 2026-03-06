# Cooking AI Agent (Chef AI)

An interactive cooking assistant powered by **GitHub Models** (GPT-4.1) and **Microsoft Agent Framework**. Chef AI helps with recipe search, ingredient extraction, substitutions, and unit conversions.

## Features

- **Recipe Search** — Find recipes by dish name, cuisine, ingredient, or dietary tag
- **Ingredient Extraction** — Get structured ingredient lists with quantities, units, and items
- **Substitutions** — Get ingredient alternatives for dietary needs, allergies, or availability
- **Unit Conversion** — Convert between cups, grams, ounces, tablespoons, and more

## Prerequisites

- Python 3.10+
- A [GitHub Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with access to GitHub Models

## Setup

1. **Create and activate a virtual environment:**

   ```bash
   cd cooking-agent
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your GitHub token:**

   Edit the `.env` file and replace `your_github_pat_here` with your actual GitHub PAT:

   ```
   GITHUB_TOKEN=ghp_your_actual_token_here
   MODEL_ID=openai/gpt-4.1
   ```

## Usage

### Interactive Console Mode

```bash
python app.py --cli
```

Chat with Chef AI in your terminal — ask for recipes, substitutions, conversions, and more.

### HTTP Server Mode (default)

```bash
python app.py
```

Starts the agent as an HTTP server, ready for production use and integration with AI Toolkit Agent Inspector for debugging.

## Debugging (VS Code)

Press **F5** to launch with the pre-configured debug setup:
- **Debug Local Agent/Workflow HTTP Server** — Runs the HTTP server with debugpy and opens the AI Toolkit Agent Inspector
- **Debug Local Agent/Workflow in Terminal** — Runs in CLI mode with debugger attached

## Example Prompts

- "Find me a quick Italian recipe"
- "What can I make with chicken and yogurt?"
- "Extract the ingredients from Pad Thai"
- "What can I use instead of eggs in baking?"
- "Convert 2 cups to milliliters"
- "I'm vegan, suggest substitutions for the Caesar Salad recipe"

## Model Configuration

The app uses **GPT-4.1** via GitHub Models by default. To change models, update `MODEL_ID` in `.env`:

```
MODEL_ID=openai/gpt-4.1-mini   # Lighter, faster option
```

> **Note:** Agent Framework packages are pinned to `1.0.0b260107` (preview). Check for updates but be aware of potential breaking API changes.
