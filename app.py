from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# JSON 데이터 로드
def load_materials():
    with open('materials.json', 'r', encoding='utf-8') as f:
        return json.load(f)

materials_data = load_materials()

@app.route('/')
def index():
    return render_template('index.html', materials=materials_data)

@app.route('/calculate', methods=['POST'])
def calculate():
    anode = request.form.get('anode')
    cathode = request.form.get('cathode')
    supply_voltage = float(request.form.get('supply_voltage'))

    # 음극과 양극 재료의 전위 가져오기
    anode_potential = None
    cathode_potential = None

    for category in materials_data["anode_materials"]:
        if anode in materials_data["anode_materials"][category]:
            anode_potential = materials_data["anode_materials"][category][anode]["potential"]

    for category in materials_data["cathode_materials"]:
        if cathode in materials_data["cathode_materials"][category]:
            cathode_potential = materials_data["cathode_materials"][category][cathode]["potential"]

    if anode_potential is None or cathode_potential is None:
        return jsonify({'error': 'Invalid materials selected.'})

    cell_potential = cathode_potential - anode_potential
    efficiency = (cell_potential / supply_voltage) * 100

    # 수식 생성
    formula_voltage = f"E_{{cell}} = E_{{cathode}} - E_{{anode}} = {cathode_potential} - {anode_potential}"
    formula_efficiency = f"Efficiency = \\frac{{E_{{cell}}}}{{E_{{supply}}}} \\times 100 = \\frac{{{cell_potential}}}{{{supply_voltage}}} \\times 100"

    return jsonify({
        'cell_potential': cell_potential,
        'efficiency': efficiency,
        'supply_voltage': supply_voltage,
        'formula_voltage': formula_voltage,
        'formula_efficiency': formula_efficiency
    })

if __name__ == '__main__':
    app.run(debug=True)
