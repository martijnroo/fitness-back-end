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
- from:string - Only measurements registered after this time are retrieved. The format is: `yyyymmddhhss`, e.g. 201504021340.
- until:string - Only measurements registered before this time are retrieved. Format is the same as for from.
- exercise_id:int - Only measurements that belong to a specific exercise are retrieved.

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

Sending the following filter parameters:

```javascript
"user_id": 2
"max": 1
"from": 20150301000000
```

Returns one measurement from user 2, registered after March 1st 2015 at midnight if such a measurement exists.


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

### Exercises

{% assign url = "/exercises/" %}

###### GET {{ url }}

Returns a list of all recorded exercises.

```javascript
{
  "exercises": [
    {
      "avg_heart_rate": 63, 
      "end": "Fri, 03 Apr 2015 05:09:53 GMT", 
      "id": 1, 
      "start": "Thu, 02 Apr 2015 23:39:49 GMT", 
      "type": "walking", 
      "user_id": 0
    }, 
    {
      "avg_heart_rate": 89, 
      "end": "Fri, 03 Apr 2015 10:44:37 GMT", 
      "id": 2, 
      "start": "Fri, 03 Apr 2015 10:28:18 GMT", 
      "type": "sleeping", 
      "user_id": 0
    },  
    {
      "avg_heart_rate": 78, 
      "end": "Thu, 30 Apr 2015 12:45:00 GMT", 
      "id": 3, 
      "start": "Thu, 30 Apr 2015 12:30:00 GMT", 
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
start   : int   the start time of the exercise in format yyyymmddhhmmss
end     : int   the end time of the exerciss in format yyyymmddhhmmss
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
  "end": "Thu, 30 Apr 2015 12:45:00 GMT", 
  "id": 18, 
  "start": "Thu, 30 Apr 2015 12:30:00 GMT", 
  "type": "fishing", 
  "user_id": 1
}
```


###### DELETE {{ url }}

Deletes a specific exercise. Returns HTTP status 204 if successful or HTTP status 404 if user did not exist.

