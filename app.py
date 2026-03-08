from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import base64
import os
app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files['photo']
        image_data = base64.b64encode(file.read()).decode('utf-8')

        prompt = (
            "Ты эксперт по внешности и физиогномике. Оцени лицо человека на фото. "
"Ответь на русском языке строго в таком формате (без лишних слов, только этот формат):\n\n"
"ОЦЕНКА: [число от 1 до 10, можно дробное например 7.5]\n"
"АРХЕТИП: [одно из: Лис / Охотник / Красавчик / Олень / Медведь]\n"
"ОПИСАНИЕ АРХЕТИПА: [2-3 предложения что означает этот архетип, какие черты лица характерны, какие известные люди имеют этот архетип]\n"
"ПОХОЖ НА: [имя одной конкретной знаменитости мирового или российского уровня]\n"
"СИЛЬНЫЕ СТОРОНЫ:\n- [конкретная черта лица с деталями например: выразительные миндалевидные глаза с опущенными уголками]\n- [пункт 2]\n- [пункт 3]\n"
"ЧТО УЛУЧШИТЬ:\n- [конкретный actionable совет например: попробуй прическу crop fade или curtains чтобы подчеркнуть скулы]\n- [конкретный совет 2]\n- [конкретный совет 3]\n"
"ИТОГ: [2-3 предложения честной мотивирующей оценки с конкретным потенциалом]\n\n"
"Будь максимально конкретным, называй конкретные черты лица, конкретные прически, конкретные упражнения. Не давай общих советов."
        )

        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }],
            max_tokens=600
        )

        result_text = response.choices[0].message.content
        return jsonify({"success": True, "result": result_text})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run()