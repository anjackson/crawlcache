FROM python:3.9

RUN apt-get update && apt-get install -y curl build-essential openssl libssl-dev pkg-config

ARG SQUID_VERSION=4.13

# TODO: verify the squid download with the signing key
RUN mkdir /src \
    && cd /src \
    && wget http://www.squid-cache.org/Versions/v4/squid-$SQUID_VERSION.tar.xz \
    && mkdir squid \
    && tar -C squid --strip-components=1 -xvf squid-$SQUID_VERSION.tar.xz
    
RUN cd /src/squid && \
    ./configure \
        --prefix=/usr \
        --datadir=/usr/share/squid \
		--sysconfdir=/etc/squid \
		--localstatedir=/var \
		--mandir=/usr/share/man \
		--enable-inline \
		--enable-async-io=8 \
		--enable-storeio="ufs,aufs,diskd,rock" \
		--enable-removal-policies="lru,heap" \
		--enable-delay-pools \
		--enable-cache-digests \
		--enable-underscores \
		--enable-icap-client \
		--enable-follow-x-forwarded-for \
		#--enable-auth-basic="DB,fake,getpwnam,NCSA,NIS,PAM,POP3,RADIUS,SASL,SMB" \
		#--enable-auth-digest="file" \
		#--enable-auth-negotiate="kerberos,wrapper" \
		#--enable-auth-ntlm="fake" \
		#--enable-external-acl-helpers="file_userip,session,SQL_session,unix_group,wbinfo_group" \
		#--enable-url-rewrite-helpers="fake" \
		--enable-eui \
		--enable-esi \
		--enable-icmp \
		--enable-zph-qos \
		--with-openssl \
		--enable-ssl \
		--enable-ssl-crtd \ 
		--disable-translation \
		--with-swapdir=/var/spool/squid \
		--with-logdir=/var/log/squid \
		--with-pidfile=/var/run/squid.pid \
		--with-filedescriptors=65536 \
		--with-large-files \
		--with-default-user=proxy \
        --disable-arch-native \
        --disable-ipv6
		
ARG CONCURRENCY=1

RUN cd /src/squid && \
    make -j$CONCURRENCY && \
    make install

RUN /usr/libexec/security_file_certgen -c -s /var/spool/squid/ssl_db -M 16MB && chown -R proxy: /var/spool/squid/ssl_db

RUN chown proxy: /dev/stdout && chown proxy: /dev/stderr 
RUN mkdir /var/cache/squid && chown -R proxy: /var/cache/squid
RUN touch /var/run/squid.pid && chown proxy: /var/run/squid.pid

COPY *.* /etc/squid/

USER proxy

CMD squid -f /etc/squid/squid.conf -N -d 1

