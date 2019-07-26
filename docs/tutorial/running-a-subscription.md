---
id: running-a-subscription
title: Running a subscription
sidebar_label: 10. Running a subscription
---

The `subscription` will bring real-time capabilities to your applications, and a feeling of reactivity for your clients.

Open your favorite browser at this URL [http://localhost:8080/graphiql](http://localhost:8080/graphiql) and execute the following request.

The response will be auto-updated after each message it receives.

## Subscribe to the cooking timer

This fabulous feature will start the countdown based on the `cookingTime` property of the targeted recipe:
```graphql
subscription {
  launchAndWaitCookingTimer(id: 1) {
    remainingTime
    status
  }
}
```

![Subscribe to the cooking timer](/docs/assets/subscription.gif)
