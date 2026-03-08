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
            "ПОХОЖ НА: [имя известной знаменитости мирового или российского уровня]\n"
            "СИЛЬНЫЕ СТОРОНЫ:\n- [пункт 1]\n- [пункт 2]\n- [пункт 3]\n"
            "ЧТО УЛУЧШИТЬ:\n- [конкретный совет 1]\n- [конкретный совет 2]\n- [конкретный совет 3]\n"
            "ИТОГ: [1-2 предложения мотивации и честной оценки потенциала]\n\n"
            "Будь честным, конкретным и тактичным. Не льсти."
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