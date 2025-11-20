import pandas as pd
import dns.resolver
import smtplib
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def email_exists(email):
    try:
        domain = email.split('@')[1]

        # MX record lookup
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange)

        # SMTP handshake
        server = smtplib.SMTP(timeout=10)
        server.connect(mx_host)
        server.helo(server.local_hostname)
        server.mail('validator@example.com')
        code, _ = server.rcpt(email)
        server.quit()

        return code == 250

    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Bulk Email Existence Checker (ODS + Progress Bar)"
    )

    parser.add_argument("-i", "--input", required=True, help="Input ODS file")
    parser.add_argument("-o", "--output", required=True, help="Output ODS file")
    parser.add_argument("-c", "--column", required=True, help="Column with emails")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Number of threads")

    args = parser.parse_args()

    print("\n📂 Loading dataset...")
    df = pd.read_excel(args.input, engine="odf")

    emails = df[args.column].tolist()
    results = {}

    print(f"🚀 Starting validation with {args.threads} threads...\n")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(email_exists, email): email for email in emails}

        for future in tqdm(as_completed(futures), total=len(emails), desc="Validating", ncols=80):
            email = futures[future]
            try:
                result = future.result()
            except:
                result = False
            results[email] = result

    # Map results back
    df["exists"] = df[args.column].map(results)

    print("\n💾 Saving output...")
    df.to_excel(args.output, engine="odf", index=False)

    print(f"\n✅ Completed.\n📄 Output saved to: {args.output}\n")


if __name__ == "__main__":
    main()

