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
### 1. Để chạy file SocialNetworkSource.ipynb: 
Mở terminal trong folder chứa `requirements.txt` để chạy lệnh cài đặt thư viện: 
  ```
  pip install -r requirements.txt
  ```
### 2. Để chạy Website:
#### Website gợi ý phim

Dự án này liên quan đến một website gợi ý phim sử dụng thuật toán khám phá cộng đồng, dự đoán liên kết và lan truyền thông tin trong mạng xã hội. Website này được xây dựng bằng Python sử dụng Streamlit và FastAPI.

#### Hướng dẫn thiết lập
Để khởi động API và giao diện web cùng lúc, thực hiện lệnh terminar ở thư mục `./Website`
```bash
py run.py
```
Sau đó, truy cập vào địa chỉ http://localhost:8501/ để sử dụng ứng dụng web.
API sẽ được chạy ở địa chỉ http://127.0.0.1:8000/docs.




