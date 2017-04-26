# Really Nice Access Log Generator

## Run

```
$ python ./rnal_generator.py > access.log
```

## Configuration

* line.conf example

```
count   ip_address                    date          time                              time_offset     method    path                         bytes_sent            user_agent
325      172.28.22.68                  01/Apr/2017   {random_time:00:00:00,23:59:59}   0900            POST     /users  {random_int:59,121}  {random_file:user_agent.txt}
122      {random_file:ip_address.txt}  01/Apr/2017   {random_time:00:00:00,23:59:59}   0900            GET      /users/{random_int:234,999}  {random_int:59,121}  {random_file:user_agent.txt}
150      {random_file:ip_address.txt}  01/Apr/2017   18:23:15                          0900            GET      /posts?page={random_int:1,999}&page_size=20  23521 {random_file:user_agent.txt}
200      {random_file:ip_address.txt}  01/Apr/2017   18:23:15                          0900            GET      /posts?page={random_int:1,999}&page_size=20&keyword={random_file:keyword.txt}  23521 {random_file:user_agent.txt}
125      {random_file:ip_address.txt}  01/Apr/2017   {random_time:00:00:00,23:59:59}   0900            GET      /static/js/bootstra-min.js  23521 {random_file:user_agent.txt}

```

## Column keywords

to be
