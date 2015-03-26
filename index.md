---
layout: default
---

# API endpoints
This page gives an overview of the endpoints of our fitness API back-end.


### Users

{% assign url = "/users/" %}

###### GET {{ url }}

Returns a list of all users.

```javascript
{
    "users": [
        {
            "id": 1,
            "nickname": "John"
        },
        {
            "id": 2,
            "nickname": "Jane"
        }
    ]
}
```

###### POST {{ url }}

Creates a new user with the given name. Returns the new user's id and HTTP status 201 if successful.

Send:

```javascript
name: John
```

Returns:

```javascript
1
```

{% assign url = "/users/\<int:id\>" %}

###### GET {{ url }}

Returns the details of one user.

```javascript
{
  "id": 1,
  "nickname": "John"
}
```

###### PUT {{ url }}

Updates the details of a specific user, or creates a new user if it did not exist. Returns HTTP status 204 if update successful, or returns the new user's id if user created.

Send:

```javascript
name: Jane
```
Returns:

```javascript
1
```

###### DELETE {{ url }}

Deletes a specific user. Returns HTTP status 204 if successful or HTTP status 404 if user did not exist.


### Measurements

{% assign url = "/measurements/" %}


###### GET {{ url }}

Returns a list of all measurements.

```javascript
{
  "measurements": [
    {
      "heart_rate": 70,
      "id": 1,
      "timestamp": "Wed, 25 Mar 2015 17:12:49 GMT",
      "user_id": 2
    },
    {
      "heart_rate": 84,
      "id": 2,
      "timestamp": "Wed, 25 Mar 2015 17:12:56 GMT",
      "user_id": 3
    },
    {
      "heart_rate": 64,
      "id": 3,
      "timestamp": "Wed, 25 Mar 2015 17:12:59 GMT",
      "user_id": 2
    }
  ]
}
```

###### POST {{ url }}

Creates a new measurement. Returns the new measurement's id and HTTP status 201 if successful. The server generates an id and a timestamp for the measurement.

Send:

```javascript
"heart_rate": 64,
"user_id": 2
```

Returns:

```javascript
4
```
