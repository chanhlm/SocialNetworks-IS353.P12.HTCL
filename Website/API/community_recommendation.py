# community_recommendation.py
import networkx as nx
import pandas as pd
from collections import Counter

def girvan_newman(graph, edges):
    # Detect communities using Girvan-Newman algorithm
    communities = list(nx.community.girvan_newman(graph))
    modularity_df = pd.DataFrame(
        [
            [k + 1, nx.community.modularity(graph, communities[k])]
            for k in range(len(communities))
        ],
        columns=["k", "modularity"],
    )
    best_k = (modularity_df.loc[modularity_df["modularity"].idxmax()]["k"]).astype(int)


    # Recommend popular movies within each community
    partition = {node: idx for idx, community in enumerate(communities[best_k - 1]) for node in community}

    user_movie_history = {}
    for user, movie in edges:
        if user not in user_movie_history:
            user_movie_history[user] = []
        user_movie_history[user].append(movie)

    community_recommendations = {}
    for community_id in set(partition.values()):
        community_members = [user for user, com_id in partition.items() if com_id == community_id]
        movie_counter = Counter()
        for user in community_members:
            movies = user_movie_history.get(user, [])
            movie_counter.update(movies)

        # Select top 5 popular movies within the community
        popular_movies = [movie for movie, _ in movie_counter.most_common(10)]
        community_recommendations[community_id] = popular_movies

    # Create user-specific recommendations
    user_recommendations = {}
    for user, community_id in partition.items():
        movies_watched = set(user_movie_history.get(user, []))
        recommendations = [movie for movie in community_recommendations[community_id] if movie not in movies_watched]
        user_recommendations[user] = recommendations

    return user_recommendations

def louvain(graph, edges):
    user_recommendations = {}

    return user_recommendations