# XGrapher

## What is XGrapher?

 A simple interface to directly push data into ONgDB and read data via ReST.
 

## Stack

- ONgDB
- Docker
- Poetry
- FastAPI
- Py2Neo

## Deployment

- Install python ^ 3.7
- Start `ONgDB` database (Optionally use ongdb.yml in docker folder)
- `poetry install`
- Run `run.py` or run `scripts\launch.sh` or run `docker-compose -f <docker-compose.yml> up -d`

## Capability

- Add nodes directly or using graph
    - endpoints = /api/v1/data/graph ,/api/v1/data, /api/v1/data/relation
```
{
  "graphs": [
    {
      "start": {
        "type": "Framework",
        "id_field": "name",
        "attributes": {
           "name" : "FastAPI"
         }
      },
      "through": {
        "type": "RELY_ON"
      },
      "reach": {
        "type": "Framework",
        "id_field": "name",
        "attributes": {
           "name" : "Pydantic"
         }
      }
    },
    {
        "through": {
        "type": "BASED_ON"
      },
      "reach": {
        "type": "Language",
        "id_field": "name",
        "attributes": {
           "name" : "Python",
           "tag" : "simple tag"
         }
      }
    }
  ]
}

```

- Query data based on graph
    - /api/v1/query/

```
{
    "traverse": [
        {
            "traverse_from": {
                "type": "Language",
                "alias": "n",
                "filter": {
                    "name": "Python"
                },
                "where": "n.tag = \"simple tag\""
            },
            "through": {
                "relation": "BASED_ON",
                "alias": "b"
            },
            "reach": {
                "type": "Framework",
                "alias": "f"
            }
        },
        {
            "through": {
                "relation": "RELY_ON",
                "alias": "r"
            },
            "reach": {
                "type": "Framework",
                "alias": "f2"
            }
        }

    ],
    "return_attributes": [
        "f2"
    ]
}


```

- Store parameterised native query and then run it later
    - /api/v1/query/store

```

Store
-------
Name: sample
Query: MATCH (language:Language{name : $language}) RETURN language LIMIT 25

Execution
----------
POST /api/v1/query/store?name=sample -d "{"language": "Python"}"

```