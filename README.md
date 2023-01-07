# DRF Authentication with JWT

Project description: Django REST framework authentication with JWT demo

# Installation of Dependencies

```shell
    pip install -r requirements-dev.txt
```

# User Guide

First of all we need to create a superuser with a standard Django command

```shell
    python manage.py createsuperuser
```

## How to start a development server ?

```shell
    python manage.py runserver
```

## How to start a development server with HTTPS support?

In the Django project root directory create a directory **development_certificates**.

```shell
    python manage.py runserver_plus --cert-file development_certificates/cert.crt
```

## Unit Tests

Pytest package was  used for unit testing.

Execute unit tests:

```shell
    pytest -v
```

## API Endpoints

### 0. API Schema

```text
    1.1. API Schema: GET /api/v1/swagger/ui/
    
    Description: Displays a web page with API Swagger specification. In order to try the endpoints an access token
    is needed. Type into the form: Bearer Access_Token_Value
    
    Example: Suppose that the value of your access token is 'MyAccessToken123', then you need to enter into
    the form: Bearer MyAccessToken123
    
    Success Status Code: 200 OK
```

### 1. Authentication Endpoints

```text
    1.1. User Authentication: POST /api/v1/auth/token/
    
    Description: User sends **username** and **password** in the request body, and gets a pair of tokens in return: 
    the **access token** and the **refresh token**.
    
    Request Body Template:
    {
        "username": "existing_name",
        "password": "existing_password"
    }
    
    Success Status Code: 200 OK
```

```text
    1.2. Access Token Refresh: POST /api/v1/auth/token/refresh/

    Description: User sends a refresh token in the request body, and gets in return a new access token.
    
    Request Body Template:
    {
        "refresh": "refresh_token_value"
    }
    
    Success Status Code: 200 OK
``` 
 
```text
    1.3. Logout: POST /api/v1/auth/logout/
   
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    Description: This request deactivates the refresh token.
   
    Add into request body the refresh token:
    {
        "refresh": "refresh_token_value"
    }
    
    Success Status Code: 200 OK
```

```text
    1.4. Logout All User Devices: GET /api/v1/auth/logout_all/    
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    Description: The request disables the refresh tokens for all active user devices.
    
    Success Status Code: 205 Reset Content
```

### 2. API Welcome View

```text
    2.1. API Welcome View: GET /api/v1/
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    Description: This is an API ping point, it allows to check if the API is working. Only authenticated users can 
    access this endpoint. In case of successful authentication you will get the following response:
    
    {
        "name": "My Awesome API",
        "api_version": "v1",
        "message": "Welcome!"
    }
    
    Success Status Code: 200 OK
```

### 3. Account Management Endpoints

```text
    3.1. Personal Account Data: GET /api/v1/account/
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    Description: Shows user personal account data.
    
    Success Status Code: 200 OK
```

```text
    3.2. List of User Accounts: GET /api/v1/account/management/
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    !!! Special permissions required !!!
    Only staff user can list user accounts.
    
    Description: Shows user account list with account data.
    
    Success Status Code: 200 OK
```

```text
    3.3. Create User Account: POST /api/v1/account/management/create/
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    !!! Special permissions required !!!
    Only Super User can create a new user account.
    
    Description: Creates new user account.
    
    Success Status Code: 201 Created
```

```text
    3.4. Show User Account with Specified User ID: GET /api/v1/account/management/<int:id>/
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    !!! Special permissions required !!!
    Only staff user can list user accounts.
    
    Description: Shows user account with specified user ID. 
    
    Success Status Code: 200 OK
```

```text
    3.5. Update User Account with Specified User ID: GET /api/v1/account/management/<int:id>/update/
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    !!! Special permissions required !!!
    Only super user can update user accounts.
    
    Description: Updates user account with specified user ID. 
    
    Success Status Code: 200 OK
```

```text
    3.6. Delete User Account with Specified User ID: DELETE /api/v1/account/management/<int:id>/delete/
    
    !!! This request requires AUTHORIZATION !!! 
    Add into request headers:
    Authorization: Bearer access_token_value
    
    !!! Special permissions required !!!
    Only super user can delete user accounts.
    
    Description: Deletes user account with specified user ID. 
    
    Success Status Code: 204 No Content
```