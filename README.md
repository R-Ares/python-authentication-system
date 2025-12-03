\# 🔐 Python Authentication System (Salted + Hashed Passwords)



A simple but secure authentication system written in Python.  

It supports \*\*registration, login, and user deletion\*\*, all using \*\*salted SHA-256 hashing\*\*, stored safely inside a `users.json` file.



This project was created to practice \*\*Cybersecurity fundamentals\*\*, secure password handling, and Python programming.



---



\## 🚀 Features



\### ✅ \*\*Register Users\*\*

\- Username must be unique  

\- Password is validated for:

&nbsp; - Minimum length: 8 characters  

&nbsp; - At least 1 uppercase letter  

&nbsp; - Not only digits  

\- Passwords are \*\*never stored in plain text\*\*



---



\### 🔐 \*\*Secure Password Storage\*\*

Passwords are stored as:

\- \*\*SHA-256 hash\*\*

\- \*\*Random 16-byte hex salt\*\*

\- Stored in `users.json` as:



```json

{

&nbsp;   "alex": {

&nbsp;       "hash": "f739e...",

&nbsp;       "salt": "b5823..."

&nbsp;   }

}



