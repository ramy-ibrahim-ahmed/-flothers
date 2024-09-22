import re
import math
from urllib.parse import urlparse


def feature_extraction_pipeline(url):

    def url_length(url):
        return len(url)

    def domain_length(url):
        return len(url.split("/")[2]) if len(url.split("/")) > 2 else 0

    def path_length(url):
        return len(url.split("/", 3)[-1]) if len(url.split("/")) > 3 else 0

    def count_features(url, features):
        return {f"num{feature}": url.count(feature) for feature in features}

    def exist_features(url, features):
        return {
            f"is{feature}": 1 if url.count(feature) > 0 else 0 for feature in features
        }

    def contains_ipv4(url):
        ip_pattern = r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
        return 1 if bool(re.search(ip_pattern, url)) else 0

    def contains_ipv6(url):
        ipv6_pattern = (
            r"\b(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|"
            + r"([0-9a-fA-F]{1,4}:){1,7}:|"
            + r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|"
            + r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"
            + r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|"
            + r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|"
            + r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"
            + r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|"
            + r":((:[0-9a-fA-F]{1,4}){1,7}|:)|"
            + r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|"
            + r"::(ffff(:0{1,4}){0,1}:){0,1}"
            + r"((25[0-5]|(2[0-4]|1{0,1}[0-9]|[1-9]?)[0-9])\.){3,3}"
            + r"(25[0-5]|(2[0-4]|1{0,1}[0-9]|[1-9]?)[0-9])|"
            + r"([0-9a-fA-F]{1,4}:){1,4}:"
            + r"((25[0-5]|(2[0-4]|1{0,1}[0-9]|[1-9]?)[0-9])\.){3,3}"
            + r"(25[0-5]|(2[0-4]|1{0,1}[0-9]|[1-9]?)[0-9]))\b"
        )
        return 1 if bool(re.search(ipv6_pattern, url)) else 0

    def contains_ip_address(url):
        return 1 if contains_ipv4(url) or contains_ipv6(url) else 0

    def num_sub_domains(url):
        subdomains = url.split("http")[-1].split("//")[-1].split("/")
        return len(subdomains) - 1

    def contains_hexadecimal(url):
        hex_pattern = r"%[0-9A-Fa-f]{2}"
        return 1 if bool(re.search(hex_pattern, url)) else 0

    def calculate_entropy(url):
        string = url.strip()
        if not string:
            return 0.0
        frequency = {c: string.count(c) for c in set(string)}
        length = len(string)
        prob = [count / length for count in frequency.values()]
        entropy = -sum(p * math.log(p, 2) for p in prob if p > 0)
        return entropy

    def count_chars_domain_extension(url):
        url = url.split("//")[-1]
        domain = url.split("/")[0]
        last_dot_index = domain.rfind(".")
        if last_dot_index == -1:
            return -1
        ext = domain[last_dot_index + 1 :]
        return min(len(ext), 4) if ext.isalpha() else -1

    def is_port(url):
        try:
            parsed_url = urlparse(url)
            return 1 if parsed_url.port else 0
        except:
            return 0

    def count_digits_in_url(url):
        return sum(char.isdigit() for char in url)

    def count_chars_in_url(url):
        return sum(char.isalpha() for char in url)

    def count_special_in_url(url):
        return sum(not char.isalnum() for char in url)

    def host_exist(url):
        try:
            hostname = urlparse(url).hostname
            if hostname is None:
                return 0
            escaped_hostname = re.escape(hostname)
            return 1 if re.search(escaped_hostname, url) else 0
        except:
            return 0

    def num_parameters(url):
        params = url.split("&")
        return len(params) - 1

    def get_number_of_subdomains(url):
        domain = re.sub(r"^https?://", "", url).split("/")[0]
        domain_parts = domain.split(".")
        return len(domain_parts) - 2 if len(domain_parts) > 2 else 0

    # Extract features
    features = {
        "url_length": url_length(url),
        "domain_length": domain_length(url),
        "path_length": path_length(url),
        "is_IP": contains_ip_address(url),
        "num_sub_domains": num_sub_domains(url),
        "contains_hexadecimal": contains_hexadecimal(url),
        "entropy": calculate_entropy(url),
        "count_num_domain_extension": count_chars_domain_extension(url),
        "is_port": is_port(url),
        "digits_count": count_digits_in_url(url),
        "alpha_count": count_chars_in_url(url),
        "special_chars_count": count_special_in_url(url),
        "is_host": host_exist(url),
        "num_params": num_parameters(url),
        "num_subdomains": get_number_of_subdomains(url),
    }

    feature_list_1 = ["-", "=", ".", "%", "//", "_", "/"]
    feature_counts_1 = count_features(url, feature_list_1)
    features.update(feature_counts_1)

    feature_list_2 = [
        "@",
        "?",
        "#",
        "+",
        "http",
        "https",
        ".com",
        "www.",
        ".org",
        "&",
        ";",
        "~",
    ]
    feature_counts_2 = exist_features(url, feature_list_2)
    features.update(feature_counts_2)

    return features


def non_binary_columns():
    return [
        "url_length",
        "domain_length",
        "path_length",
        "num_sub_domains",
        "entropy",
        "count_num_domain_extension",
        "digits_count",
        "alpha_count",
        "special_chars_count",
        "num_params",
        "num_subdomains",
        "num-",
        "num=",
        "num.",
        "num%",
        "num//",
        "num_",
        "num/",
    ]
