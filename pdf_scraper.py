from glob import glob
import PyPDF2
import re


def get_all_pdf_files():
    return glob("*.pdf")


def extract_data_from_pdf(pdf_file):
    data = {}
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()

        print(text, end=" ===\n")

    lines = text.split("\n")

    # print(lines[2])
    print(lines[3])

    # ll = "W001  WALKIN IN UNITED 1 DPD 13.80"

    # pattern = r"(\w+)\s+(.*?)\s+IN\s+(.*?)\s+(\d+)\s+(.*?)\s+(\S+)"
    # pattern = r"(\w+)\s+(.*?)\s+IN\s+(.*?)\s+(\d+)\s+(.*?)\s+\.\.\.\s+(\S+)"
    # pattern = r"(\w+)\s+(.*?)\s+IN\s+(.*?)\s+(\d+)\s+([^\s]+(?: [^\s]+)?)\s+(\S+)"
    pattern = r"(\w+)\s+(.*?)\s+IN\s+(.*?)\s+(\d+)\s+([^\s]+(?: [^\s]+)?)\s+(.*?)$"
    match = re.match(pattern, lines[3])

    if match:
        account_number = match.group(1)
        customer = match.group(2)
        destination = match.group(3)
        pieces = match.group(4)
        service = match.group(5)
        box_weight = match.group(6).split()[1]
        # ACCOUNT NUMBER CUSTOMER Origin Destination Pieces SERVICE Box Weight
        keys = [
            "ACCOUNT NUMBER",
            "CUSTOMER",
            "Destination",
            "Pieces",
            "SERVICE",
            "Box Weight",
        ]
        values = [account_number, customer, destination, pieces, service, box_weight]

        data = {key: value for key, value in zip(keys, values)}

        print(data)

        # print(
        #     account_number,
        #     customer,
        #     destination,
        #     pieces,
        #     service,
        #     box_weight,
        #     end="-----\n",
        # )

        return account_number, customer, destination, pieces, service, box_weight
    else:
        print("nai")
        return None

    # for line in lines:
    #     if re.match(r'^ACCOUNT NUMBER\s+', line):
    #         data['ACCOUNT NUMBER'] = line.split()[1]

    # patterns = {
    #     "ACCOUNT NUMBER": r"ACCOUNT NUMBER\s+(\S+)",
    #     "CUSTOMER": r"CUSTOMER\s+(.*?)\s+Origin",
    #     "Origin": r"Origin\s+(.*?)\s+Destination",
    #     "Destination": r"Destination\s+(\S+)",
    #     "Pieces": r"Pieces\s+(\S+)",
    #     "SERVICE": r"SERVICE\s+(\S+)",
    #     "Box Weight": r"Box Weight\s+(\S+)",
    # }

    # # Extract data using regex patterns
    # for key, pattern in patterns.items():
    #     match = re.search(pattern, text)
    #     if match:
    #         data[key] = match.group(1).strip()

    # return data


def main():
    pdf_files = ["1712647796-pdf2_A1107146-(1).pdf"]

    extract_data_from_pdf("1712647796-pdf2_A1107146-(1).pdf")

    # for pdf_file in pdf_files:
    #     print(f"Extracting data from {pdf_file}:")
    #     data = extract_data_from_pdf(pdf_file)
    #     for key, value in data.items():
    #         print(f"{key}: {value}")
    #     print("\n")


if __name__ == "__main__":
    # files = get_all_pdf_files()
    # print(files)
    main()
