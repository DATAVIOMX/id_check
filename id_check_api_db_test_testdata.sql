/* 
DATA INSERTION FOR TESTING THE DATABASE
AUTHOR: MOTOKO RESEARCH
DATE: 2019-12-20
*/


/* Data insertion */

INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (1, 'Otto',,'','');
INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (2, 'Omar',,'','');
INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (3, 'Fernando',,'','');
INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (4, 'Victoria',,'','');
INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (5, 'Hugo',,'','');
INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (6, 'Paco',,'','');
INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (7, 'Luis',,'','');
INSERT INTO users(userid, username, pwhash, creation_date, update_date, status, api_key, api_key_exp_date) VALUES (8, 'Donald',,'','');

INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (1,1,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (2,1,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (3,2,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (4,2,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (5,3,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (6,4,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (7,5,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (8,6,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (9,7,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (10,8,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (11,9,'','','','','');
INSERT INTO api-calls(callid, userid, api_key, call_date, call_point, status_code, call_text) VALUES (12,8,'','','','','');

/* IMAGES CAN BE STORED AS NUMPY ARRAY STRINGS
INSERT INTO TABLE images()
INSERT INTO TABLE images()
INSERT INTO TABLE images()
INSERT INTO TABLE images()
INSERT INTO TABLE images()
INSERT INTO TABLE images()
*/
