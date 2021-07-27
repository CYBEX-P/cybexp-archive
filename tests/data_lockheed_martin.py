"""
Loads Lock Martin Cyber Kill Chain Data
(into RAM and MongoDB)
"""



from tahoe import Attribute, Object, Event, Instance, MongoBackend

Instance._backend = MongoBackend(dbname="demo_tahoe_db")

oid = "identity--e7c981ed-ab33-4d7a-b55d-db9413560040"

# =================================
# Event Email 1 ===================
# =================================

timestamp1 = 1236092478

received = ['(qmail 71864 invoked by uid 60001); Tue, 03 Mar 2009 15:01:19 +0000',
            'from [60.abc.xyz.215] by web53402.mail.re2.yahoo.com via HTTP; Tue, 03 Mar 2009 07:01:18 -0800 (PST)']
att_received_0 = Attribute('att_email_header_received', received[0])
att_received_1 = Attribute('att_email_header_received', received[1])
obj_received = Object('obj_email_header_received', [att_received_0, att_received_1])

from_ip = '60.abc.xyz.215'
from_email = 'dn...etto@yahoo.com'
att_from_ip = Attribute('ip', from_ip)
att_from_email = Attribute('email_addr', from_email)
obj_from = Object('from', [att_from_ip, att_from_email])

subject = 'AIAA Technical Committees'
att_subject = Attribute('subject', subject)
                  
to_email = 'johndoe1@lockheedmartin.com'
att_to_email = Attribute('email_addr', to_email)
obj_to = Object('to', att_to_email)

reply_to = 'dn...etto@yahoo.com'
att_reply_to = Attribute('email_addr', reply_to)
obj_reply_to = Object('reply_to', att_reply_to)

message_id = '<107017.64068.qm@web53402.mail.re2.yahoo.com>'
att_message_id = Attribute('message_id', message_id)

mime_ver = '1.0'
att_mime_ver = Attribute('mime_ver', mime_ver)

x_mailer = 'YahooMailWebService/0.7.289.1'
att_x_mailer = Attribute('x_mailer', x_mailer)

content_type = 'multipart/mixed; boundary="Boundary_(ID_Hq9CkDZSoSvBMukCRm7rsg)"'
att_content_type = Attribute('content_type', content_type)

body = """Please submit one copy (photocopies are acceptable) of this form, and one copy of nominee’s resume to: AIAA Technical Committee Nominations, 1801 Alexander Bell Drive, Reston, VA 20191. Fax number is 703/264-7551. Form can also be submitted via our web site at www.aiaa.org, Inside AIAA, Technical Committees"""
att_body = Attribute('body', body)

data = [obj_received, obj_from, att_subject, obj_to, obj_reply_to, att_message_id,
        att_mime_ver, att_x_mailer, att_content_type, att_body]
mal_data = [att_from_ip, att_from_email, att_subject, att_reply_to, att_message_id, att_body]
event_email_1 = Event('email', data, oid, timestamp1, mal_data=mal_data)
event_email_1.set_category('malicious')



# =================================
# Event Email 2 ===================
# =================================

timestamp2 = 1236151908

received = ['(qmail 97721 invoked by uid 60001); 4 Mar 2009 14:35:22 -0000',
            'from [216.abc.xyz.76] by web53411.mail.re2.yahoo.com via HTTP; Wed, 04 Mar 2009 06:35:20 PST']
att_received_0 = Attribute('att_email_header_received', received[0])
att_received_1 = Attribute('att_email_header_received', received[1])
obj_received = Object('obj_email_header_received', [att_received_0, att_received_1])

from_ip = '216.abc.xyz.76'
from_email = 'dn...etto@yahoo.com'
att_from_ip = Attribute('ip', from_ip)
att_from_email = Attribute('email_addr', from_email)
obj_from = Object('from', [att_from_ip, att_from_email])

subject = '7th Annual U.S. Missile Defense Conference'
att_subject = Attribute('subject', subject)
                  
to_email = 'johndoe2@lockheedmartin.com'
att_to_email = Attribute('email_addr', to_email)
obj_to = Object('to', att_to_email)

reply_to = 'dn...etto@yahoo.com'
att_reply_to = Attribute('email_addr', reply_to)
obj_reply_to = Object('reply_to', att_reply_to)

message_id = '<107017.64068.qm@web53402.mail.re2.yahoo.com>'
att_message_id = Attribute('message_id', message_id)

mime_ver = '1.0'
att_mime_ver = Attribute('mime_ver', mime_ver)

x_mailer = 'YahooMailWebService/0.7.289.1'
att_x_mailer = Attribute('x_mailer', x_mailer)

content_type = 'multipart/mixed; boundary="0-760892832-1236177320=:97248"'
att_content_type = Attribute('content_type', content_type)

body = "Welcome to the 7th Annual U.S. Missile Defense Conference"
att_body = Attribute('body', body)

data = [obj_received, obj_from, att_subject, obj_to, obj_reply_to, att_message_id,
        att_mime_ver, att_x_mailer, att_content_type, att_body]
#mal_data = [att_from_ip, att_from_email, att_subject, att_reply_to, att_message_id, att_body]
event_email_2 = Event('email', data, oid, timestamp2)




# =================================
# Event Email 3 ===================
# =================================


timestamp3 = 1237793508

received = ['(qmail 97721 invoked by uid 60001); 4 Mar 2009 14:35:22 -0000',
            '(qmail 82085 invoked by uid 60001); Mon, 23 Mar 2009 17:14:21 +0000',
            'from [216.abc.xyz.76] by web43406.mail.sp1.yahoo.com via HTTP; Mon, 23 Mar 2009 10:14:21 -0700 (PDT)']
att_received_0 = Attribute('att_email_header_received', received[0])
att_received_1 = Attribute('att_email_header_received', received[1])
att_received_2 = Attribute('att_email_header_received', received[2])                        
obj_received = Object('obj_email_header_received', [att_received_0, att_received_1, att_received_2])

from_ip = '216.abc.xyz.76'
from_email = 'ginette.c...@yahoo.com'
att_from_ip = Attribute('ip', from_ip)
att_from_email = Attribute('email_addr', from_email)
obj_from = Object('from', [att_from_ip, att_from_email])

subject = 'Celebrities Without Makeup'
att_subject = Attribute('subject', subject)
                  
to_email = 'johndoe3@lockheedmartin.com'
att_to_email = Attribute('email_addr', to_email)
obj_to = Object('to', att_to_email)

message_id = '<297350.78665.qm@web43406.mail.sp1.yahoo.com>'
att_message_id = Attribute('message_id', message_id)

mime_ver = '1.0'
att_mime_ver = Attribute('mime_ver', mime_ver)

x_mailer = 'YahooMailWebService/0.7.289.1'
att_x_mailer = Attribute('x_mailer', x_mailer)

content_type = 'multipart/mixed; boundary="Boundary_(ID_DpBDtBoPTQ1DnYXw29L2Ng)"'
att_content_type = Attribute('content_type', content_type)

body = ""
att_body = Attribute('body', body)

data = [obj_received, obj_from, att_subject, obj_to, att_message_id,
        att_mime_ver, att_x_mailer, att_content_type, att_body]
#mal_data = [att_from_ip, att_from_email, att_subject, att_reply_to, att_message_id, att_body]
event_email_3 = Event('email', data, oid, timestamp3)
