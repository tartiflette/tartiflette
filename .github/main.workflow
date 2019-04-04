workflow "build and release" {
  on = "push"
  resolves = ["release"]
}

action "display github event" {
  uses = "./github-actions/shell/"
  runs = "cat"
  args = "/github/workflow/event.json"
}

action "build docker image" {
  uses = "actions/docker/cli@master"
  args = "build -t tartiflette ."
}

action "build artifact" {
  uses = "./github-actions/python/"
  runs = "make"
  args = "build-artifact"
}

action "unit test" {
  needs = ["build docker image"]
  uses = "actions/docker/cli@master"
  args = "run -i tartiflette make test-unit"
}

action "functional test" {
  needs = ["build docker image"]
  uses = "actions/docker/cli@master"
  args = "run -i tartiflette make test-functional"
}

action "style" {
  needs = ["build docker image"]
  uses = "actions/docker/cli@master"
  args = "run -i tartiflette make style"
}

action "set version and changelog" {
  uses = "./github-actions/shell/"
  needs = ["unit test", "functional test", "style", "build artifact", "display github event"]
  runs = "make"
  args = "github-action-version-and-changelog"
}

action "is master" {
  uses = "actions/bin/filter@master"
  needs = ["set version and changelog"]
  args = "branch master"
}

action "publish to pypi" {
  uses = "./github-actions/pypi/"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  needs = ["is master"]
}

action "release" {
  uses = "./github-actions/release/"
  secrets = ["GITHUB_TOKEN"]
  needs = ["publish to pypi"]
  env = {
    USERNAME = "dailymotion"
    REPOSITORY = "tartiflette"
  }
}
