FROM continuumio/miniconda3

WORKDIR /home/pythings/

RUN conda install -c conda-forge wordcloud streamlit
RUN conda install -c conda-forge nltk
RUN python -c 'import nltk; nltk.download("punkt")'
RUN python -c 'import nltk; nltk.download("stopwords")'


COPY . ./
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["./nyt_streamlit.py"]


# docker image build -t nyt .
# docker run --rm -p 8501:8501 nyt
