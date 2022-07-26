# nyt -- New York Times WordClouds
A Streamlit webapp written in pure Python to provide visualizations of frequently used words in popular articles the New York Times according to user-given conditions (time frame, medium, etc.).

## Example
![Example of webapp output](/screenshot.png?raw=true "An example from July 2022")

## Instructions Docker:
```sh
docker image build -t nyt .
docker run --rm -p 8501:8501 nyt
```
