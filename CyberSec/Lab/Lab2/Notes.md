

# SSLHonorCipherOrder on
- Check encryption from left to right

# DO NOT DO
- SSLProtocol all -SSLv3
- SSLProxyProtocol all -SSLv3
## We do not allow all and ban some
## We ban all and use some
## Change to
- SSLProtocol -all +TLSv1.2 +TLSv1.3
 - SSLProxyProtocol -all +TLSv1.2 +TLSv1.3

# Note
- SSLVerifyClient require
- SSLVerifyDepth  10
# Server Root
- the server root is defined at httpd.conf
# Risk
- Using SSLCertificateKeyFile "${SRVROOT}/conf/ssl/ec-private-key.pem" while setting apache is very risky, risk of exposing your private key
-> Use other way to secure 


# Security modules
- All of the security setting is done in httpd-ssl.conf
- All of the modules needed will be load in httpd.conf
- By default the ssl module will not be load

![[Pasted image 20241109151627.png]]
Need this in order to use tls