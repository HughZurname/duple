# Welcome

## Duple

_(/ˈdjuːp(ə)l/) ~ based on two main beats to the bar._

---

A little preamble... The proejct has been given a name because working on something called tech-test is kind of boring `¯\_(ツ)_/¯`. Initially the project used brute force methods like tf-idf, edit distance and metaphone for the matching algorithm, the results were relatively poor however. I found a libary provided by [dedupe.io](https://docs.dedupe.io/en/latest/) which uses a mixture of different matching predicates like those mentioned above along with Regularized Logistic Regression to train a matching model with reinforcement learning. The training phase takes a little bit of time but the model tends to generalise well to other datasets of a similar structure _(I tested this by generating some of my own random duplicates)_

The A/C in the tech-test were pretty much satisfied by combining dedupe with pandas, this can be found in `duple-api/duple/console.py` and can be run with `python -m duple -c -f profile-data/DataShed_Technical_Test.csv` from within the duple-api folder. It will output a file called `relateddata.csv` where you run the command from. I have supplied this with a pretrained model, but if you would like to test the training pahse of the console labeler you can just change the `settings_file` as seen below.

```
def deduplicate(
    df,
    recall_weight=1,
    sample_size=0.3,
    settings_file="training-data/test_dedupe_learned_settings",
    training_file="training-data/test_dedupe_training.json",
)
```

Because this seemed like a fun project, I decided to take things a little further and build a fronted and backing service for performing the training and deduplication phases. More detail follows below.

---

## Running

The instructions for running each of the projects can be found in the `README.md` in the root of thier subdirectories. Alternatively a docker-compose.yaml has been supplied and can be run with `docker-compose -f "docker-compose.yaml" up -d --build` the client can be accessed via `localhost:5000` and the api on `localhost:8080`

## Structure

This project is broken in to two main sections:

- `duple-api` contains
  - the original console app that meets the A/C for the tech-test
  - the main deduplication service that supports the frontend client
- `duple-client` contains
  - the react frontend client for training and deduplication

_Both projects have a relatively flat structure which hopefully makes navigating the project simpler._

## Concepts

## Rationale

## Testing

## Known/Potential Issues
