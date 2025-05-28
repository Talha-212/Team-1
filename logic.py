import time

def calculate_wpm_accuracy(start_time, typed_text, reference_text):
    elapsed_time = max(time.time() - start_time, 1)
    words = typed_text.strip().split()
    wpm = round(len(words) / (elapsed_time / 60))

    correct_chars = sum(1 for a, b in zip(typed_text, reference_text) if a == b)
    total_chars = len(reference_text)
    accuracy = round((correct_chars / total_chars) * 100) if total_chars else 0

    return wpm, accuracy

def highlight_errors(text_widget, typed_text, reference_text):
    text_widget.tag_remove("mistake", "1.0", "end")
    for i, (typed_char, ref_char) in enumerate(zip(typed_text, reference_text)):
        if typed_char != ref_char:
            index = f"1.0 + {i} chars"
            text_widget.tag_add("mistake", index, f"{index} +1c")
    text_widget.tag_config("mistake", foreground="red")
