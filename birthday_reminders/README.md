# Birthday Reminders

List all birthdays that you want to check in the csv file. Keep the rows in the format "DATE(d.mm.yyyy), NAME". Execute `birthday_reminders.py`. 

Instead of using the python script, I have found a much simpler way to check if a friend has his birthday today. I keep the csv file, but instead of processing it with python, I will just use good old shell commands. 

```sh
cat /Users/david.kuda/dev/repos/python_automation/birthday_reminders/birthdays.csv \
  | grep $(date "+%d.%m.") \
  | xargs echo "birthday:"
```

output:
```
birthday: 14.09.1970, DaterDava
```

