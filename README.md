<!-- README.md is generated from README.Rmd. Please edit that file -->

# filast

With the **filast** package, any **Python** user can fill in missing emails in their CRM. 

Emails are compsed of two parts: a username, and a domain. 

<img src="images/email_parts.PNG" height="120px" />

There are free email domains like gmail.com or aol.com, and company domains like oracle.com or toshiba.com.

The usernames with free email domains are very unrestricted. For example, John Smith could chose to make his email jsmith@gmail.com or j.smith88@gmail.com. Whereas, at company's it is common practice to issue employees email addresses with the same username syntax. That's what makes them predictable.

The majority of company email usernames are composed of a combination of some the following:
* first name
* last name
* first initial
* last initial
* dot
* underscore

The most common combination is first initial + last name; or **filast** (hence the name of the package).

If you have the email, first and last name for a contact, you can determine what their email username syntax is. 

| Email            | First Name | Last Name |
| ---------------- | ---------- | --------- | 
| jsmith@gmail.com | John       | Smith     | 

We can extract information from the 3 base fields to produce a dataframe like this:

| Email            | First Name | Last Name | First Initial | Last Initial | Dot | Underscore | Username |
| ---------------- | ---------- | --------- | ------------- | ------------ | --- | ---------- | -------- |
| jsmith@gmail.com | john       | smith     | j             | s            | .   | _          | jsmith   |

Then, we can determine the position of the names, initial and common symbols in the email username.

<img src="images/positions.PNG" height="120px" />

If the ___ does not exist, we leave a 0.

| First Name | Last Name | First Initial | Last Initial | Dot | Underscore |
| ---------- | --------- | ------------- | ------------ | --- | ---------- |
| 0          | 2         | 1             | 0            | 0   | 0          | 

The username syntax code for this example is 021000. There are twenty possible codes with these six __ and you can find them all here.

### Determining A Company's Email Username Syntax

### Determining A Company's Email Domain

## Installation

The **filast** package can be installed directly from **GitHub** with

``` python
pip install git+https://github.com/jvanzalk/filast.git
from filast import companytools
```

If you encounter a bug, have usage questions, or want to share ideas to
make this package better, feel free to file an
[issue]().

## License
