### Analyzer 
[![Build Status](https://travis-ci.com/63phc/analyzer.svg?branch=master)](https://travis-ci.com/63phc/analyzer)
#### Run analyzer

```bash
git clone https://github.com/63phc/analyzer.git
cd analyzer/analyzer
python run.py <REPO> -b <BRANCH> -s <DATE> -u <DATE>
#  EXAMPLE
python run.py 63phc/lks -b develop -s 2018-10-10 -u 2018-11-11
#  EXAMPLE
python run.py https://github.com/63phc/lks --branch=develop --since=2018-10-10 --until=2018-11-11
```

#### Limited request
- Tokens you have generated that can be used to access the GitHub API.
https://github.com/settings/tokens 
- Write token in .env file
```bash
touch .env
nano .env
# EXAMPLE token 
cp .env.example .env
```

#### Structure

- [analyzer.py](analyzer/analyzer.py) 
- [api.py](analyzer/api.py)
- [conf.py](analyzer/conf.py)
- [model.py](analyzer/model.py)
- [run.py](analyzer/run.py)
- [app.py](app.py) 

#### Local run flask api

```bash
pip install -r requirements.txt
python app.py
curl http://0.0.0.0:5000?repo='<REPO>'&branch='<BRANCH>'&since='<DATE>'&until='<DATE>'
#  EXAMPLE
curl http://0.0.0.0:5000?repo='63phc/lks'&branch='develop'&since='2018-10-10'&until='2018-11-11'
```

#### Docker run analyzer

```bash
docker build -t analyzer .
#  EXAMPLE
docker run -p 8000:8000 --rm -it analyzer
curl http://0.0.0.0:8000?repo='63phc/lks'&branch='develop'&since='2018-10-10'&until='2018-11-11'
```
