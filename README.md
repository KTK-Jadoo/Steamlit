# Steamlit

A recommendation system (or recommender system) is a class of machine learning that uses data to help predict, narrow down, and find what people are looking for among an exponentially growing number of options.

The AI algorithm implemented here takes the following into account:

1) Explicit feedback is a rating explicitly given by the user to express their satisfaction with an item. Examples are: number of stars on a scale from 1 to 5 given after buying a product, thumb up/down given after watching a video, etc. This feedback provides detailed information on how much a user liked an item, but it is hard to collect as most users typically don’t write reviews or give explicit ratings for each item they purchase.

2) Implicit feedback, on the other hand, assume that user-item interactions are an indication of preferences. Examples are: purchases/browsing history of a user, list of songs played by a user, etc. This feedback is extremely abundant, but at the same time it is less detailed and more noisy (e.g. someone may buy a product as a present for someone else). However, this noise becomes negligible when compared to the sheer size of available data of this kind, and most modern Recommender Systems tend to rely on implicit feedback.

Collaborative Filtering, Matrix factoring Model, Alternating Least Squares, Stochastic Gradient Descent, SVD. Light FM