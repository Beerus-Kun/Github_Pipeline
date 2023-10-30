import os

CONFIG_FILE = "configs/data_extraction.json"
API_URL = "https://api.github.com/graphql"
GITHUB_HEADER = {"Authorization": f"Bearer {os.getenv('github_token')}"}
BUCKET="github-datalake"
DYNAMODB_TABLE = "github"
DYNAMODB_ITEM = "AWS_stepfunction"
PARQUET_EXTENSION = ".parquet"
S3_FOLDER = "github"

ORGANIZATION_QUERY ="""
query {
  organization(login: "__organization_name__") {
   announcement
    createdAt
    description
    email
    name
    websiteUrl
    id
    location
    url
  }
}
"""

REPOSITORY_QUERY = """
query {
  organization(login: "__organization_name__") {
    repositories(first: 10, __cursor__) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        id
        createdAt
        name
        description
        url
      }
    }
  }
}
"""

LANGUAGE_QUERY = """
query {
    node(id: "__repository_id__") {
    ...on Repository{
      languages(first: 20, __cursor__){
        nodes{
          name
          id
          color
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
"""

PULL_REQUEST_QUERY = """
query {
    node(id: "__repository_id__") {
    ...on Repository{
        pullRequests(first: 5, __cursor__){
          pageInfo{
            endCursor
            hasNextPage
          }
          nodes{
            body
            createdAt
            viewerSubscription
            id
          }
        }
      
    }
  }
}
"""

BRANCH_QUERY ="""
query {
  node(id: "__repository_id__") {
    ... on Repository {
      refs(refPrefix: "refs/heads/", first: 1, __branch_cursor__) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          name
          id
        }
      }
    }
  }
}
"""

COMMIT_QUERY = """
query {
  node(id: "__repository_id__") {
    ... on Repository {
      refs(refPrefix: "refs/heads/", first: 1, __branch_cursor__) {
        nodes {
          target {
            ... on Commit {
              history(first: 10, __commit_cursor__) {
                pageInfo {
                  hasNextPage
                  endCursor
                }
                nodes {
                  author {
                    name
                  }
                  message
                  committedDate
                  id
                }
              }
            }
          }
        }
      }
    }
  }
}
"""