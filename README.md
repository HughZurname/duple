# Welcome

## Duple

_(/ˈdjuːp(ə)l/) ~ based on two main beats to the bar._

The proejct has been given a name because working on something called tech-test is kind of boring `¯\_(ツ)_/¯`.

---

## Why

The criteria for the tech test were very open ended, so once I had implemented an MVP (the console app) I had some fun and built something that was maybe _a tiny bit_ exta.

Initially the project used brute force methods like tf-idf, edit distance and metaphone for the matching algorithm, the results were relatively poor however. However the libary provided by [dedupe.io](https://docs.dedupe.io/en/latest/) which uses a combination of different matching predicates like those mentioned above along with Regularized Logistic Regression to train a matching model with reinforcement learning. The training phase takes a little bit of time but the model tends to generalise well to other datasets of a similar structure _(I tested this by generating some of my own random duplicates)_. It finds duplicate data fairly quickly once a model is trained, using the 11k row example data finds a result of ~950 duplicates in a few seconds.

Because this seemed like a fun project, I decided to take things a little further than the console app entioned below, and build a fronted with a backing service for performing the training and deduplication phases. In hindsight this was perhaps a little over ambitious and I didn't manage to get everything I would have liked to in the time.

---

## Console App

The A/C in the tech-test were minimally satisfied by combining dedupe with [pandas](https://pandas.pydata.org), this can be found in `duple-api/duple/console.py` and can be run with `python -m duple -c -f profile-data/DataShed_Technical_Test.csv` from within the duple-api folder. It will output a file called `relateddata.csv` with a count of the duplicates as a log message. where you run the command from. I have supplied this with a pretrained model, but if you would like to test the training phase of the console labeler you can just change the `settings_file` as seen below.

```python
def deduplicate(
    df,
    recall_weight=1,
    sample_size=0.3,
    settings_file="training-data/test_dedupe_learned_settings",
    training_file="training-data/test_dedupe_training.json",
)
```

---

## Running

The instructions for running each of the projects can be found in the `README.md` in the root of thier subdirectories. Alternatively a docker-compose.yaml has been supplied and can be run with `docker-compose up -d --build` the client can be accessed via `localhost:5000` and the api on `localhost:8080`. Swagger docs are vailible for the api on
`localhost:8080/doc/api`

## Testing

As the project contains components implemented in different languages the testing methods are specific to those, therefore the instrucions for them can be found in thier respective sub directories.

The `test-e2e` folder contains an automated test using [taiko](https://taiko.gauge.org/) and [gauge](https://gauge.org/)

## Structure

This project is broken in to two main sections:

- `duple-api` contains
  - the original console app that meets the A/C for the tech-test
  - the main deduplication service that supports the frontend client
- `duple-client` contains
  - the react frontend client for training and deduplication

_Both projects have a relatively flat structure which hopefully makes navigating the project simpler._

## Design

_An architecture diagram was supposed ot go here but again I ran out of time_, however the general idea is that a react client connects to a python backend running deduplication tasks by scheduling them on to a message queue and notifying the client of completion (this was supposed to use server push).

## Known/potential issues

- Very large files will need to be deduplicated in chunks, the backend currently makes use of `Dedupe().match` which according to [this section of the docs](https://docs.dedupe.io/en/latest/API-documentation.html#Dedupe.match) should only be used for relatively small datasets. In testing it is fine with anything up to around 30k rows.

- It is recomended that you carry out subsequent tests in a new session (i.e. open a new tab in chrome etc.) the caching can be a little agressive in some scenarios and needs refinement.

## What could/should still be done

- Testing! I thought I'd give myself more time to finish this.
  - The api has better documentation and testing
  - The frontend client was seen as an 'extra' so could do with some docs and better testing.
- SSL and perhaps some kind of client auth.
- Chunked matching with dedupe to allow scaling to larger datasets.
- A better Pub/Sub mechanism (maybe rabbitmq/kafka) handrolling something simple was easier here.
- An actual document datastore (maybe mongo) but again an in memory python object sufficed here.
