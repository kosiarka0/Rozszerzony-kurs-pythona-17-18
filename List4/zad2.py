def paragraphs(stream):
    last_sign = None
    ret_str = ""
    while True:
        sign = stream.read(1)
        if sign == "":
            yield ret_str
            return
        if last_sign == "\n" and sign == "\n":
            yield ret_str
            last_sign = None
            ret_str = ""
            continue
        if not last_sign:
            last_sign = sign
            continue

        ret_str, last_sign = (ret_str + last_sign), sign


def format_paragraph(paragraph, line_length):
    from textwrap import fill
    return fill(paragraph, line_length)


if __name__ == "__main__":
    with open("try.txt") as f:
        print("\n------\n".join(format_paragraph(para, 10) for para in paragraphs(f)))
