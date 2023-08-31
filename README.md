# PROJECT_VIVINO
![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-brightgreen.svg)
![Pandas](https://img.shields.io/badge/Made%20with-Pandas-blue.svg)
![SQLAlchemy](https://img.shields.io/badge/Powered%20by-SQLAlchemy-blue.svg)
![Tableau](https://img.shields.io/badge/Uses-Tableau-9cf.svg)

## Project Description
Vivino is the world’s largest online wine marketplace and most downloaded wine app with a reliable online community is made up of millions of wine drinkers from around the world, coming together to make buying the right wine simple, straightforward, and fun by utilizing crowd-sourced data to personalize wine recommendations so that every community member feels confident about their wine choices.

This project is aimed to provide an interactive analysis of vivino market segmentation. The project is built on top of the provided dataset, which can be retrieved from [this link](https://drive.google.com/file/d/122rj3-c0mpFPL04IXeXjSp2_H66-33RS/view?usp=sharing). 

## Folder Structure
```bash
project_vivino
├── data
│   ├── tableau_work
│   │   ├── Screenshot (11).png
│   │   ├── vivino1.pdf.twb
│   │   ├── vivino1.twbx     
│   ├── vivino_database.accdb
│   └── vivino_db.mdb
│   └── vivino.db    
├── notebooks
│   ├── vivino_market_analysis.ipynb
├── output
│   ├── Parameters.pdf
│   └── price_dist_provinces.png
├── src
│   └── vivino_streamlit.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements_vivino.txt
```

## Installation

To set up the project locally, follow these steps:

1. Clone the repository: `git clone https://github.com/mfirdaus354/project_vivino.git`
2. Change into the project directory: `cd project_vivino`
3. Install the required dependencies: `pip install -r requirements_vivino.txt`

## Usage

To use the project, follow these steps:

1. Ensure the dependencies are installed (see [Installation](#installation)).
2. In order to run the streamlit app, execute this following command in a Terminal window
        'python -m streamlit run ./src/vivino_streamlit.py'
3. The analysis of the dataset is accesible by opening the vivino_market_analysis.ipynb in the notebooks folder

## INSIGHTS

### QUESTION 1
We want to highlight 10 wines to increase our sales. Which ones should we choose and why?
- Those with good ratings but not a big amount of ratings
- Natural wines?
![answer](./output/Screenshot%202023-08-31%20161953.png). 

### QUESTION 2
