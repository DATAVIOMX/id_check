CREATE TABLE users(
    userid INTEGER AUTOINCREMENT PRIMARY KEY,
    username TEXT,
    pwhash TEXT,
    creation-date TEXT,
    update-date TEXT,
    status INT,
    api-key TEXT,
    api-key-exp-date TEXT
    );
    
CREATE TABLE api-calls(
    callid INTEGER AUTOINCREMENT PRIMARY KEY
    userid INTEGER FOREIGN KEY REFERENCES users(userid),
    api-key TEXT,
    call-date TEXT,
    call-point TEXT,
    status code INT,
    call-text TEXT
);


CREATE TABLE images(
imageid TEXT,
creation-date TEXT,
image BLOB,
img-type TEXT
);
