# Automation Scripts for Tribal Wars(klanlar)

## Features

* Auto Scavenge

### Auto Scavenge

- It only uses **spear** and **sword** units.
- It calculates the optimal number of units to deploy based on maximizing **resource collection per hour**.

## Config

### Sample Base Config:

You just need to change your baseUrl.

```yaml
gameInfo:
  baseUrl: "https://tr89.klanlar.org"
baseRequest:
  headers:
    accept: "application/json, text/javascript, */*; q=0.01"
    cache-control: "no-cache"
    content-type: "application/x-www-form-urlencoded; charset=UTF-8"
    pragma: "no-cache"
    tribalwars-ajax: "1"
    x-agentname: "test"
    x-correlationid: "test"
    x-requested-with: "XMLHttpRequest"

```

### Scavenge Config:

```yaml
- villageId: Your village id
  maxHours: integer (null=infinity)
  worldSpeed: 1
  options:
    ff: bool (isEnabled for Option 1)
    bb: bool (isEnabled for Option 2)
    ss: bool (isEnabled for Option 3)
    rr: bool (isEnabled for Option 4)

```

### Env variables:

| VAR    | Values   | Description                        |
|--------|----------|------------------------------------|
| ACTION | scavenge | select the mode of the application |

### Cookie

You need to place your cookie into the file '**resources/cookie.txt**'

## How to run

### With python

#### Scavenge Mode

> ACTION=scavenge python3 main.py

### With Docker

#### Build Image

> docker build --build-arg ACTION={your_action} -t {your_image_name} .

#### Run Container

> docker run {your_image_name}
