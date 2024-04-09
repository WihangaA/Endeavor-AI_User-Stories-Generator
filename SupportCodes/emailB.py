import email

def get_body_from_eml_file(eml_file_path):
    with open(eml_file_path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)
    
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" or content_type == "text/html":
                body += part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')

    return body

eml_file_path = "sysX.eml" 
body_content = get_body_from_eml_file(eml_file_path)
print(body_content)