# The simplest Message Queue server

_This is only for testing purposes._

## Prerequisites
- Python 3

## Run
Simply run it with a port,

On Linux:
```bash
./main.py [<port>]
```

Or on Windows:
```cmd
python ./main.py [<port>]
```

## Usage
Assuming it is run locally on port 8000 (default).

To push a new message:
```bash
curl -H 'Content-Type: text/html' -d '{"submission_id":5}' \
     localhost:8000/push/queue_name
```
Note: You can send anything in the body and it will be
pushed into the queue as a string, regardless of
the content-type header since it is simply ignored.

To pull a message:
```bash
curl localhost:8000/pull/queue_name
```
