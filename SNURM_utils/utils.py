import json
from http.client import HTTPConnection


def rpad(s, N):
    spaces = " " * (N - len(s))
    return s + spaces


def lpad(s, N):
    spaces = " " * (N - len(s))
    return spaces + s


def status(jobs):
    header = (
        f"{rpad('ID',6)} │ {rpad('CMD',20)} │ {rpad('TIME',20)} │ {rpad('STATE',10)}"
    )
    print()
    print(header)
    print("─" * 7 + "┼" + "─" * 22 + "┼" + "─" * 22 + "┼" + "─" * 11)
    for job in jobs:
        ID = job["id"]
        cmd = job["cmd"]
        cmd = (cmd[: 16 - 2] + "..") if len(cmd) > 16 else cmd
        state = job["state"]
        if state == "CANCELLED":
            time = "-"
        elif state == "QUEUED":
            time = job["creation"]
        else:
            time = job["elapsed"]
        print(f"{ID:<6} │ {cmd:<20} │ {time:<20} │ {state:<10}")
    print()


def POST_req(obj, addr, port):
    c = HTTPConnection(addr, port)
    c.connect()
    encoded = json.dumps(obj).encode("utf-8")
    c.request(
        "POST",
        "/",
        body=encoded,
        headers={"Content-type": "application/json", "Content-length": len(encoded)},
    )
    response_bytes = c.getresponse().read()
    response_string = response_bytes.decode("utf-8")
    return json.loads(response_string)


def GET_req(path, addr, port):
    c = HTTPConnection(addr, port)
    c.connect()
    c.request(
        "GET",
        path,
    )
    response_bytes = c.getresponse().read()
    response_string = response_bytes.decode("utf-8")
    return json.loads(response_string)
