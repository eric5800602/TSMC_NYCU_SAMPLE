FROM python:3.6.15-slim
COPY . /sample_crawler
WORKDIR /sample_crawler
EXPOSE 8080/tcp
EXPOSE 8080/udp
RUN pip install -r ./requirements.txt
RUN python -c "import nltk;nltk.download('corpus')"
RUN python -c "import nltk;nltk.download('tokenize')"
RUN python -c "import nltk;nltk.download('stopwords')"
RUN python -c "import nltk;nltk.download('word_tokenize')"
RUN python -c "import nltk;nltk.download('punkt')"
CMD ["python","crawler_sample.py"]
