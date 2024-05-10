#
#
from google.cloud import bigquery
from utils.list_scraper import eventList
import time
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_service_account_credentials.json"

def run_():
    client = bigquery.Client()
    query_string = """
        SELECT * FROM `project.db.table`
        """
    df_his = (
        client.query(query_string).result().to_dataframe(create_bqstorage_client=True)
    )
    lastsearch = df_his['name'][:9].values

    df_all = eventList(lastsearch=lastsearch).generate_list()
    df_sum = eventList(lastsearch=lastsearch).summary(dataframe=df_all)

    df_all.to_csv('/Users/mac/PycharmProjects/listCrawling/dataset/list_all.csv')
    df_sum.to_csv('/Users/mac/PycharmProjects/listCrawling/dataset/list_summary.csv')

if __name__ == "__main__":
    start_time = time.time()
    run_()
    print("Update completed in {:.2f} seconds".format(time.time() - start_time))


