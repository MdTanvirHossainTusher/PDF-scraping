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
            print(page_num, end="-------------------------------\n")
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
    # match = re.match(pattern, "W001  WALKIN IN UNITED KINGDOM 1 DPD EXPRESS ... 13.80")

    if match:
        account_number = match.group(1)
        customer = match.group(2)
        destination = match.group(3)
        pieces = match.group(4)
        service = match.group(5)
        box_weight = match.group(6).split()[1]

        # print(
        #     account_number,
        #     customer,
        #     destination,
        #     pieces,
        #     service,
        #     box_weight,
        #     end="-----\n",
        # )

        # return account_number, customer, destination, pieces, service, box_weight
    else:
        print("No value found!")
        # return None

    company = lines[5].split()
    if len(company) == 3:
        senders_company = company[0]
        recipients_company = company[1]
    elif len(company) >= 5:
        senders_company = " ".join(company[:2])
        recipients_company = " ".join(company[2:4])
    # print(senders_company)
    # print(recipients_company)

    names = lines[7].split()
    if len(names) == 3:
        senders_name = names[0]
        recipients_name = names[1]
    elif len(names) >= 5:
        senders_name = " ".join(names[:2])
        recipients_name = " ".join(names[2:4])
    # print(senders_name)
    # print(recipients_name)

    # Assuming address_line contains '1 GULDEHRA, 54 KURUKSHETRA 12 ASHFORD AVENUE, HAYES 13.80'
    # address_line = "1 GULDEHRA edd, 54 KURUKSHETRA ds 12 ASHFORD AVENUE, HAYES 13.80"
    # address_line = "GULDEHRA, KURUKSHETRA ds ASHFORD AVENUE, HAYES 13.80"
    address_line = lines[9]

    address = address_line.split(",")
    print(address)
    print(address[1][::-1])
    find_number = False
    recipients_address = ""
    first_address_second_half_idx = -1
    for idx, char in enumerate(address[1][::-1]):
        # print(idx, char, end="+++\n")
        if (char.isalpha() or char == " ") and not find_number:
            recipients_address += char
            # print("first")
        elif char.isdigit():
            recipients_address += char
            find_number = True
            # print("second")

        else:
            first_address_second_half_idx = idx
            break
            # print("third")
    senders_address_last_part = ""
    for c in address[2]:
        if c.isalpha() or c == " ":
            senders_address_last_part += c

    recipients_address = (
        f"{recipients_address[::-1]},{senders_address_last_part}".strip()
    )
    senders_address = (
        f"{address[0]},{address[1][::-1][first_address_second_half_idx + 1 :][::-1]}"
    )

    # print(senders_address)
    # print(recipients_address)

    chargeble_weight = lines[11]

    print(lines[12].split())

    pins_tel = lines[12].split()
    if lines[12][9].lower() == "t":
        senders_pin = lines[13].split(",")[0]
        senders_telephone = pins_tel[3]
        recipients_pin = pins_tel[5]
        recipients_telephone = pins_tel[8]
    else:
        senders_pin = pins_tel[1]
        senders_telephone = pins_tel[4]
        recipients_pin = pins_tel[6]
        recipients_telephone = pins_tel[9]

    goods_description_and_booking_date = lines[15].split("-")
    # print(goods_description_and_booking_date, end=" ,,, \n")
    goods_description = goods_description_and_booking_date[0][:-4]
    booking_date = goods_description_and_booking_date[1].split()[1]

    keys = [
        "ACCOUNT NUMBER",
        "CUSTOMER",
        "Destination",
        "Pieces",
        "SERVICE",
        "Box Weight",
        "SENDER'S COMPANY",
        "RECIPIENT'S COMPANY",
        "SENDER'S NAME",
        "RECIPIENT'S NAME",
        "SENDER'S ADDRESS",
        "RECIPIENT'S ADDRESS",
        "CHARGEABLE WT.",
        "SENDER'S PinCode",
        "SENDER'S TEL NO.",
        "RECIPIENT'S PinCode",
        "RECIPIENT'S TEL NO.",
        "DESCRIPTION OF GOODS",
        "BOOKING DATE",
    ]
    values = [
        account_number,
        customer,
        destination,
        pieces,
        service,
        box_weight,
        senders_company,
        recipients_company,
        senders_name,
        recipients_name,
        senders_address,
        recipients_address,
        chargeble_weight,
        senders_pin,
        senders_telephone,
        recipients_pin,
        recipients_telephone,
        goods_description,
        booking_date,
    ]

    data = {key: value for key, value in zip(keys, values)}

    # print(data)

    # # Extract data using regex patterns
    # for key, pattern in patterns.items():
    #     match = re.search(pattern, text)
    #     if match:
    #         data[key] = match.group(1).strip()

    # return data


def main():
    pdf_files = ["1712647796-pdf2_A1107146-(1).pdf"]

    extract_data_from_pdf("1712647796-pdf2_A1107144-(1).pdf")

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
