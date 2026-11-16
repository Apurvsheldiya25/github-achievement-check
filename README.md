# GitHub achievement check

List the achievement names visible on a public GitHub profile with Python 3.9 or later. Run the script with the account's username.

```sh
python check_achievements.py octocat
```

The script reads the public achievements page once per run. It uses only the Python standard library and requires no credentials. Hidden badges and private contribution details are outside its scope. If GitHub changes the badge markup, the script may return an empty list.
