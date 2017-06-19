# Recover Ethereum wallet password

This repo does a few things:

- Builds a Docker container with Ethereum and Bitcoin python libraries
- Adapts the [pyethrecoverv3][perv3] in these ways:
  - Wallet file name and password parameters specified in environment
    variables that may be passed into the Docker container environment
  - Password search space is a string of length `PASSWD_LEN` randomly
    composed from an alphabet of 95 printable characters:
    alphanumeric
    ``0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ``
    and symbols ``!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~``
  - The search space may be crudely broken up for manual distribution
    across multiple containers by specifying an alphabet index range
    for the first character:  `SLICE_START=0` and `SLICE_END=20` means
    search only passwords beginning with the first 20 characters of
    the alphabet, `0123456789abcdefghij`.  A second container may be
    given `SLICE_START=20` and `SLICE_END=40`, and so on.

To use this repo, check it out into a directory and `cd` into it; copy
a json-formatted Ethereum v3 wallet to e.g. `mywallet.json`, and build
and run the container as follows:

```
# Build Docker container
docker build -t pyethrecover .
# Execute Docker container with current directory bind-mounted
docker run -it -w $PWD -v $PWD:$PWD \
    -e PASSWD_LEN=16 -e SLICE_START=0 -e SLICE_END=4 \
    -e WALLET_FILE=mywallet.json \
    pyethrecover ./doit.py
```

[perv3]: https://github.com/danielchalef/pyethrecoverv3
