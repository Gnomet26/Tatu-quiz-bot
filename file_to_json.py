import re

def validate_question_block(text, index):
    errors = []

    if text.count('%#') != 2:
        errors.append(f"Savol {index}: ❌ '%#' ochilishi/yopilishi to‘g‘ri emas.")

    if text.count('%@') != 1 or text.count('@%') != 1:
        errors.append(f"Savol {index}: ❌ '%@' va '@#' juftligi bo'lishi kerak.")

    wrong_open = text.count('%$')
    wrong_close = text.count('$%')
    if wrong_open != 3 or wrong_close != 3:
        errors.append(f"Savol {index}: ❌ 3 ta xato javob bo'lishi kerak (%$: {wrong_open}, $%: {wrong_close})")

    return errors

def parse_question_block(text):
    question = re.search(r'%#(.*?)%#', text, re.DOTALL).group(1).strip()
    correct = re.search(r'%@(.*?)@%', text, re.DOTALL).group(1).strip()  # <-- to‘g‘rilandi
    wrongs = re.findall(r'%\$(.*?)\$%', text, re.DOTALL)  # <-- to‘g‘rilandi

    options = [{"text": correct, "is_correct": True}]
    for w in wrongs:
        options.append({"text": w.strip(), "is_correct": False})

    return {
        "question": question,
        "options": options
    }

def process_questions_from_text(raw_text):
    blocks = [b.strip() for b in raw_text.strip().split('\n\n') if b.strip()]
    all_results = []
    all_errors = []

    for i, block in enumerate(blocks, start=1):
        errors = validate_question_block(block, i)
        if errors:
            all_errors.extend(errors)
        else:
            parsed = parse_question_block(block)
            all_results.append(parsed)

    return all_results, all_errors
