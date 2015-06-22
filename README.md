# Timed Authentication POC

## What?

I've been looking for a way to avoid cleartext password to be sent when authenticating.
I wanted the system to be:

* Stateless;
* The hash sent over the wire should expire;
* Password highly resistant to BF if hash intercepted;
* Password highly resistant to BF if database is stolen;

## Files description

* timedauth.py: Flask REST api implementing the "Timed Authentication"
* cli.py: Python CLI to query that REST API
* auth.html: HTML/Javascript login to this REST API

## How

### Backend

On the backend, the hash stored in the database is computed using kdf(password, login, 20000).

When a request is made, the following logic is followed:

* sha256( password_hash + now ) is compared to the request's password;
* if no match, we drift 'now' of 15 seconds before and after and compute again;
* if any of those match, then the password was correct and the user is authenticated;
* if not, then either the password was wrong or the client/server's clock was skewed.

### Client

* When a client wants to authenticade, we compute sha256( kdf(password, login, 20000) + now )
* We send this hash as the password

## Who

I'd be happy to receive any feedback or comment you may have... You can reach me on:

* [@tgouverneur](https://twitter.com/tgouverneur)
* thomas <at> espix <dot> net

## Thanks

* [@aris_ada](https://twitter.com/aris_ada)
* [@tartinedeouf](https://twitter.com/tartinedeouf), my love ;-)
* Matthew, Ellie
