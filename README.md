# Vehicle Parts Analysis

A graph theory-based analysis of vehicle parts sharing in the automotive industry.

## Structure

- `src/`: Source code modules.
- `docs/`: Reports and documentation files.
- `assets/`: Generated images and assets.
- `tests/`: Automated tests.

## Installation

1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the interactive analysis tool:

```bash
python -m src.main
```

## Features

- Bipartite graph modeling (Car-Part relationships).
- Projected graph analysis (Car-Car compatibility).
- Community detection and clustering.
- Resilience testing and supply chain analysis.
