CREATE TABLE users(
    userid INTEGER AUTO INCREMENT PRIMARY KEY,
    username TEXT,
    pwhash TEXT,
    creation_date TEXT,
    update_date TEXT,
    status INT,
    api_key TEXT,
    api_key_exp_date TEXT
    );
    
CREATE TABLE api_calls(
    callid INTEGER AUTO INCREMENT PRIMARY KEY,
    userid INTEGER,
    api_key TEXT,
    call_date TEXT,
    call_point TEXT,
    status_code INT,
    call_text TEXT,
    FOREIGN KEY(userid) REFERENCES users(userid)
);


CREATE TABLE images(
imageid TEXT,
creation_date TEXT,
image BLOB,
img_type TEXT
);
