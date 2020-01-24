/*
 * id_check_db_prod_test_queries.sql
 * Purpose: Database for IDCheck API
 * Created: 2020-01-11
 * Author: Otto Hahn Herrera
 * NOTES:   
 * Database provides column level encryption for API keys, calls and responses
 * We are going to test the work insertions, deletions and modifications  
 */

/* User creation queries */
insert into users 
	(userid,
	creation_date,
	update_date,
	status,
	api_key,
	api_key_exp_date,
	calls_remaining)
	values (
	gen_random_uuid(),
	localtimestamp,
	localtimestamp,
	0,
	'MJfvgk91xkTdRyDNPc-TO1LhxK6fo_4a',
	localtimestamp,
	0
);

/* User modification queries */

update users set calls_remaining = 10 where api_key = 'MJfvgk91xkTdRyDNPc-TO1LhxK6fo_4a';

/* New call (user exists) */

insert into api_calls 
	(callid,
	userid,
	call_date,
	call_point,
	status_code,
	call_text,
	response) 
	values 
	(1,
	'1996024c-d64d-4ce9-a244-fcda97443c0f',
	localtimestamp,
	'id-check',
	'200',
	pgp_sym_encrypt('{"api_key":"MJfvgk91xkTdRyDNPc-TO1LhxK6fo_4a", "front":"value2", "back":"value3"}', 'longsecretencryptionkey'),
	pgp_sym_encrypt('{"success":"call successful"}', 'longsecretencryptionkey')
);



