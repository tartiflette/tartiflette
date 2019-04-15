workflow "build and release" {
  on = "push"
  resolves = ["release"]
}

action "build docker image" {
  uses = "actions/docker/cli@master"
  args = "build -t tartiflette ."
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

action "build and publish to pypi" {
  uses = "./github-actions/pypi/"
  secrets = ["TWINE_PASSWORD", "TWINE_USERNAME"]
  needs = ["unit test", "functional test", "style"]
}

action "is master" {
  uses = "actions/bin/filter@master"
  needs = ["build and publish to pypi"]
  args = "branch master"
}

action "is ref master" {
  uses = "./github-actions/shell/"
  needs = ["is master"]
  runs = "is_ref"
  env = {
    REF_NAME = "refs/heads/master"
  }
}

action "set version and changelog" {
  uses = "./github-actions/shell/"
  needs = ["is ref master"]
  runs = "make"
  args = "github-action-version-and-changelog"
}

action "release" {
  uses = "./github-actions/release/"
  secrets = ["GITHUB_TOKEN"]
  needs = ["set version and changelog"]
  env = {
    USERNAME = "dailymotion"
    REPOSITORY = "tartiflette"
  }
}
