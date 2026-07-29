# Sehno Bug Bounty Public Program List — Google Dorks

Source: https://github.com/sehno/Bug-bounty/blob/master/bugbounty_public_program_list.md

Use these Google dorks to discover bug bounty / VDP programs.

## Program Discovery Sites
- https://github.com/arkadiyt/bounty-targets-data/tree/master/data
- https://www.vulnerability-lab.com/list-of-bug-bounty-programs.php
- https://firebounty.com/

## Google Dorks for Responsible Disclosure Programs

### General
```
site:.eu responsible disclosure
inurl:responsible disclosure program
inurl:vulnerability disclosure program
inurl:vulnerability program rewards
inurl:security@ report vulnerability
inurl:bugbounty reward program
inurl /bug bounty
inurl : / security
inurl:security.txt
inurl:security "reward"
inurl : /responsible disclosure
inurl : /responsible-disclosure/ reward
inurl : / responsible-disclosure/ swag
inurl : / responsible-disclosure/ bounty
inurl:'/responsible disclosure' hoodie
```

### By Region
```
site .nl responsible disclosure
site .eu responsible disclosure
site .uk responsible disclosure
site .de inurl:bug inurl:bounty
site .cn intext:security report reward
```

### Platform-Specific
```
"powered by bugcrowd" -site:bugcrowd.com
"powered by hackerone" "submit vulnerability report"
"powered by synack"
"Submission Form powered by Bugcrowd" -bugcrowd.com
```

### Security.txt
```
inurl:/security ext:txt "contact"
inurl:/.well-known/security ext:txt
inurl:/.well-known/security ext:txt intext:hackerone
inurl:/.well-known/security ext:txt -hackerone -bugcrowd -synack -openbugbounty
inurl:security-policy.txt ext:txt
inurl:/security ext:txt "contact"
```

### University Programs
```
"responsible disclosure" university
inurl:/responsible-disclosure/ university
```

### Others
```
intext:"BugBounty" and intext:"BTC" and intext:"reward"
intext:bounty inurl:/security
inurl:"bug bounty" and intext:"€" and inurl:/security
inurl:"bug bounty" and intext:"$" and inurl:/security
inurl:"bug bounty" and intext:"INR" and inurl:/security
buy bitcoins "bug bounty"
"vulnerability reporting policy"
"If you believe you've found a security vulnerability"
```
