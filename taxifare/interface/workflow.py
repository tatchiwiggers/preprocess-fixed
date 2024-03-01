from taxifare.interface.main import evaluate, preprocess, train
from prefect import task, flow

@task # task 1
def preprocess_new_data(min_date: str, max_date: str):
    # takes the dates as params for one month of data
    preprocess(min_date=min_date, max_date=max_date)

@task # task 2
def evaluate_production_model(min_date: str, max_date: str):
    eval_mae = evaluate(min_date=min_date, max_date=max_date)
    return eval_mae

@task # task 3
def re_train(min_date: str, max_date: str):
    # retrain te model on new data
    # updates the split ratio to take 20%of new month as a val set
    train_mae = train(min_date=min_date, max_date=max_date, split_ratio=0.2)
    return train_mae

@flow
def train_flow():
    min_date = "2015-01-01"
    max_date = "2015-02-01"
    processed = preprocess_new_data.submit(min_date, max_date)
    old_mae = evaluate_production_model.submit(min_date, max_date, wait_for=[processed])
    new_mae = re_train.submit(min_date, max_date, wait_for=[processed])

if __name__ == "__main__":
    train_flow()