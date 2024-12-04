from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Biến lưu trữ dữ liệu trên RAM
movies = []
users = []
ratings = []

# Đọc dữ liệu từ file CSV
def load_data():
    df = pd.read_csv("../../Dataset/Dataset.csv")
    df = df.fillna(' ') 
    global movies, users, ratings

    movies_df = df[['tmdbId', 'title', 'poster', 'date_published', 'homepage']].drop_duplicates()
    movies = movies_df.to_dict(orient='records')
    

    users_df = df[['userId']].drop_duplicates()
    users = users_df.to_dict(orient='records')

    ratings_df = df[['userId', 'tmdbId', 'rating', 'timestamp']]
    ratings = ratings_df.to_dict(orient='records')

# Models
class Movie(BaseModel):
    tmdb_id: int
    title: str
    poster: str
    date_published: str
    homepage: str

class User(BaseModel):
    user_id: str

class Rating(BaseModel):
    user_id: str
    tmdb_id: int
    rating: float
    timestamp: int

# Load dữ liệu khi khởi động ứng dụng
@app.on_event("startup")
def startup_event():
    load_data()

# Endpoint: Lấy danh sách phim
@app.get("/movies")
def get_movies():
    return {"movies": movies}



# Endpoint: Thêm phim mới
@app.post("/add_movie")
def add_movie(movie: Movie):
    if any(m['tmdbId'] == movie.tmdb_id for m in movies):
        raise HTTPException(status_code=400, detail="Movie already exists")
    movies.append(movie.dict())
    return {"message": "Movie added successfully"}

# Endpoint: Lấy danh sách người dùng
@app.get("/users")
def get_users():
    return {"users": users}

# Endpoint: Thêm người dùng mới
@app.post("/add_user")
def add_user(user: User):
    if any(u['userId'] == user.user_id for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    users.append(user.dict())
    return {"message": "User added successfully"}

# Endpoint: Thêm đánh giá
@app.post("/add_rating")
def add_rating(rating: Rating):
    if not any(u['userId'] == rating.user_id for u in users):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    if not any(m['tmdbId'] == rating.movie_id for m in movies):
        raise HTTPException(status_code=400, detail="Invalid movie ID")
    ratings.append(rating.dict())
    return {"message": "Rating added successfully"}

# Endpoint: Lấy gợi ý phim dựa trên tần suất
@app.get("/recommendation/{user_id}")
def recommend_movies(user_id: str):
    if not any(u['userId'] == user_id for u in users):
        raise HTTPException(status_code=404, detail="User not found")

    # Tìm tần suất các phim được đánh giá cao
    user_movies = [r['movie_id'] for r in ratings if r['user_id'] == user_id]
    movie_frequency = {}
    for rating in ratings:
        if rating['movie_id'] not in user_movies:
            movie_frequency[rating['movie_id']] = movie_frequency.get(rating['movie_id'], 0) + 1

    # Sắp xếp theo tần suất
    recommendations = sorted(movie_frequency.items(), key=lambda x: x[1], reverse=True)
    recommended_movies = [movie for movie in movies if movie['tmdbId'] in [movie_id for movie_id, _ in recommendations]]
    
    return {"recommendations": recommended_movies}

# Chạy server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
