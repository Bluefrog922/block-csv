import requests
import re

def unscramble_from_hex(encoded_string):
    result = ''
    for i in range(0, len(encoded_string), 2):
        char_code = int(encoded_string[i:i+2], 16)
        result += chr(char_code ^ 123 + i // 2 % 5)
    return result

def scrape_and_decode_domains(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            encoded_script = response.text
            domain_part = re.search(r'const domains=\[([\s\S]*?)\];', encoded_script).group(1)
            encoded_domains = re.findall(r"'(.*?)'", domain_part)
            decoded_domains = [unscramble_from_hex(domain) for domain in encoded_domains]
            return decoded_domains
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def check_domain_in_file(domain, filename):
    with open(filename, 'r') as file:
        existing_domains = {line.strip() for line in file}
        return domain in existing_domains

def write_domains_to_file(domains, filename):
    with open(filename, 'a+') as file:
        existing_domains = {line.strip() for line in file}
        for domain in domains:
            if domain not in existing_domains:
                file.write(domain + '\n')
                existing_domains.add(domain)

def process_domains(url, filename):
    decoded_domains = scrape_and_decode_domains(url)
    for domain in decoded_domains:
        if not check_domain_in_file(domain, filename):
            write_domains_to_file([domain], filename)

url = "https://random-proxy.com/"
output_file = "block.txt"
process_domains(url, output_file)
print(f"Random proxes written to {output_file}.")