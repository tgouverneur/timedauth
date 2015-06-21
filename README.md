# Timed Authentication POC

## What?

Nowadays, SSL is not as trusted as it was 10 years ago. 
Thinking about it, I came up with this POC of "Timed Authentication".

The main difference with classic authentication, is that no cleartext password is transfered, but instead it's hashed together with the unix timestamp, making it unusable by any MITM attack.

On the server, there's a configurable allowed clock skew and hashes are computed around the NOW(), if nothing match the hash, the password was either wrong or the clock of the client (or the server!?) was skewed.

## Who

* [@tgouverneur](https://twitter.com/tgouverneur) on twitter
* thomas <at> espix <dot> net
