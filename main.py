# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
from typing import List

import pandas as pd
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from util import gql_flatten

load_dotenv()

# Setup GraphQL
headers = {"Authorization": f"API-Key {os.environ['SPLASHBACK_API_KEY']}"}
transport = AIOHTTPTransport(url='https://api.splashback.io/graphql', headers=headers)
client = Client(transport=transport)


def get_samples(
        pool_id: str,
        site_ids: List[int],
        parameter_ids: List[int]
) -> pd.DataFrame:
    query = gql("""
      query($poolId: UUID!, $siteIds: [Int!]!, $parameterIds: [Int!]!) {
        samples(
            poolId: $poolId
            order: {dateTime: ASC}
            where: {
                siteId: { in: $siteIds }
                sampleVariants: {
                    some: {
                        sampleValues: {
                            some: {
                                parameterId: { in: $parameterIds } 
                            }
                        }
                    }
                }
            }
        ) {
          nodes {
            id dateTime
            site { id name }
            program { id name } 
            comments
            
            sampleVariants {
                sampleValues(where: { parameterId: { in: $parameterIds } }) {
                    parameter { id name }
                    qualifier value
                }
            }
          }
        }
      }
    """)
    variables = {
        'poolId': pool_id,
        'siteIds': site_ids,
        'parameterIds': parameter_ids
    }
    response = client.execute(query, variable_values=variables)
    data = gql_flatten('sample', response['samples']['nodes'])
    df = pd.DataFrame.from_records(data)
    return df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_samples = get_samples('00000000-0000-0000-0000-000000001004',
                             site_ids=[52], parameter_ids=[55, 56])
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
