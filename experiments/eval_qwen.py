import pandas as pd
import numpy as np
from collections import Counter
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from transformers import AutoModelForCausalLM, AutoTokenizer
import ast
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
def get_corrected_sentence(text, model, tokenizer):
    system_message = "You are a helpful assistant that corrects punctuation errors in text. Take the text and correct it. Do not add any other text or comments."
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": text}
    ]
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True
    )
    model_inputs = tokenizer([prompt], return_tensors="pt").to(model.device)
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1000
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    result = tokenizer.decode(output_ids, skip_special_tokens=True)
    if '</think>' in result:
        result = result.split('</think>')[-1].strip()
    return result

punctuation_signs = ['!', ',', '.', '...', ':', '?']
def prepare_pred(text):
    tokens = [token for token in text.split(' ') if token != '']
    labels = []
    for token in tokens:
        if (len(token) > 3) and (token[-3:] == '...'):
            labels.append('...')
        elif token and token[-1] in punctuation_signs:
            labels.append(token[-1])
        else:
            labels.append('o')
    return labels

def evaluate_qwen_on_test(df, model, tokenizer):
    all_true = []
    all_pred = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Обработка тестовых данных"):
        text = row['clear_punct_lower']     
        true_labels = row['labels']         
        if isinstance(true_labels, str):
            true_labels = ast.literal_eval(true_labels)
        pred_text = get_corrected_sentence(text, model, tokenizer)
        pred_labels = prepare_pred(pred_text)
        min_len = min(len(true_labels), len(pred_labels))
        all_true.extend(true_labels[:min_len])
        all_pred.extend(pred_labels[:min_len])
    return all_true, all_pred

def calc_metrics_no_proba(y_true, y_pred):
    class_mapping = {
        'o': 0,
        '.': 1,
        ',': 2,
        '!': 3,
        '?': 4,
        ':': 5,
        '...': 6
    }
    n_classes = len(class_mapping)
    y_pred_enc = np.array([class_mapping[label] for label in y_pred])
    y_true_enc = np.array([class_mapping[label] for label in y_true])
    print('Доля пробелов:', (y_true_enc == 0).mean())
    print('Accuracy:', accuracy_score(y_true_enc, y_pred_enc))
    metrics = []

    counts = np.zeros(n_classes, dtype=int)
    for k, v in Counter(y_true_enc).items():
        counts[k] = v
    metrics.append(list(counts))

    f1 = f1_score(y_true_enc, y_pred_enc, average=None, labels=range(n_classes))
    precision = precision_score(y_true_enc, y_pred_enc, average=None, zero_division=0, labels=range(n_classes))
    recall = recall_score(y_true_enc, y_pred_enc, average=None, zero_division=0, labels=range(n_classes))
    metrics.append(list(f1))
    metrics.append(list(precision))
    metrics.append(list(recall))

    metrics_index = ['Count', 'F1-Score', 'Precision', 'Recall']
    df_metrics = pd.DataFrame(metrics, columns=class_mapping.keys(), index=metrics_index)
    return df_metrics

if __name__ == "__main__":
    df = pd.read_csv('/home/jovyan/Kozlov_KY/RuPunctNet/DL_experiments/new_books_prepared.csv', index_col=0)
    df['tokens'] = df.tokens.apply(ast.literal_eval)
    df['labels'] = df.labels.apply(ast.literal_eval)
    df = df[df.tokens.apply(len) < 200]
    df_train, df_val_test = train_test_split(df, test_size=0.2, random_state=999)
    df_val, df_test  = train_test_split(df_val_test, test_size=0.5, random_state=999)

    model_name = "Qwen/Qwen3-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="float16",
        device_map="cuda:0"
    )

    all_true, all_pred = evaluate_qwen_on_test(df_test, model, tokenizer)
    metrics = calc_metrics_no_proba(all_true, all_pred)
    print(metrics) 