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

Returns a list of all measurements, sorted from most to least recent. Optional filter parameters are:

- user_id:int - Only retrieve measurements from a specific user.
- max:int - Limits the number of retrieved measurements (i.e. the x most recent measurements are retrieved).
- from:string - Only measurements registered after this time are retrieved. The format is: `yyyymmddhhmmssfff`, e.g. 20150522181130000.
- until:string - Only measurements registered before this time are retrieved. Format is the same as for from.
- exercise_id:int - Only measurements that belong to a specific exercise are retrieved.

```javascript
{
  "measurements": [
    {
      "heart_rate": 70,
      "id": 1,
      "timestamp": "20150522181137759",
      "user_id": 2
    },
    {
      "heart_rate": 84,
      "id": 2,
      "timestamp": "20150522181131145",
      "user_id": 3
    },
    {
      "heart_rate": 64,
      "id": 3,
      "timestamp": "20150522181130000",
      "user_id": 2
    }
  ]
}
```

Sending the following filter parameters:

```javascript
"user_id": 2
"max": 1
"from": "20150522181137759"
```

Returns one measurement from user 2, registered after March 1st 2015 at midnight if such a measurement exists.


###### POST {{ url }}

Creates one or more new measurements. Returns HTTP status 201 if successful. The server generates id's for the measurements. The server also generates a timestamp for each measurement that does not have one.

Send:

```javascript
{
    "measurements": [
        {
            "heart_rate": 64,
            "user_id": 2
        },
        {
            "heart_rate": 80,
            "user_id": 5,
            "timestamp": 20150522181137000
        },
        {
            "heart_rate": 77,
            "user_id": 2
        }
    ]
}
```

### Exercises

{% assign url = "/exercises/" %}

###### GET {{ url }}

Returns a list of all recorded exercises.

```javascript
{
  "exercises": [
    {
      "avg_heart_rate": 63,
      "end": "20150522181137000",
      "id": 1,
      "start": "20150418181137000",
      "type": "walking",
      "user_id": 0
    },
    {
      "avg_heart_rate": 89,
      "end": "20150418181137000",
      "id": 2,
      "start": "20150418121137000",
      "type": "sleeping",
      "user_id": 0
    },  
    {
      "avg_heart_rate": 78,
      "end": "20150418181137000",
      "id": 3,
      "start": "20150418111137000",
      "type": "fishing",
      "user_id": 1
    }
  ]
}
```

###### POST {{ url }}

Creates a new exercise with the given name. Returns the new exercise's id and HTTP status 201 if successful.

Send:

```javascript
user_id : int   the id of the user exercising
type    : str   the activity type. i.e. ice hockey
start   : int   the start time of the exercise in format yyyymmddhhmmssfff
end     : int   the end time of the exerciss in format yyyymmddhhmmssfff
```

Returns the id of the created exercise

```javascript
1
```

{% assign url = "/exercises/\<int:id\>" %}

###### GET {{ url }}

Returns data for the specific exercise.

```javascript
{
  "avg_heart_rate": null,
  "end": "20150522181130000",
  "id": 18,
  "start": "20150522181130000",
  "type": "fishing",
  "user_id": 1
}
```


###### DELETE {{ url }}

Deletes a specific exercise. Returns HTTP status 204 if successful or HTTP status 404 if user did not exist.
