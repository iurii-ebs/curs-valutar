define({ "api": [
  {
    "type": "get",
    "url": "/users/activate-done/",
    "title": "Request activate-done page",
    "name": "ActivateDoneView",
    "group": "UserActivation",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserActivation"
  },
  {
    "type": "get",
    "url": "/users/activate/encoded_uid/token",
    "title": "Request user activation",
    "name": "ActivateView",
    "group": "UserActivation",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserActivation"
  },
  {
    "type": "get",
    "url": "/users/password-change-done/",
    "title": "Request password-change-done page",
    "name": "PasswordChangeDoneView",
    "group": "UserPasswordChange",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserPasswordChange"
  },
  {
    "type": "get",
    "url": "/users/password-change/uid_encoded/token",
    "title": "Request password change page",
    "name": "PasswordChangeView",
    "group": "UserPasswordChange",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserPasswordChange"
  },
  {
    "type": "get",
    "url": "/users/password-reset-done/",
    "title": "Request password-reset-done page",
    "name": "PasswordResetDoneView",
    "group": "UserPasswordReset",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserPasswordReset"
  },
  {
    "type": "get",
    "url": "/users/password-reset/",
    "title": "Request password reset",
    "name": "PasswordResetView",
    "group": "UserPasswordReset",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserPasswordReset"
  },
  {
    "type": "post",
    "url": "/users/password-reset/",
    "title": "Confirm password reset",
    "name": "PasswordResetView",
    "group": "UserPasswordReset",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>User's email.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserPasswordReset"
  },
  {
    "type": "get",
    "url": "/users/register-done/",
    "title": "Request register-done page",
    "name": "RegisterDoneView",
    "group": "UserRegistration",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserRegistration"
  },
  {
    "type": "get",
    "url": "/users/register/",
    "title": "Request registration page",
    "name": "RegisterView",
    "group": "UserRegistration",
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserRegistration"
  },
  {
    "type": "post",
    "url": "/users/register/",
    "title": "Request user registration",
    "name": "RegisterView",
    "group": "UserRegistration",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "first_name",
            "description": "<p>User's first_name.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "last_name",
            "description": "<p>User's last_name.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>User's email.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>User's username.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>User's password.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "redirect",
            "description": "<p>to /users/register-done/</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "UserRegistration"
  },
  {
    "type": "post",
    "url": "/users/password-change/uid_encoded/token",
    "title": "Request password change page",
    "name": "PasswordChangeView",
    "group": "Users",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password1",
            "description": "<p>User's new password.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password2",
            "description": "<p>User's new password confirm.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "apps/users/views.py",
    "groupTitle": "Users"
  },
  {
    "type": "post",
    "url": "/wallets/:id/transactions/",
    "title": "Post Wallets Transactions",
    "name": "PostTransactions",
    "group": "Wallets",
    "description": "<p>Post transactions in the user wallet</p>",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Content-Type",
            "defaultValue": "application/json",
            "description": ""
          },
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "Authorization",
            "defaultValue": "Bearer <JWT token>",
            "description": ""
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "amount",
            "description": "<p>Transaction amount (can be negative).</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": false,
            "field": "currency",
            "description": "<p>Currency id to transfer.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "JSON",
            "optional": false,
            "field": "object",
            "description": "<p>containing status as success and object message</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success Response (Example):",
          "content": "{\n    \"id\": 11,\n    \"wallet\": {\n        \"id\": 1,\n        \"user\": 1,\n        \"currency\": 1,\n        \"balance\": 228309,\n        \"value_buy\": 4085856.9,\n        \"value_sell\": 4018238.4,\n        \"profit\": -67618.5\n    },\n    \"amount\": 1111,\n    \"currency\": 1,\n    \"rate\": 7\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "JSON",
            "optional": false,
            "field": "object",
            "description": "<p>containing status as failed and error message</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error Response (Example):",
          "content": "{\n\"detail\": \"The target wallet is not of the same currency. Please use a different wallet.\"\n}",
          "type": "json"
        }
      ]
    },
    "sampleRequest": [
      {
        "url": "http://127.0.0.1:8000/wallets/1/transactions/"
      }
    ],
    "version": "0.0.0",
    "filename": "apps/wallet/views.py",
    "groupTitle": "Wallets"
  }
] });
