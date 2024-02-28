from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import matplotlib.image as mpl
import pandas as pd
from sklearn.cluster import KMeans
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/suapaleta')
def suapaleta():
    return render_template('suapaleta.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'imagem' not in request.files:
        return 'Nenhuma imagem no formulário'

    imagem = request.files['imagem']

    # Chama a função extrai_recurso
    features = extrai_recurso(imagem)

    if features is not None:
        # Chama a função gera_paleta
        gera_paleta(features)

        # Converte a imagem para base64 para exibi-la na página HTML
        img_str = img_to_base64(imagem)
        return render_template('resultado.html', imagem=img_str)
    else:
        return 'Erro ao processar a imagem'

def extrai_recurso(imagem):
    image = mpl.imread(imagem)
    if image is None:
        print(f"Erro ao carregar a imagem: {imagem}")
        return None
    # Transforma a imagem em uma matriz 1D
    image = image.reshape(-1, 3)
    return image

def gera_paleta(imagem):
    modelo = KMeans(n_clusters=5)
    novos_clusters = modelo.fit_predict(imagem)
    # Exibe a contagem de pixels em cada cluster
    print(pd.Series(novos_clusters).value_counts())

    # Visualiza a paleta de cores para a nova imagem
    new_palette_2 = modelo.cluster_centers_.astype(int)
    new_palette_hex = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in new_palette_2]
    plt.imshow([new_palette_2])
    plt.axis('off')
    plt.savefig('static/paleta.png')  # Salva a paleta como uma imagem
    plt.clf()

def img_to_base64(imagem):
    image = mpl.imread(imagem)
    img_str = BytesIO()
    plt.imsave(img_str, image)
    img_str.seek(0)
    img_base64 = base64.b64encode(img_str.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

if __name__ == '__main__':
    app.run(debug=True)
