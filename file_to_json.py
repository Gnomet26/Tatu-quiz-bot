import re

def validate_question_block(text, index):
    errors = []

    # Maxsus belgilar sonini tekshiramiz
    if text.count('%#') != 1 or text.count('#%') != 1:
        errors.append(f"Savol {index}: ❌ '%# ... #%'' savol formati xato (1 tadan bo'lishi kerak).")

    if text.count('%@') != 1 or text.count('@%') != 1:
        errors.append(f"Savol {index}: ❌ '%@ ... @%' formatida 1 ta to‘g‘ri javob bo‘lishi kerak.")

    if text.count('%$') != 3 or text.count('$%') != 3:
        errors.append(f"Savol {index}: ❌ 3 ta '%$ ... $%' noto‘g‘ri javob bo‘lishi kerak.")

    return errors


def parse_question_block(text):
    question = re.search(r'%#(.*?)#%', text, re.DOTALL).group(1).strip()
    correct = re.search(r'%@(.*?)@%', text, re.DOTALL).group(1).strip()
    wrongs = re.findall(r'%\$(.*?)\$%', text, re.DOTALL)

    options = [{"text": correct, "is_correct": True}]
    for w in wrongs:
        options.append({"text": w.strip(), "is_correct": False})

    return {
        "question": question,
        "options": options
    }


def process_questions_from_text(raw_text):
    # Har bir savol bloki %# bilan boshlanadi
    raw_blocks = re.split(r'(?=%#)', raw_text)
    all_results = []
    all_errors = []

    for i, block in enumerate(raw_blocks, start=1):
        block = block.strip()
        if not block:
            continue

        errors = validate_question_block(block, i)
        if errors:
            all_errors.extend(errors)
        else:
            try:
                parsed = parse_question_block(block)
                all_results.append(parsed)
            except Exception as e:
                all_errors.append(f"Savol {i}: ❌ Parsingda xatolik: {str(e)}")

    return all_results, all_errors
