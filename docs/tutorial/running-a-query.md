---
id: running-a-query
title: Running a query
sidebar_label: 6. Running a query
---

We are going to use what [we developed in the previous step](./write-your-resolvers.md).

To query the **Tartiflette recipes manager**, we will use the GraphiQL client which is embeded in `tartiflette-aiohttp` and available at this address [http://localhost:8080/graphiql](http://localhost:8080/graphiql) when your server is running.

## Get all the recipes

Copy/paste this GraphQL request to your GraphiQL instance and execute it:
```graphql
{
  recipes {
    id
    name
    cookingTime
  }
}
```

![All recipes](/docs/assets/query-all-recipes-v1.png)

## Get all the recipes with ingredients

The power of GraphQL is to be able to get many different resources in a single request.

We will execute a request to retrieve the recipes with all the ingredients:
```graphql
query {
  recipes {
    id
    name
    cookingTime
    ingredients {
      name
      quantity
      unitMeasurement
    }
  }
}
```

![All recipes with ingredients](/docs/assets/query-all-recipes-with-ingredients-v1.png)

## Get only one recipe

Below, a request to select only one recipe, by its `id`:
```graphql
{
  recipe(id: 1) {
    id
    name
    cookingTime
    ingredients {
      name
      quantity
      unitMeasurement
    }
  }
}
```

![Only one recipe](/docs/assets/query-one-recipe-v1.png)
