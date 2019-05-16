import pytest

from tartiflette import Resolver, create_engine

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

enum IngredientQuality  {
    GOOD
    NOT_GOOD
    BAD
    NOT_BAD
    SOSO
}

input Ingredientrrrte {
    id: Int
    name: String
    type: String
    quality: IngredientQuality
    aListOfNumber: [Int]
}

type Ingredient {
    id: Int
    name: String
    type: String
    quality: IngredientQuality
    aListOfNumber: [Int]
}

input PatchRecipeInput {
    id: Int
    name: String
    cookingTime: Int
    ingredients: [Ingredientrrrte]
}

type ListObjectWithObject {
    id: Int
    name: String
    cookingTime: Int
    ingredients: [Ingredient]
}

type ABigObject {
    lol: Recipe
}

input ABigInputObject {
    lol: RecipeInput
}

type Mutation {
  updateRecipe(input: RecipeInput): Recipe
  deleteRecipe(input: ABigInputObject): ABigObject
  createRecipe(input: CreateRecipeInput): Recipe
  patchRecipe(input: PatchRecipeInput): ListObjectWithObject
}

type Query {
    recipe: Recipe
}
"""


@pytest.fixture(scope="module")
async def ttftt_engine():
    @Resolver("Mutation.updateRecipe", schema_name="test_issue127")
    @Resolver("Mutation.deleteRecipe", schema_name="test_issue127")
    @Resolver("Mutation.createRecipe", schema_name="test_issue127")
    @Resolver("Mutation.patchRecipe", schema_name="test_issue127")
    async def update_recipe(_, args, *__, **kwargs):
        return args["input"]

    return await create_engine(sdl=_SDL, schema_name="test_issue127")


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
        (
            """
            mutation {
                patchRecipe(
                    input: {
                        id: 5,
                        name: "THE REcipe",
                        cookingTime: 86,
                        ingredients: [
                            {
                                id: 6,
                                name: "A Salad",
                                type: "HEALTHY",
                                quality: SOSO,
                                aListOfNumber: [5,63,98],
                            },
                            {
                                id: 9,
                                name: "A Tea",
                                type: "GREASY",
                                quality: NOT_GOOD,
                                aListOfNumber: [121,987,9632],
                            }
                        ]
                    }
                ) {
                    id
                    name
                    cookingTime
                    ingredients {
                        id
                        name
                        type
                        quality
                        aListOfNumber
                    }
                }
            }
            """,
            {},
            {
                "data": {
                    "patchRecipe": {
                        "id": 5,
                        "name": "THE REcipe",
                        "cookingTime": 86,
                        "ingredients": [
                            {
                                "id": 6,
                                "name": "A Salad",
                                "type": "HEALTHY",
                                "quality": "SOSO",
                                "aListOfNumber": [5, 63, 98],
                            },
                            {
                                "id": 9,
                                "name": "A Tea",
                                "type": "GREASY",
                                "quality": "NOT_GOOD",
                                "aListOfNumber": [121, 987, 9632],
                            },
                        ],
                    }
                }
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_issue127(query, variables, expected, ttftt_engine):
    assert await ttftt_engine.execute(query, variables=variables) == expected
