import re
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Загрузка
df = pd.read_csv("SMSSpamCollection", sep='\t', header=None, names=['label', 'message'])
df['label_encoded'] = (df['label'] == 'spam').astype(int)

# 2. Чистка
def clean_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['clean_message'] = df['message'].apply(clean_text)

# 3. Разделение (test 20% — не трогаем)
df_full_train, df_test = train_test_split(
    df, test_size=0.2, random_state=42, stratify=df['label_encoded']
)

# 4. TF-IDF + модель на full_train
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2)
X_full_train = vectorizer.fit_transform(df_full_train['clean_message'])

model = LogisticRegression(
    C=1.0, max_iter=1000, class_weight='balanced', random_state=42
)
model.fit(X_full_train, df_full_train['label_encoded'].values)

# 5. Сохранение (векторизатор + модель)
with open('model_spam.bin', 'wb') as f_out:
    pickle.dump((vectorizer, model), f_out)

print("Модель сохранена в model_spam.bin")