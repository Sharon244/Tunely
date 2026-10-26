# Tunely — Lyrics-Based Music Recommendation App

Tunely is a Streamlit music recommendation app that suggests tracks with lyrics similar to a selected song. The current app uses a precomputed song dataset and cosine-similarity matrix.

## Features
- Select a song from the available dataset
- Choose how many similar songs to receive
- View recommended songs and artists
- Dark interface with custom styling

## Technologies
- Python
- Streamlit
- Pandas
- TF-IDF and cosine similarity (used to build the recommendation data)

## Project files
- `app.py` — Streamlit user interface and recommendation logic
- `requirements.txt` — Python dependencies

## Run locally
1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Place the required data files in this folder: `df.pkl` and `similarity.pkl`.
5. Start the app:

   ```bash
   streamlit run app.py
   ```

## Data files note
The current version of `app.py` loads `df.pkl` and `similarity.pkl`. These files were not included in this upload pack because they were not available with the app source file. The app will need those generated files to run. Do not upload copyrighted or private datasets unless you have permission to share them. You can instead add instructions or code for generating the files from a permitted dataset.

## Future improvements
- Add a reproducible preprocessing and model-building notebook
- Add validation for missing data files
- Deploy the app so it can be tried online
