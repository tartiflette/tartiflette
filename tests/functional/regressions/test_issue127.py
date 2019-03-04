import pytest

from tartiflette import Engine, Resolver

_SDL = """
input RecipeInput {
  id: Int
  name: String
  cookingTime: Int
}

input CreateRecipeInput{
    id: Int
    name: String
    cookingTime: Int
    ingredients: [String]
}

type Recipe{
    id: Int
    name: String
    cookingTime: Int
    ingredients: [String]
}

type Mutation {
  updateRecipe(input: RecipeInput): Recipe
  deleteRecipe(input: ABigInputObject): ABigObject
  createRecipe(input: CreateRecipeInput): Recipe
}

type ABigObject {
    lol: Recipe
}

input ABigInputObject {
    lol: RecipeInput
}

type Query {
    recipe: Recipe
}

"""


@Resolver("Mutation.updateRecipe", schema_name="test_issue127")
@Resolver("Mutation.deleteRecipe", schema_name="test_issue127")
@Resolver("Mutation.createRecipe", schema_name="test_issue127")
async def update_recipe(_, args, *__, **kwargs):
    return args["input"]


_ENGINE = Engine(_SDL, schema_name="test_issue127")


@pytest.mark.parametrize(
    "query,variables,expected",
    [
        (
            """
            mutation($lol: Int) {
                updateRecipe(input: {
                        id: 1,
                        name: "The best Tartiflette by Eric Guelpa",
                        cookingTime: $lol
                }) {
                    id
                    name
                    cookingTime
                }
            }
            """,
            {"lol": 20},
            {
                "data": {
                    "updateRecipe": {
                        "id": 1,
                        "name": "The best Tartiflette by Eric Guelpa",
                        "cookingTime": 20,
                    }
                }
            },
        ),
        (
            """mutation($lol: Int) {
                deleteRecipe(input: {
                    lol: {
                        id: 1,
                        name: "The best Tartiflette by Eric Guelpa",
                        cookingTime: $lol
                }}){
                    lol {
                        id
                        name
                        cookingTime
                    }
                }
            }""",
            {"lol": 4896},
            {
                "data": {
                    "deleteRecipe": {
                        "lol": {
                            "id": 1,
                            "name": "The best Tartiflette by Eric Guelpa",
                            "cookingTime": 4896,
                        }
                    }
                }
            },
        ),
        (
            """
            mutation($lol: Int) {
                createRecipe(input: {
                        id: 1,
                        name: "The best Tartiflette by Eric Guelpa",
                        cookingTime: $lol,
                        ingredients: ["A Salad", "A Tea"]
                }) {
                    id
                    name
                    cookingTime
                    ingredients
                }
            }
            """,
            {"lol": 20},
            {
                "data": {
                    "createRecipe": {
                        "id": 1,
                        "name": "The best Tartiflette by Eric Guelpa",
                        "cookingTime": 20,
                        "ingredients": ["A Salad", "A Tea"],
                    }
                }
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_issue127(query, variables, expected):
    assert await _ENGINE.execute(query, variables=variables) == expected
