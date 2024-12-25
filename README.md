# IS353.P12.HTCL - Social Network

## Course Information
**Course**: IS353.P12.HTCL - Social Network
**Lecturer**: MSc. Thao Bao Tran
**Semester**: 1, 2024-2025  

## Team Information
| No. | Student ID | Full Name           |
| --- | ---------- | ------------------- |
| 1   | 21520596   | Tran Thi Kim Anh    |
| 2   | 21521049   | Ho Quang Lam        |
| 3   | 21521586   | Le Thi Le Truc (Leader) |
| 4   | 21521882   | Le Minh Chanh       |

## Project Information
**Project Title**: `MOVIE RECOMMENDATION SYSTEM SOCIAL NETWORK DESIGN`
**Dataset**: [MovieLens32M](https://grouplens.org/datasets/movielens/32m/) and [Movie Data from TMDB API](https://developer.themoviedb.org/docs/getting-started)

## Overview dataset
The dataset includes the main attributes: `userId` and `tmdbId` (Movie ID), used to record user ratings for movies. The dataset is a filtered version of the original dataset, consisting of `5,345 rows and 5 attributes`. These attributes will be used in the process of developing algorithms in social networks, recommending movies to users, and building a website.

## Summary
- **Build a user graph from a bipartite User-Movie graph**  
- **Display and calculate basic graph metrics**  
- **Compute centrality measures and identify key players in the graph**  
- **Community detection**  
  - Explore communities using the Girvan-Newman and Louvain algorithms.  
  - Recommend movies based on the community detection results.  
- **Link prediction**  
  - Predict links using Heuristics methods.  
  - Recommend movies for the users at both ends of the predicted links.  
- **Simulate information diffusion using the Independent Cascade (IC) model**  
  - Generate a list of recommended movies for affected users based on the diffusion results.  

## Technology: 
**Python**: NetworkX, Pandas, Numpy, Scikit-learn, Matplotlib, Seaborn, Streamlit, FastAPI, Python-louvain, Community


## SETUP
### 1. To run the `SocialNetworkSource.ipynb` file:
Open the terminal in the folder containing `requirements.txt` and run the following command to install the required libraries:

### 2. To run the Website:
#### Movie Recommendation Website

This project involves a movie recommendation website that uses community detection algorithms, link prediction, and information propagation in social networks. The website is built using Python with Streamlit and FastAPI.

#### Setup Instructions
To start the API and the web interface simultaneously, execute the following command in the terminal within the `./Website` directory:
```bash
py run.py
```
Then, access the web application at http://localhost:8501/.
The API will be available at http://127.0.0.1:8000/docs.





